"""
This is the main command line interface for `filerecords`. 
"""

import argparse
import filerecords.cli.init as init
import filerecords.cli.comment as comment
import filerecords.cli.flag as flag
import filerecords.cli.move as move
import filerecords.cli.remove as remove
import filerecords.cli.undo as undo
import filerecords.cli.list as list
import filerecords.cli.list_local as list_local
import filerecords.cli.lookup as lookup
import filerecords.cli.read as read 
import filerecords.cli.clear as clear
import filerecords.cli.export as export
import filerecords.cli.destroy as destroy


def setup():
    """
    Setup the command line interface.
    """
    descr = "filerecords – a command line tool for storing file metadata in a structured way."
    parser = argparse.ArgumentParser( description = descr )
    parser.add_argument("-v", "--version", action="store_true", help="Show version")
    subparsers = parser.add_subparsers(help="Available commands")

    # Add the sub-commands here.
    init.setup(subparsers)
    comment.setup(subparsers)
    flag.setup(subparsers)
    undo.setup(subparsers)
    lookup.setup(subparsers)
    read.setup(subparsers)
    move.setup(subparsers)
    remove.setup(subparsers)
    list.setup(subparsers)
    list_local.setup(subparsers)
    export.setup(subparsers)
    clear.setup(subparsers)
    destroy.setup(subparsers)
    

    args = parser.parse_args()

    if args.version:
        print("filerecords version 0.0.1")

    else:
        args.func( args )

if __name__ == "__main__":
    setup()