"""
`Registry` is the main class handling the `filerecords` registry.
The registry itself is a hidden directory containing the records of files and directories in yaml format.


API Usage
=========

In the code API, a registry can be accessed by setting up a Registry object, which will automatically locate the 
closest available registry, but can also initialize a new registry. 

.. code-block:: python

    from filerecords.api import Registry

    # Call a registry from the current directory.
    reg = Registry()


Initializing new registries
---------------------------

The above code will try to find a registry in any directory that higher in the directory tree than the current directory.
If none is found, a new registry is automatically initialized in the current directory.

In case a registry is found, the registry can be accessed now. However, a new registry can still be initialized in the current directory
by calling `reg.init()`.

.. code-block:: python

    # Initialize a new registry in the current directory 
    # (even if a registry was found in a parent directory).
    reg.init()


Accessing the registry
----------------------

The registry's own metadata can be accessed via the `comments` and `flags` attributes directly.

.. code-block:: python

    # Get the registry's comments.
    reg.comments

    # Get the registry's flags.
    reg.flags

    # Get the defined flag groups.
    reg.groups


New comments and flags can be added to the registry itself using the `add_comment()` and `add_flags()` methods.

.. code-block:: python

    # Add a new comment.
    reg.add_comment( "This is a new comment." )

    # Add a new flag.
    reg.add_flag( "new_flag" )  


After editing the comments or flags of a registry, the changes must be saved using the `save()` method.

.. code-block:: python

    # Save the registry.
    reg.save()


To access records from the registry the `get_record()` method can be used.

.. code-block:: python

    # Get a record from the registry.
    record = reg.get_record( "path/to/file" )

    # e.g. 
    record = reg.get_record( "results/gsea_20082022.tsv" )


This will return a `FileRecord` object which now allows to access the metadata of the file.

Alternatively, if the precise filename is not known or a number of files shall be found, the `search()` 
method can be used to find records based on their flags or on regex patterns in their filenames.

.. code-block:: python

    # Search for records with the "important" flag.
    records = reg.search( flag = "important" )

    # Search for records with the "important" flag and which are bam files.
    records = reg.search( flag = "important", pattern = ".*\.bam" )


.. note::

    Search always applies *and* logic to to the pattern and flag. Only a single flag is supported for searching.
    To include multiple flags in a search, first define a flag group and then search for the group's label flag.

    For instance, assume we wish to search for flags "important" and "results" at the same time.
    We first create a group (see below) containing these flags and then search for the group. Then we need to flag our files of interest
    with the group. This is not an ideal system yet and may be updated in the future.


Flags and flag groups
---------------------

Flags are used to mark files in the registry. They can be used to mark files as important, as results, as temporary files, etc.
They are a shorthand for the details in the comments. Often it is desirable to add multiple flags at the same time to a file. To 
avoid having to repeatedly add multiple flags at the same time, registries support `flag groups` which summarize multiple flags by one label.

.. code-block:: python

    # Add a new flag group
    reg.add_group( "supergroup", ["important", "results"] )

    # now add a new file and flag it as member of the supergroup
    reg.add( "my_superfile.txt", comment = "superfile", flags = "supergroup" )

    # search for all files flagged as supergroup
    records = reg.search( flag = "group:supergroup" )


Adding and editing records
--------------------------

New files can be added to the registry using the `add()` method. 
If a file is already recorded, the `update()` method must be used instead.

.. code-block:: python

    # add a "results/" directory to the registry
    reg.add( "results/", comment = "the main results", flags = ["results", "important"] )

    # to now add additional comments or flags to the "results/" directory use update instead
    reg.update( "results/", comment = "an additional comment about the results", flags = ["perhaps_another_flag"] )


Records (i.e. files or directories) can be `moved` and/or `removed` from the registry. By default these actions also affect the files in the filesystem.
I.e. a file is by default also deleted if it is removed from the registry - this can be controlled, however.

.. code-block:: python

    # Move a file to a new location.
    record.move( "/path/to/file", "new/path/to/file" )

    # Only adjust the references in the registry 
    # (maybe because you already moved the file and forgot to update the registry).
    record.move( "/path/to/file", "new/path/to/file", keep_file = True )

    # Remove a record from the registry.
    record.remove( "/path/to/file" )

    # Only remove the references in the registry but keep the file in the filesystem.
    record.remove( "/path/to/file", keep_file = True )


Exporting the contents of the registry
--------------------------------------

The registry contents can be represented in markdown format using the `to_markdown()` method, 
or in yaml format using the `to_yaml()` method.

.. code-block:: python

    # Export the registry to a markdown file.
    reg.to_markdown( timestamp = True, filename = "registry.md" )

    # Export the registry to a yaml file.
    reg.to_yaml( timestamp = True, filename = "registry.yaml" )

"""

