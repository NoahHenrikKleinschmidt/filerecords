"""
This is the base class for the `filerecords` API classes.

.. note::

    This is not intended to be used directly.
    
"""

from datetime import datetime
import os

import filerecords.api.utils as utils

logger = utils.log()

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

    def lookup_last( self ) -> dict:
        """
        Get the last comment.

        Returns
        -------
        dict
            The last comment dictionary with timestamp as key, 
            user and comment as values.
        """
        if len( self.metadata["comments"] ) == 0:
            logger.info("No comments found.")
            return None

        last = sorted( list( self.comments.keys() ) )[-1]
        return { last : self.metadata["comments"].get( last ) }

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

    def remove_flags( self, flag : (str or list) ):
        """
        Remove one or more flags from the registry.

        Note
        ----
        This will not automatically save the metadata,
        use the save() method to do so.

        Parameters
        ----------
        flag : str or list
            The flag(s) to remove.
        """
        if not isinstance( flag, list ):
            flag = [ flag ]
        logger.debug( "Removing flags: {}".format( flag ) )

        for f in flag:
            self.metadata["flags"].remove( f )

    def add_flags( self, flag : (str or list) ):
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

        self.metadata["flags"] += flag
        logger.debug( "(before set) metadata['flags']: {}".format( self.metadata["flags"] ) )

        self.metadata["flags"] = list( set( self.metadata["flags"] ) )
        logger.debug( "(after set) metadata['flags']: {}".format( self.metadata["flags"] ) )


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
