"""
The `records screen` command can be used to check if all recorded files still exist at their recorded locations. 

Usage
-----

    >>> records screen

"""

def setup( parent ):
    """
    Set up the CLI
    """
    descr = "Screen the recorded files at their recorded locations."
    parser = parent.add_parser( "screen", description = descr, help=descr )
    parser.add_argument( "-f", "--flag", help = "The flag search for. Note, this may only be a single flag! To search for multiple flags at a time, define a flag group first and then search for it's label using 'group:your_group'.", default = None )
    parser.add_argument( "-e", "--pattern", help = "The regular expression to search for.", default = None )
    parser.set_defaults( func = screen )

def screen( args ):
    """
    The core function to screen recorded files.
    """
    import filerecords.api as api
    import os
    
    # from filerecords.api.utils import log
        
    # logger = log()
    reg = api.Registry( "." )

    print( "Screening..." )
    for record in reg.search( pattern = args.pattern, flag = args.flag ):
        if not os.path.exists( record.filename ):
            print( f"File {record.filename} does not exist!" )
    print( "Screening finished." )