from datetime import datetime
import shutil
import os
import subprocess
import pandas as pd


import filerecords.api.base as base
import filerecords.api.file_record as file
import filerecords.api.utils as utils
import filerecords.api.settings as settings

logger = utils.log()

class Registry(base.BaseRecord):
    """
    The main class of a filrecords registry. It loads the registry 
    information from a parent directory and makes the data accessible.

    Note
    
        This class will search for existing registries automatically in the filesystem and 
        initialize a new registry if none are found. However, even if one is found a new registry can be
        initialized in the current directory by calling `init()`.

    Parameters
    ----------
    directory : str
        The directory to load the registry from. 
        By default the current working directory is used. 
    """
    def __init__(self, directory : str = "." ):
        super().__init__()

        # self.directory = os.path.abspath( directory ) 
        self.directory = subprocess.check_output( f"cd {directory} ; pwd", shell = True ).decode().strip()
        
        self.index = None

        self._initialized = False
        self._find_registry()
        
        if not self._initialized:
            self._load_registry()

    def init( self, permissions : (int or str) = None ):
        """
        Initialize a new registry in the given directory.

        Parameters
        ----------
        permissions : int or str
            The permissions to use for the registry directory. 
            By default the permissions of the parent directory are used.
        """
        self._initialized = True
        utils.make_new_registry( self.directory, perms = permissions )

        self.registry_dir = os.path.join( self.directory, settings.registry_dir ) 
        self._load_registry()

    def save( self ):
        """
        Save the registry state and updated metadata.
        """
        self.index.to_csv( self.indexfile, index = False, sep = "\t" )
        super().save()

    
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
        logger.debug( f"directory={self.directory}")
        logger.debug( f"registry_dir={self.registry_dir}")
        filename = os.path.join( self.directory, filename )
        logger.debug( f"filename={filename}" )
        match = os.path.relpath( filename, self.registry_dir )
        logger.debug( f"match={match}" )

        match = self.index.relpath == match 
        logger.debug( f"match={match}" )

        if match.any():

            if match.sum() > 1:
                logger.warning( f"More than one record found for {filename}." )
                return [ file.FileRecord( registry = self, id = i ) for i in self.index.loc[match, "id"].values ] 
            
            id = self.index.loc[match, "id"].values[0]
            return file.FileRecord( registry = self, id = id )

        return None

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

    def add( self, filename : str, comment : str = None, flags : list = None ):
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
        
        if not comment and not flags:
            raise ValueError( "No flags or comment given. At least one must be given." )


        record = file.FileRecord( registry = self, filename = filename )
        new_id = record.id

        logger.debug( f"adding: {filename} (filename = { os.path.basename(record.relpath) })" )
        
        if comment:
            record.add_comment( comment )
    
        if flags:
            record.add_flags( flags )
        
        index_entry = pd.DataFrame( { "id" : [new_id], "filename" : [os.path.basename(record.relpath)], "relpath" : [record.relpath] } )
        self.index = pd.concat( [self.index, index_entry], ignore_index = True )

        record.save()
        # logger.info( f"Added {filename} to the registry." )


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
        # logger.info( f"Updated {filename} in the registry." )

    def search( self, pattern: str = None, flag : str = None ):
        """
        Search for records in the registry either through a filename pattern or by a flag.

        Parameters
        ----------
        pattern : str
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

        if pattern:
            records = self.index["filename"].str.contains( pattern, regex = True )
            if records.sum() == 0:
                logger.warning( f"No records found for pattern {pattern}." )
            else:
                records = self.index.loc[records, "id"].values
                records = [ file.FileRecord( self, id = id ) for id in records ]
        
        if flag:
            if not records:
                records = [ file.FileRecord( self, id = id ) for id in self.index.id ]
            records = [ i for i in records if flag in i.flags ]
        
        if not pattern and not flag:
            logger.warning( "No search criteria specified, returning all records." )
            records = [ file.FileRecord( self, id = id ) for id in self.index.id ]

        return records

    def move( self, current : str, new : str, keep_file : bool = False ):
        """
        Move a file to a new location.

        Parameters
        ----------
        current : str
            The filename of the file to move.
        new : str
            The new filename to move the file to.
        keep_file : bool
            If True only the path reference is adjusted within the registry.
            If False the file moving will also be performed.
        """
        record = self.get_record( current )

        if record is None:
            logger.warning( f"No record found for {current}." )
            return

        elif isinstance( record, list ):
            logger.warning( f"More than one record found for {current}, can only edit one record at a time." )
            return

        # Note: the {}_path are relative to the registry dir and therefore
        # registry internal, while the actual current and new are relative to the users
        # current working directory and must not be altered for file moving...

        current_path = os.path.relpath( current, self.registry_dir )
        new_path = os.path.relpath( new, self.registry_dir )
        mask = self.index.relpath == current_path
        
        self.index.loc[ mask, "relpath" ] = new_path
        self.index.loc[ mask, "filename" ] = os.path.basename( new )

        if not keep_file:
            os.rename( current, new )

        self.save()

    def remove( self, filename : str, keep_file : bool = False ):
        """
        Remove a file from the registry.

        Parameters
        ----------
        filename : str
            The filename of the file to remove.
        keep_file : bool
            If True, the file will not be removed from the filesystem, only its records in the registry.
        """
        record = self.get_record( filename )
        if record is None:
            logger.warning( f"No record found for {filename}." )
            return

        if not keep_file:
            if os.path.isfile( filename ):
                os.remove( filename )
            elif os.path.isdir( filename ):
                shutil.rmtree( filename )
            else:
                logger.warning( f"{filename} is not a file or directory. Cannot remove." )

        os.remove( record.metafile )
        self.index = self.index[ self.index.id != record.id ]
        
        self.save()
        # logger.info( f"Removed {filename} from the registry." )


    def to_yaml( self, include_records : bool = True, timestamp : bool = False, filename : str = None ):
        """
        Convert the source registry to a single YAML file.

        Parameters
        ----------
        include_records : bool
            Include the records in the markdown.
        timestamp : bool
            Add a timestamp in the markdown.
        filename : str (optional)
            The filename of the yaml file to create.
            If none is provided, no file is created.

        Returns
        -------
        dict
            The assembled dictionary of the registry.
        """

        _dict = dict( self.metadata )
        _dict["directory"] = self.directory
        if timestamp:
            _dict["timestamp"] = datetime.now().strftime( "%Y-%m-%d %H:%M:%S" )

        if include_records:
            records = [ file.FileRecord( self, id = id ) for id in self.index.id ]
            records = { record.relpath[3:] : record.to_yaml() for record in records }
            _dict[ "records" ] = records

        if filename is not None:
            utils.save_yamlfile( filename, _dict )

        return _dict

    def to_markdown( self, include_records : bool = True, timestamp : bool = False, filename : str = None ):
        """
        Convert the metadata to a markdown representation.

        Parameters
        ----------
        include_records : bool
            Include the records in the markdown.
        timestamp : bool
            Add a timestamp in the markdown.
        filename : str (optional)
            The filename of the markdown file to create.
            If none is provided, no file is created.

        Returns
        -------
        str
            The markdown representation of the registry.
        """
        # add basic information and timestamp of manifest creation
        text = f"# {self.directory}\n\n"
        if timestamp: 
            text += f"{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n"
        
        # add registry's own comments
        text += "## Registry comments\n\n"
        for timestamp in self.comments:
            comment, user = list( self.comments[timestamp].values() )
            text += f"{settings.comment_format( comment, user, timestamp)}\n\n"

        # add all flags and flag groups
        text += "## Registered flags\n\n"
        for i in sorted( self.flags ):
            text += f"- {i}\n"
        text += "\n"

        text += "### Flag groups\n\n"
        text += "| Group | Flags |\n"
        text += "|------|------|\n"
        for label, flags in self.groups.items():
            text += f"| {label} | {', '.join(flags)} |\n"

        if include_records:
            text += "\n"
            text += "## Records\n\n"
            if len( self.index.id ) == 0:
                text += "No records found."
            else:
                for record in self.index.id:
                    record = file.FileRecord( self, id = record )
                    text += record.to_markdown( comments_header = False )

        if filename is not None:
            with open( filename, "w" ) as f:
                f.write( text )

        return text

    def base_has_registry( self ):
        """
        Checks if the current directory already has a registry.
        """
        return os.path.exists( os.path.join( self.directory, settings.registry_dir ) )


    @property
    def groups( self ) -> dict:
        """
        Get the defined flag-groups.
        """
        return self.metadata["groups"]

    def _find_registry( self ):
        """
        Finds the local registry associated with the given directory.
        This will parse the directory hierarchy upwards until it finds a registry.
        If none are found it will initialize a new registry in the given directory.
        """
        self.registry_dir = utils.find_registry( self.directory )

        if self.registry_dir is None:
            logger.info( "No local registry found. Initializing a new registry." )
            self.init()
            self.registry_dir = os.path.join( self.directory, settings.registry_dir )
        
        
    def _load_registry( self ):
        """
        Loads the registry data from the indexfile and metafile
        """
        self.indexfile = utils.get_indexfile( self.registry_dir )
        self.metafile = utils.get_metafile( self.registry_dir )

        self.index = utils.load_indexfile( self.indexfile )
        self.metadata = utils.load_yamlfile( self.metafile )

    def __repr__( self ):
        return f"{self.__class__.__name__}(directory = {self.directory}, registry_in = {os.path.dirname( os.path.dirname( self.registry_dir ) ) })"