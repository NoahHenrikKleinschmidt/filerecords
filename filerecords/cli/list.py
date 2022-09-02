"""
The `records list` command can be used to list recorded files within the registry.
By default this will list all recorded files in the registry.  The results can be restricted
using the ``-f`` and ``-e`` flags.

Usage
-----

    >>> records list [-f <flag>] [-e <pattern>]

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
    descr = "List file records."
    parser = parent.add_parser( "list", description = descr, help = descr )
    parser.add_argument( "-f", "--flag", help = "The flag search for. Note, this may only be a single flag! To search for multiple flags at a time, define a flag group first and then search for it's label using 'group:your_group'.", default = None )
    parser.add_argument( "-e", "--pattern", help = "The regular expression to search for.", default = None )
    parser.set_defaults( func = search )

def search( args ):
    """
    The core function to search for entries.
    """
    import filerecords.api as api
    import filerecords.api.utils as utils

    logger = utils.log()
    reg = api.Registry( "." )

    records = reg.search( args.pattern, flag = args.flag )

    if len( records ) == 0:
        logger.info( "No records found." )
        return
    
    output = ""
    for record in records:
        output += f"{record.relpath[3:]}  ({', '.join(record.flags)})\n"

    print( output.rstrip() )