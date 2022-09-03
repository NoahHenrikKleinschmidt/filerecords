"""
The `records flag` command can be used to add flags to a specific file or the registry itself, and to define flag groups.

Usage
-----

    >>> records flag [-f <flags>] [-g <groupname> : <grouplabels>] <filename>

    where ``<filename>`` is the path to the file to comment. If left blank the flag is added to the registry itself.
    ``-f <flags>``, adds any number of flags. These can include defined flag group labels.
    ``-g <groupname> : <grouplabels>``, will define a flag group in the registry. 
    ``-f`` and ``-g`` can be provided at the same time. 
"""


def setup( parent ):
    """
    Set up the CLI
    """
    descr = "Add flags to files or the registry itself (can also be done with comment), and define flag groups (this command only)."
    parser = parent.add_parser( "flag", description = descr, help = descr )
    parser.add_argument( "filename", nargs = "?", help = "The file to comment. If left blank the comments are applied to the registry itself", default = None )
    parser.add_argument( "-f", "--flags", help = "Add flags.", nargs="+", default = None )
    parser.add_argument( "-g", "--group", help = "Add flag groups to the registry. Flag groups can be specified via '<name> : <flag1> <flag2>...' syntax. Note, this option specifies a single group. It can be supplied multiple times to specify multiple groups in one go.", nargs="+", action = "append", default = None )

    parser.set_defaults( func = flag )

def flag( args ):
    """
    The core function to add comments.
    """
    import filerecords.api as api
    import filerecords.cli.auxiliary as aux
    # import filerecords.api.utils as utils

    # logger = utils.log()
    reg = api.Registry( "." )

    # add any new groups to the registry.
    if args.group:
        aux._register_groups( reg, args.group )

    # this bit is (almost) identical to the comment function

    if args.flags:

    #    if len(args.flags) == 1: 
    #     args.flags = args.flags[0]

        if not args.filename:

            if args.flags:
                reg.add_flags( args.flags )
            reg.save()

        else:

            record = reg.get_record( args.filename )
            if record is None:
                reg.add( args.filename, flags = args.flags )
            else:
                reg.update( args.filename, flags = args.flags )