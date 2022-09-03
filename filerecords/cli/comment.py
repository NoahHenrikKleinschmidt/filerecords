"""
The `records comment` command can be used to add a comment to a specific file or the registry itself.

Usage
-----

    >>> records comment [-c <comment>] [-f <flags>] <filename>

    where ``<filename>`` is the path to the file to comment. If left blank the comment is added to the registry itself.
    ``-c <comment>``, adds a comment or description message.  ``-f <flags>``, adds any number of flags. These can include defined flag group labels.
"""


def setup( parent ):
    """
    Set up the CLI
    """
    descr = "Add comments to files or the registry itself."
    parser = parent.add_parser( "comment", description = descr, help = descr )
    parser.add_argument( "filename", nargs = "?", help = "The file to comment. If left blank the comments are applied to the registry itself", default = None )
    parser.add_argument( "-c", "--comment", help = "Add a comment or description.", default = None )
    parser.add_argument( "-f", "--flags", help = "Add flags.", nargs="+", default = None )
    parser.set_defaults( func = comment )

def comment( args ):
    """
    The core function to add comments.
    """
    import filerecords.api as api
    # from filerecords.api.utils import log

    # logger = log()

    reg = api.Registry( "." )

    # # the add and update functions are expecting to find a string
    # # if noly one value is present...
    # if args.flags and len(args.flags) == 1:
    #     args.flags = args.flags[0]

    if not args.filename:

        if args.comment:
            reg.add_comment( args.comment )

        if args.flags:
            reg.add_flags( args.flags )

        reg.save()
        
    else:

        record = reg.get_record( args.filename )
        if record is None:

            reg.add( args.filename, comment = args.comment, flags = args.flags )
            # logger.info( f"Added {args.filename} to the registry." )
            print( f"Added {args.filename} to the registry." )

        else:

            reg.update( args.filename, comment = args.comment, flags = args.flags )
            # logger.info( f"Updated {args.filename}'s records." )
            print( f"Updated {args.filename}'s records." )