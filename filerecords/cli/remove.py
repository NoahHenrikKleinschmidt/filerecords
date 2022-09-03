"""
The `records rm` command can be used to remove a file or directory from the registry.
This command by default also performs file removal. 

Usage
-----

    >>> records rm [-k] <filename>

    where ``<filename>`` is the path to the file to remove from the registry. 
    The ``-k`` option can be specified to prevent the file from being removed itself. In this case
    the file will remain while its records are removed.
"""

def setup( parent ):
    """
    Set up the CLI
    """
    descr = "Remove files from the registry."
    parser = parent.add_parser( "rm", description = descr, help=descr )
    parser.add_argument( "filename", help = "The file to remove." )
    parser.add_argument( "-k", "--keep", help = "Keep the file itself and only remove the records. By default the file or directory itself is also removed.", action = "store_true", default = False )
    parser.set_defaults( func = remove )

def remove( args ):
    """
    The core function to remove entries from the registry.
    """
    import filerecords.api as api
    # from filerecords.api.utils import log
        
    # logger = log()
    reg = api.Registry( "." )
    reg.remove( args.filename, keep_file = args.keep )
    # logger.info( f"Removed {args.filename} from the registry." )
    print( f"Removed {args.filename} from the registry." )