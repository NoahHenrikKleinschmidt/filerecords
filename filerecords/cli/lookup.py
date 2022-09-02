"""
The `records lookup` command can be used look up the latest comment of a given file.

Usage
-----

    >>> records lookup <filename>

    where ``<filename>`` is the file of interest.
    
"""



def setup( parent ):
    """
    Set up the CLI
    """
    descr = "Look up a file's latest comment."
    parser = parent.add_parser( "lookup", description = descr, help = descr )
    parser.add_argument( "filename", nargs = "?", help = "The file to look up. If left blank the latest registry comment is looked up.", default = None )
    parser.set_defaults( func = lookup )

def lookup( args ):
    """
    The core function to look up the latest comment.
    """
    import filerecords.api as api
    import filerecords.api.utils as utils
    
    logger = utils.log()
    reg = api.Registry( "." )

    if not args.filename:

        last = reg.lookup_last()
        name = f"{reg.directory} (registry)"

    else:

        record = reg.get_record( args.filename )
        last = record.lookup_last() if record is not None else None
        name = f"{args.filename} ({', '.join(record.flags)})" if record is not None else args.filename

    if last:
        
        timestamp = list( last.keys() )[0]
        logger.debug( f"{last[timestamp]=}" )

        comment = last[timestamp]["comment"]
        user = last[timestamp]["user"]
        last = f"""{name}\n{comment}  |  {user} @ {timestamp.strftime("%Y-%m-%d %H:%M:%S")}"""
        print( last )