"""
The `records mv` command can be used to move / rename a file or directory in the registry.
This command by default also performs file moving. 

Usage
-----

    >>> records mv [-k] <filename>

    where ``<filename>`` is the path to the file to move / rename in the registry. 
    The ``-k`` option can be specified to prevent the file from being moved itself. In this case
    the file will remain unchanged while its records are adjusted.
"""


def setup( parent ):
    """
    Set up the CLI
    """
    descr = "Move / rename files or directories in the registry."
    parser = parent.add_parser( "mv", description = descr, help=descr )
    parser.add_argument( "current", help = "The file to move / rename." )
    parser.add_argument( "new", help = "The file's new path." )
    parser.add_argument( "-k", "--keep", help = "Keep the file itself and only adjust the records. By default the file or directory itself is also moved.", action = "store_true", default = False )
    parser.set_defaults( func = move )

def move( args ):
    """
    The core function to move / rename entries in the registry.
    """
    import filerecords.api as api
    # import filerecords.api.utils as utils

    # logger = utils.log()
    reg = api.Registry( "." )
    reg.move( args.current, args.new, keep_file = args.keep )
