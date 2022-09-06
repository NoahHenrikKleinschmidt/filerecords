"""
These are the default settings that control filerecords behavior.
"""
import logging

# ----------------------------------------------------------------
#   General settings
# ----------------------------------------------------------------

log_level = logging.INFO
"""The default logging level"""

# ----------------------------------------------------------------
#   Formatting settings
# ----------------------------------------------------------------
comment_format = lambda comment, name, timestamp : f"{comment}  |  {name} @ {timestamp.strftime('%Y-%m-%d %H:%M:%S')}"
"""The default format in which comments shall be represented in markdown files. This must be a function accepting a `comment`, `name`, and `timestamp (datetime object)` argument and return a string."""

# ----------------------------------------------------------------
#   Basic files
# ----------------------------------------------------------------

registry_dir = ".registry"
"""The directory to store the registry in"""

indexfile = "INDEXFILE"
"""The name of the indexfile, which will map filenames (basenames) to unique identifiers within the registry."""

registry_metafile = "METAFILE"
"""The name of the file storing the registry's own metadata - i.e. registry comments and the associated flags and flag groups."""

registry_export_name = "registry"
"""The default name of exported registry file(s) in yaml or markdown format"""

# ----------------------------------------------------------------
#   File architecture
# ----------------------------------------------------------------

indexfile_header = "id\tfilename\trelpath\n"
"""The header of the indexfile"""

entryfile_template = {
                        "comments" : {},
                        "flags" : [],
                    }
"""The template for file record entries"""