"""
The `records undo` command can be used to remove a file or directory's last added comment.

Usage
-----

    >>> records undo [-f <flags>] <filename>

    where ``<filename>`` is the path to the file whose last comment to remove. 
    If left blank the comment is removed from the registry itself.
    ``-f <flags>``, removes any number of flags. These can include defined flag group labels.

    Note
    ----
    When flags are specified, then only the flags are removed while the comments are left untouched.
"""


def setup( parent ):
    """
    Set up the CLI
    """
    descr = "Remove flags or the latest comment from a file or directory."
    parser = parent.add_parser( "undo", description = descr, help=descr )
    parser.add_argument( "filename", nargs = "?", help = "The file whose metadata to undo. If left blank the actions are applied to the registry itself", default = None )
    parser.add_argument( "-f", "--flags", help = "Any flags to remove.", nargs="+", default = None )
    parser.set_defaults( func = undo )

def undo( args ):
    """
    The core function to undo comments or files.
    """
    import filerecords.api as api
    import filerecords.api.utils as utils

    logger = utils.log()

    reg = api.Registry( "." )
    
    if args.flags and len(args.flags) == 1:
        args.flags = args.flags[0]
    
    if not args.filename:

        if args.flags:
            reg.remove_flags( args.flags )
        else:
            reg.undo_comment()

        reg.save()

    else:

        record = reg.get_record( args.filename )
        if record is None:
            logger.error( f"No record for {args.filename}" )
            return
        
        if args.flags:
            record.remove_flags( args.flags )
        else:
            record.undo_comment()
        
        logger.info( f"Updated {args.filename} in the registry." )
        record.save()