"""
The `records ls` command can be used to list files from the current directory for which records are available.
The results can be restricted using flags or regex patterns.

Usage
-----

    >>> records ls [-f <flag>] [-e <pattern>]

    where ``<flag>``, is a flag to search for and ``<pattern>``, is a regular expression to search for.
    Both ``<flag>`` and ``<pattern>`` *can* be specified at the same time. 

    Note
    ----
    The ``-f`` flag can only be used to search for a single flag. To search for multiple flags at a time, define a flag group first and then search for it's label using 'group:your_group'.

"""

def setup( parent ):
    """
    Set up the CLI
    """
    descr = "List files in the current directory that have records."
    parser = parent.add_parser( "ls", description = descr, help = descr )
    parser.add_argument( "-f", "--flag", help = "The flag search for. Note, this may only be a single flag! To search for multiple flags at a time, define a flag group first and then search for it's label using 'group:your_group'.", default = None )
    parser.add_argument( "-e", "--pattern", help = "The regular expression to search for.", default = None )
    parser.set_defaults( func = search )

def search( args ):
    """
    The core function to search for entries in the local directory.
    """
    
    import os, subprocess
    import filerecords.api as api
    import filerecords.api.utils as utils

    logger = utils.log()

    reg = api.Registry( "." )
        
    records = reg.search( args.pattern, flag = args.flag )

    # now restrict to those records that are stored in the current directory.
    # The current directory can either be specified by a path or be the base directory anway
    # in which case the relpath is empty.
    current = subprocess.check_output( "pwd", shell = True ).decode() # os.getcwd() keeps resolving symbolic links and without shell the same here...
    current = os.path.relpath( current.strip(), reg.registry_dir )
    logger.debug( f"{current=}")
    records = [ i for i in records if os.path.dirname( i.relpath ) == current ]

    if len( records ) == 0:
        logger.info( "No records found." )
        return

    output = ""
    for record in records:
        output += f"{record.relpath[3:]}  ({', '.join(record.flags)})\n"

    print( output.rstrip() )