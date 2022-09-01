"""
These are the main classes handling the `filerecords` registry.

The registry is a hidden directory containing the recorded files and their metadata.
"""

from datetime import datetime
import logging
import uuid
import os
import pandas as pd


import filerecords.api.utils as utils
import filerecords.api.settings as settings

logger = utils.log( level = logging.DEBUG )

class BaseRecord:
    """
    The basic record handling class for storing metadata.

    Parameters
    ----------
    filename : str
        The yaml file storing the record metadata.
    metadata : dict
        The metadata of the record.
    """
    def __init__(self, filename : str = None, metadata : dict = None ):
        self.metafile = filename
        self.metadata = metadata

        if self.metafile:
            self.load( self.metafile )

    def save( self ):
        """
        Save the metadata.
        """
        utils.save_yamlfile( self.metafile, self.metadata )

    def load( self, filename : str ):
        """
        Load yaml metadata from a file.
        
        Parameters
        ----------
        filename : str
            The path to the yaml file.
        """
        self.metafile = filename 
        self.metadata = utils.load_yamlfile( filename )

    def undo_comment( self ):
        """
        Undo the last comment.

        Note
        ----
        This will not automatically save the metadata,
        use the save() method to do so.
        """
        last = sorted( list( self.comments.keys() ) )[-1]
        self.metadata["comments"].pop( last )

    @property
    def comments( self ) -> dict:
        """
        Get the comments.
        """
        return self.metadata["comments"]
    
    @property
    def flags( self ) -> list:
        """
        Get the flags.
        """
        return self.metadata["flags"]

    def add_comment( self, comment : str ):
        """
        Add a comment to the registry.

        Note
        ----
        This will not automatically save the metadata,
        use the save() method to do so.

        Parameters
        ----------
        comment : str
            The comment to add.
        """
        user = os.environ["USER"] 
        self.metadata["comments"].update(  { datetime.now() : {
                                                                 "comment" : comment, 
                                                                 "user" : user 
                                                            } 
                                            }  )

    
    
    def add_flags( self, flag : str or list ):
        """
        Add a new flag to the registry.

        Note
        ----
        This will not automatically save the metadata,
        use the save() method to do so.

        Parameters
        ----------
        flag : str or list
            The flag(s) to add.
        """
        if not isinstance( flag, list ):
            flag = [ flag ]
        logger.debug( "Adding flags: {}".format( flag ) )

        self.metadata["flags"].extend( flag )
        logger.debug( "(before set) metadata['flags']: {}".format( self.metadata["flags"] ) )

        self.metadata["flags"] = list( set( self.metadata["flags"] ) )
        logger.debug( "(after set) metadata['flags']: {}".format( self.metadata["flags"] ) )

