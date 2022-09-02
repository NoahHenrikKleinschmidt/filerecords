"""
The `records clear` command can be used clear all records of a registry.
This action is equivalent to destroying the old registry and creating a new one.

Usage:

    >>> records clear [-e <export_file>]

    To prevent loss of records, the records can be exported either to a yaml or a markdown file (or both) 
    before clearing. The ``-e`` option can be specified to export the records to a file. 
"""

def setup( parent ):
    """
    Set up the CLI
    """
    descr = "Clear the registry."
    parser = parent.add_parser( "clear", description = descr, help = descr )
    parser.add_argument( "-e", "--export", help = "Export the registry before clearing. This will create a default 'registry-{timestamp}' file in either yaml or markdown format, or both, in the current directory.", choices = ["yaml", "md", "both"] )
    parser.add_argument( "-y", help = "Skip the confirmation prompt.", action = "store_true" )
    parser.set_defaults( func = clear )


def clear( args ): 
    """
    The core function to clear the registry.
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

        confirmation = input( "This is a destructive action! Are you sure you wish to clear your records? [y|N]: ").lower()
        if not confirmation == "y":
            logger.info( "Aborting..." )
            return

    # remove the old registry
    shutil.rmtree( reg.registry_dir )

    # make a new registry
    reg.init()