"""
The `records read` command can be used read the entire records of a given file.

Usage
-----

    >>> records read <filename>

    where ``<filename>`` is the file of interest.
    
"""


def setup( parent ):
    """
    Set up the CLI
    """
    descr = "Read a file's records."
    parser = parent.add_parser( "read", description = descr, help = descr )
    parser.add_argument( "filename", nargs = "?", help = "The file whose records to read. If left blank the registry's own records are read.", default = None )
    parser.set_defaults( func = read )

def read( args ):
    """
    The core function to read records.
    """
    import subprocess
    import filerecords.api as api
    # import filerecords.api.utils as utils
    
    # logger = utils.log()
    reg = api.Registry( "." )

    if not args.filename:

        records = reg.to_markdown( include_records = False )

    else:

        record = reg.get_record( args.filename )
        records = record.to_markdown() if record is not None else None

    if records:
        
        # we try to show the markdown file 
        # with glow rather than printing it out blankly...
        try:
            
            # first check if we have glow installed
            out = subprocess.run( "glow -h", shell=True, stdout = subprocess.PIPE, stderr = subprocess.PIPE )
            if out.returncode != 0:
                raise RuntimeError

            # if we have it installed, call glow to render the markdown
            subprocess.run( f"echo '{records}' | glow -" , shell = True )
           
        # if we don't have glow, just print the markdown normally...
        except RuntimeError:

            print( records )