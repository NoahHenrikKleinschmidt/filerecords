"""
`FileRecord` is the basic object in which records within a registry are accessed.
This object can access and edit records for a specific file within the registry.

API Usage
=========

In the code API, a `Registry` will return a `FileRecord` object for a specific file when a record is accessed.
Each `FileRecord` requires a `Registry` object as parent to be initialized, and can then either access the registry
records via the internal id (happens when records are accessed via the `Registry` object) or via the file path which is then
searched for in the registry. It is suggested to access the records directly via the `Registry` object only.


Once a `FileRecord` has been obtained from the registry its comments and flags can be accessed using the `comments` and `flags` attributes.

.. code-block:: python

    from filerecords.api import Registry

    reg = Registry()

    # Access a record via the registry
    record = reg.get_record( "path/to/file" )

    # Access the comments
    comments = record.comments

    # Access the flags
    flags = record.flags
    

The `FileRecord` object can also be used to add new comments and flags to the record.

.. code-block:: python

    record.add_comment( "the new comment" )
    record.add_flag( ["flag1", "flag2"] )


When adding comments or flags it is important to save the record afterward. 
This will automatically also save the parent registry.

.. code-block:: python

    # Save the record (will also save the registry)
    record.save()


"""

from datetime import datetime
import uuid
import os

import filerecords.api.base as base
# import filerecords.api.registry as registry
import filerecords.api.utils as utils
import filerecords.api.settings as settings

logger = utils.log()

class FileRecord(base.BaseRecord):
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
    def __init__( self, registry, id : str = None, filename : str = None ):
        super().__init__()
        self.registry = registry
        self.filename = os.path.join( os.path.join( self.registry.directory, filename ) ) if filename else None


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

        logger.debug( f"filename: {self.filename}" )


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
            _flags = []
            for flag in flags:
                _flags += get_group_flags( flag )
            flags = _flags
            del _flags
        else:
            flags = get_group_flags( flags )
        super().add_flags( flags )
        self.registry.add_flags( flags )


    def to_markdown( self, comments_header : bool = True ):
        """
        Convert the metadata to a markdown representation.

        Parameters
        ----------
        comments_header : bool
            Add a header above the comments.
        """
        # the [3:] is to remove the ../ in the relpath beginning 
        # since every relpath starts at the base directory which is one
        # level above the registry directory.

        path = self.relpath[3:].replace( "_", "\_" )
        text = f"### {path}\n\n"

        if len( self.flags ) == 0:
            flags = "No flags"
        else:
            flags = '\n- '.join( self.flags )
        text += f"- {flags}\n\n"

        if comments_header:
            text += "#### Comments\n\n"

        if len( self.comments ) == 0:

            text += "No comments\n\n"

        else:

            for timestamp in self.comments:
                comment, user = list( self.comments[timestamp].values() )
                text += f"{settings.comment_format( comment, user, timestamp)}\n\n"
            
        return text

    def to_yaml( self, timestamp : bool = False, filename : str = None ):
        """
        Convert the source registry to a single YAML file.

        Parameters
        ----------
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
        _dict["filename"] = self.filename
        _dict["relpath"] = self.relpath[3:] # the [3:] is to remove the ../ in front of every relpath
        if timestamp:
            _dict["timestamp"] = datetime.now().strftime( "%Y-%m-%d %H:%M:%S" )

        if filename is not None:
            utils.save_yamlfile( filename, _dict )

        return _dict


    def _get_relpath(self):
        """
        Make the path of the recorded file relative to the registry.
        """

        # logger.debug( f"Registry index: {self.registry.index}" ) 
        ids = self.registry.index.id.astype(str)

        # logger.debug( f"ids={ids}" )
        logger.debug( f"str(self.id)={str(self.id)}" )

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

        # logger.debug( f"ids={ids}" )
        logger.debug( f"self.id={self.id}" )

        if str(self.id) in ids:

            logger.debug( self.registry.index )
            logger.debug( ids == str(self.id) )
            logger.debug( self.registry.index.loc[ids == str(self.id), "filename"].values[0] )

            return self.registry.index.loc[ids == str(self.id), "filename"].values[0]
        return os.path.basename( self.filename )

    def __repr__( self ):
        return f"{self.__class__.__name__}(id = {self.id}, filename = {self.filename})"