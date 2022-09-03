"""
The `records init` command can be used to initialize a new registry in the current directory.

Usage:

    >>> records init [-c <comment>] [-g <groupname> : <grouplabels>] [-g <groupname> : <grouplabels>]

    -c <comment> : Adds a comment or description to the registry that is initialized.
    -g <groupname> : Adds a label group to the registry. Label groups can be specified via '<name> : <label1> <label2>...' syntax. 
    Note, this option specifies a single group. It can be supplied multiple times to specify multiple groups in one go.

Flags and Flag groups
---------------------
Flags are used to label files and group them together. Flags are arbitrary labels so they can be specified on-the-run while commenting a file. Flag groups can be used to add multiple flags at a time to a file. 
Contrary to single flags, flag groups must be defined before they can be used. 

"""


def setup( parent ):
    """
    Set up the CLI
    """
    descr = "Initialize a new registry within the current directory."
    parser = parent.add_parser( "init", description = descr, help = descr )
    parser.add_argument( "-c", "--comment", help = "Add a comment or description to the registry", default = None )
    parser.add_argument( "-f", "--flags", help = "Add flags.", nargs="+", default = None)
    parser.add_argument( "-g", "--group", help = "Add flag groups to the registry. Flag groups can be specified via '<name> : <flag1> <flag2>...' syntax. Note, this option specifies a single group. It can be supplied multiple times to specify multiple groups in one go.", nargs="+", action = "append", default = None )
    parser.add_argument ("-i", "--gitignore", help = "Add the registry to .gitignore", action = "store_true" )
    parser.set_defaults( func = init )


def init( args ): 
    """
    The core function to initialize a new registry.
    """
    import filerecords.api as api
    import filerecords.cli.auxiliary as aux
    import filerecords.api.utils as utils

    logger = utils.log()

    reg = api.Registry( "." )

    if not reg._initialized and reg.base_has_registry():
        logger.info( "A registry already exists in this directory. Skipping initialization. Use the clear command to clear the registry." )
        return 

    # the init of the Registry should have
    # already taken care of this but just to be sure...
    elif not reg._initialized:
        reg.init()

    if args.comment:
        reg.add_comment( args.comment )
    
    if args.flags:
        reg.add_flags( args.flags )

    if args.group:
        aux._register_groups( reg, args.group )

    if args.gitignore:
        utils.add_registry_to_gitignore()

    reg.save()
