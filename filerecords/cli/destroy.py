"""
The `records destroy` command can be used remove a registry entirely.

Usage:

    >>> records destroy [-e <export_file>]

    To prevent loss of records, the records can be exported either to a yaml or a markdown file (or both) 
    before removal. The ``-e`` option can be specified to export the records to a file. 
"""


def setup( parent ):
    """
    Set up the CLI
    """
    descr = "Remove the registry."
    parser = parent.add_parser( "destroy", description = descr, help = descr )
    parser.add_argument( "-e", "--export", help = "Export the registry before clearing. This will create a default 'registry-{timestamp}' file in either yaml or markdown format, or both, in the current directory.", choices = ["yaml", "md", "both"] )
    parser.add_argument( "-y", help = "Skip the confirmation prompt.", action = "store_true" )
    parser.set_defaults( func = destroy )


def destroy( args ): 
    """
    The core function to destroy a registry.

    Note
    ----
    This is virtually the same as clear() 
    but will not initialize a new registry again...
    """
    import shutil
    import filerecords.api as api
    import filerecords.api.settings as settings
    import filerecords.api.utils as utils
    from datetime import datetime

    logger = utils.log()

    reg = api.Registry( "." )

    if args.export:
        filename = f"{settings.registry_export_name}-{datetime.now()}"
        man = api.Manifest( reg )

        if args.export == "yaml" or args.export == "both":
            man.to_yaml( filename + ".yaml" )
        if args.export == "md" or args.export == "both":
            man.to_markdown( filename + ".md" )
    
    if not args.y:

        confirmation = input( "This is a destructive action! Are you sure you wish to destroy your records? [y|N]: ").lower()
        if not confirmation == "y":
            logger.info( "Aborting..." )
            return

    # remove the registry
    shutil.rmtree( reg.registry_dir )
    
    logger.info( f"Registry in {reg.directory} destroyed." )