class Registry(BaseRecord):
    """
    The main class of a filrecords registry. It loads the registry 
    information from a parent directory and makes the data accessible.

    Parameters
    ----------
    directory : str
        The directory to load the registry from.
    """
    def __init__(self, directory : str ):
        super().__init__()

        self.directory = os.path.abspath( directory ) 
        self.registry_dir = self._find_registry()

        self.index = None
        self.indexfile = utils.get_indexfile( self.registry_dir )
        self.metafile = utils.get_metafile( self.registry_dir )
        
        self._load_registry()

    def init( self ):
        """
        Initialize a new registry in the given directory.
        """
        utils.make_new_registry( self.directory )

    def save( self ):
        """
        Save the registry state and updated metadata.
        """
        self.index.to_csv( self.indexfile, index = False, sep = "\t" )
        super().save()

    def _find_registry( self ):
        """
        Finds the local registry associated with the given directory.
        This will parse the directory hierarchy upwards until it finds a registry.
        If none are found it will initialize a new registry in the given directory.
        """
        registry_dir = utils.find_registry( self.directory )

        if registry_dir is None:
            logger.info( "No local registry found. Initializing a new registry." )
            self.init()
            registry_dir = os.path.join( self.directory, settings.registry_dir )
        
        return registry_dir

    def _load_registry( self ):
        """
        Loads the registry data from the indexfile and metafile
        """
        self.index = utils.load_indexfile( self.indexfile )
        self.metadata = utils.load_yamlfile( self.metafile )


    def get_record( self, filename : str ):
        """
        Get the record of a file in the registry.

        Parameters
        ----------
        filename : str
            The filename of the file to get the record of.

        Returns
        -------
        FileRecord or list
            The record of the file or a list of records.
        """
        match = os.path.relpath( filename, self.registry_dir )
        match = self.index["relpath"].str.contains( filename )
        
        if match.any():

            if match.sum() > 1:
                logger.warning( f"More than one record found for {filename}." )
                return [ FileRecord( registry = self, id = i ) for i in self.index.loc[match, "id"].values ] 
            
            id = self.index.loc[match, "id"].values[0]
            return FileRecord( registry = self, id = id )

        return None

    @property
    def groups( self ) -> dict:
        """
        Get the defined flag-groups.
        """
        return self.metadata["groups"]

    def add_group( self, label : str, flags : list ):
        """
        Add a flag group to the registry.


        Note
        ----
        This will not automatically save the registry's metadata,
        use the save() method to do so.

        Parameters
        ----------
        label : str
            The label of the group.
        flags : list
            The flags of the group.
        """
        if not isinstance( flags, list ):
            flags = [ flags ]
        flags += [ f"group:{label}" ]

        self.metadata["groups"].update( { label : flags  } )
        self.add_flags( flags )

    def add( self, filename : str, comment : str, flags : list = None ):
        """
        Add a new file to the registry.

        Parameters
        ----------
        filename : str 
            The filename of the file to add.
        comment : str
            The comment to add to the file.
        flags : list
            Any flags to add. This can also be a defined flag-group label.
        """
        if not os.path.exists( filename ):
            raise FileNotFoundError( f"File {filename} does not exist. Can only comment existing files..." )
        
        record = FileRecord( registry = self, filename = filename )
        new_id = record.id
        record.add_comment( comment )
    
        if flags:
            record.add_flags( flags )
        
        index_entry = pd.DataFrame( { "id" : [new_id], "filename" : [filename], "relpath" : [record.relpath] } )
        self.index = self.index.append( index_entry, ignore_index = True )

        record.save()
        logger.info( f"Added {filename} to the registry." )


    def remove( self, filename : str ):
        """
        Remove a file from the registry.

        Parameters
        ----------
        filename : str
            The filename of the file to remove.
        """
        record = self.get_record( filename )
        if record is None:
            logger.warning( f"No record found for {filename}." )
            return

        os.system( f"rm {record.metafile}" )
        self.index = self.index[ self.index.filename != filename ]
        
        self.save()
        logger.info( f"Removed {filename} from the registry." )

    def update( self, filename : str, comment : str = None, flags : (str or list) = None ):
        """
        Update an existing file record.

        Parameters
        ----------
        filename : str
            The filename of the file to update.
        comment : str
            The new comment to add to the file.
        flags : str or list
            The new flags to add to the file.
        """
        record = self.get_record( filename )

        if record is None:
            logger.warning( f"No record found for {filename}." )
            return

        elif isinstance( record, list ):
            logger.warning( f"More than one record found for {filename}, can only edit one record at a time." )
            return

        if comment:
            record.add_comment( comment )
        if flags:
            record.add_flags( flags )

        record.save()
        logger.info( f"Updated {filename} in the registry." )

    def search( self, filename_pattern: str = None, flag : str = None ):
        """
        Search for records in the registry either through a filename pattern or by a flag.

        Parameters
        ----------
        filename_pattern : str
            The filename pattern to search for.
        flag : str
            The flag to search for. Note, this can only be a single flag!
            To search for multiple flags, first define a flag-group and then search
            for the group label using `group:yourgroup`. 
        
        Returns
        -------
        list
            A list of FileRecord objects of record entries matching the search criteria.
        """
        records = None

        if filename_pattern:
            records = self.index["filename"].str.contains( filename_pattern )
            records = self.index.loc[records, "id"].values
            records = [ FileRecord( self, id = id ) for id in records ]
        
        if flag:
            if not records:
                records = [ FileRecord( self, id = id ) for id in self.index.id ]
            records = [ i for i in records if flag in i.flags ]
        
        if not filename_pattern and not flag:
            logger.warning( "No search criteria specified, returning all records." )
            records = [ FileRecord( self, id = id ) for id in self.index.id ]
        
        return records

    def move( self, current : str, new : str, move_file : bool = True ):
        """
        Move a file to a new location.

        Parameters
        ----------
        current : str
            The filename of the file to move.
        new : str
            The new filename to move the file to.
        move_file : bool
            If True the file moving will also be performed.
            If False only the path reference is adjusted within the registry.
        """
        record = self.get_record( current )

        if record is None:
            logger.warning( f"No record found for {current}." )
            return

        elif isinstance( record, list ):
            logger.warning( f"More than one record found for {current}, can only edit one record at a time." )
            return

        path = os.path.relpath( current, self.registry_dir)
        self.index.loc[ self.index.relpath == path, "relpath" ] = os.path.relpath( new, self.registry_dir )

        if move_file:
            os.system( f"mv {current} {new}" )

        self.save()

