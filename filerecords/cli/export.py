"""
The `records export` command can be used export a YAML or markdown summary (manifest) of all 
records in the registry.

Usage:

    >>> records export <yaml|md|both> -f <filename>

    where either ``yaml``, ``md``, or ``both`` can be specified to export the records to a yaml or markdown file, or both.
    The ``-f`` option can be used to specify a specific filename to export to. 
    Note, `.yaml` and `.md` are added to the filename automatically.
"""

def setup( parent ):
    """
    Set up the CLI
    """
    descr = "Export the registry to a file manifest."
    parser = parent.add_parser( "export", description = descr, help = descr )
    parser.add_argument( "format", help = "The export format, which can be either yaml, markdown, or both.", choices = ["md", "yaml", "both"] )
    parser.add_argument( "-f", "--filename", help = "The filename to export to. If not specified, a default 'registry-{timestamp}' file will be created.", default = None )
    parser.set_defaults( func = export )


def export( args ): 
    """
    The core function to export the registry.
    """
    import filerecords.api as api
    import filerecords.api.settings as settings
    from datetime import datetime
    # from filerecords.api.utils import log
 
    # logger = log()
    reg = api.Registry( "." )

    if args.filename is None:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        args.filename = f"{settings.registry_export_name}-{timestamp}"

    if args.format == "yaml" or args.format == "both":
        reg.to_yaml( timestamp = True, filename = args.filename + ".yaml" )

    if args.format == "md" or args.format == "both":
        reg.to_markdown( timestamp = True, filename = args.filename + ".md" )

    # logger.info( f"Exported registry to {args.filename}" )
    print( f"Exported registry to {args.filename}" )