class FileRecord(BaseRecord):
    """
    This class represents a single file record entry.

    Parameters
    ----------
    registry : Registry
        The registry the file record is associated with.
    id : str 
        The unique identifier of the file record.
        If none is provided, a new id is created.
    filename : str 
        The filename of the file to record (if a new record is being created).
    """
    def __init__( self, registry : Registry, id : str = None, filename : str = None ):
        super().__init__()
        self.registry = registry
        self.filename = filename

        if id is None:

            if filename is None:
                raise ValueError( "A filename must be provided when adding a new file record." )
            
            _init_new = True
            self.id = uuid.uuid4()

        else:

            _init_new = False
            self.id = id


        self.relpath = self._get_relpath()
        self.filename = self._get_filename()

        self.metafile = os.path.join( self.registry.registry_dir, str(self.id) )
        if _init_new:
            utils._init_entryfile( self.registry.registry_dir, str(self.id) )
        
        self.load()

    def load( self ):
        """
        Loads the file records.

        Note
        ----
        This is done automatically during init if an existing file is specified.
        """
        super().load( self.metafile )

    def save( self ):
        """
        Save the file record.
        This will also save the the 
        registry state at the same time.
        """
        super().save()
        self.registry.save()

    def add_flags( self, flags : str or list ):
        """
        Add flags to the metadata.

        Note
        ----
        This will not automatically save the metadata,
        use the save() method to do so.

        Parameters
        ----------
        flags : str or list
            The flag(s) to add. 
            This can also be a defined flag-group label.
        """
        get_group_flags = lambda x: self.registry.groups[x] if x in self.registry.groups else [x]
        if isinstance( flags, list ):
            flags = [ get_group_flags( flag ) for flag in flags ]
        else:
            flags = get_group_flags( flags )
        super().add_flags( flags )
        self.registry.add_flags( flags )

    def _get_relpath(self):
        """
        Make the path of the recorded file relative to the registry.
        """

        # logger.debug( f"Registry index: {self.registry.index}" ) 
        ids = self.registry.index.id.astype(str)

        if str(self.id) in ids:
            return self.registry.index.loc[ids == str(self.id), "relpath"].values[0]
        
        else:

            relpath = os.path.relpath( self.filename, self.registry.registry_dir )

            if relpath in self.registry.index.relpath.values:
                directory = os.path.relpath( os.path.dirname(relpath), self.registry.directory ) 
                raise FileExistsError( f"File {self.filename} within {directory} already exists in the registry." )
        
            return relpath

    def _get_filename( self ):
        """
        Get the filename of the file record.
        """
        ids = self.registry.index.id.astype(str)
        if str(self.id) in ids:
            return self.registry.index.loc[ids == str(self.id), "filename"].values[0]
        return os.path.basename( self.filename )

    def __repr__( self ):
        return f"FileRecord( id = {self.id}, filename = {self.filename} )"


class Manifest:
    """
    This class assembles a YAML or markdown manifest of all recorded entries within a registry.
    
    Parameters
    ---------- 
    registry : Registry
        The source registry.
        {}
    """
    def __init__( self, registry : Registry ):
        self.registry = registry
        self._dict = None
        self._markdown = None

    def to_yaml( self, filename : str = None ):
        """
        Convert the source registry to a single YAML file.

        Parameters
        ----------
        filename : str
            The filename of the YAML file to create.
            If none is provided a "registry.yaml" file is created.
        """

        self._dict = dict( self.registry.metadata )
        self._dict["directory"] = self.registry.directory

        records = [ FileRecord( self, id = id ) for id in self.registry.index.id ]
        filepaths = self.registry.index.relpath.apply( lambda x: os.path.relpath( x, self.registry.directory ) ).values        
        
        entry = lambda record, path : {
                                        "name" : os.path.basename( path ),
                                        "path" : path,
                                        "flags" : record.flags,
                                        "comments" : record.comments
                                    }
        entries = { filepath : entry( record, filepath ) for record, filepath in zip( records, filepaths ) }
        self._dict[ "records" ] = entries

        if filename is None:
            filename = f"{self.registry.directory}/{settings.registry_export_name}.yaml"
        utils.save_yamlfile( filename, self._dict )

    def to_markdown( self, filename : str = None ):
        """
        Convert the source registry to a markdown file summary.
        
        Parameters
        ----------
        filename : str
            The name of the markdown file. 
            If none is provided a "registry.md" file is created.
        """

        # add basic information and timestamp of manifest creation
        self._markdown = f"# {self.registry.directory}\n\n"
        self._markdown += f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # the format in which comment shall be included in the markdown file
        comment_format = lambda comment, name, timestamp : f"{comment}  |  {name} @ {timestamp.strftime('%Y-%m-%d %H:%M:%S')}"

        # add registry's own comments
        self._markdown += "## Registry comments\n\n"
        for timestamp in self.registry.comments:
            comment, user = list( self.registry.comments[timestamp].values() )
            text = f"{comment_format( comment, user, timestamp)}\n\n"
            self._markdown += text


        # add all flags and flag groups
        self._markdown += "## Registered flags\n\n"
        for i in sorted( self.registry.flags ):
            self._markdown += f"- {i}\n"
        self._markdown += "\n"

        self._markdown += "### Flag groups\n\n"
        self._markdown += "| Group | Flags |\n"
        self._markdown += "|------|------|\n"
        for label, flags in self.registry.groups.items():
            self._markdown += f"| {label} | {', '.join(flags)} |\n"
        self._markdown += "\n\n"

        # add all records
        self._markdown += "## Records \n\n---------\n\n"

        for record in self.registry.index.id:
            record = FileRecord( self.registry, id=record )
            text += f"### {record.relpath[3:]}\n\n"
            flags = '\n- '.join( record.flags )
            text += f"- {flags}\n\n"
            text += "#### Comments\n\n"
            for timestamp in record.comments:
                comment, user = list( record.comments[timestamp].values() )
                text += f"{comment_format( comment, user, timestamp)}\n\n"
            self._markdown += text

        # now save the markdown file
        if filename is None:
            filename = f"{self.registry.directory}/{settings.registry_export_name}.md"
        with open( filename, "w" ) as f:
            f.write( self._markdown )


    @property
    def index( self ):
        return self.registry.index
    
    @property
    def metadata( self ):
        return self.registry.metadata
    
    @property
    def groups( self ):
        return self.registry.groups
    
    @property
    def directory( self ):
        return self.registry.directory
    
    @property
    def registry_dir( self ):
        return self.registry.registry_dir
    
    @property
    def flags( self ):
        return self.registry.flags