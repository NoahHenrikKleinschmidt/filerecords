The main filerecords CLI
========================

This is the main command line interface for `filerecords`.

Usage
-----

`filerecords` supports as main command either its full name 

.. code-block:: bash

   filerecords [OPTIONS] COMMAND [ARGS]...

or the abbreviated version

.. code-block:: bash

   records [OPTIONS] COMMAND [ARGS]...


On principle, (almost) any command can be used either on a specific file by specifying a filename or on the registry as a whole (by leaving the filename blank).
Hence, to look up the last comment:

   >>> records lookup my_datafile.tsv

will yield the last comment of the file "my_datafile.tsv". On the other hand,

   >>> records lookup

will yield the last comment that was added to the registry as a whole.

The "registry as a whole" or "registry itself" means that the comments and flags applied to the registry directly and not to any specific file.
These should be comments about the project itself. So, for example, if we want to add a comment about the project, you can do

   >>> records comment -c "This is a comment about the project"

whereas 

   >>> records comment -c "This is a comment about my data" my_datafile.tsv

will add a comment about the file "my_datafile.tsv" specifically.


Initializing a new registry
---------------------------

To initialize a new registry, run:

   >>> records init

This will create a new hidden directory `.registry` in the current working directory (which is the heart of the registry).
It is possible to also add comments and flags to the registry when initializing it. Also, flag groups can be added to the registry at this point.

.. code-block:: bash

   usage: records init [-h] [-c COMMENT] [-f FLAGS [FLAGS ...]] [-g GROUP [GROUP ...]] [-i]

   Initialize a new registry within the current directory.

   optional arguments:
   -h, --help            show this help message and exit
   -c COMMENT, --comment COMMENT
                           Add a comment or description to the registry
   -f FLAGS [FLAGS ...], --flags FLAGS [FLAGS ...]
                           Add flags.
   -g GROUP [GROUP ...], --group GROUP [GROUP ...]
                           Add flag groups to the registry. Flag groups can be specified via '<name> : <flag1> <flag2>...' syntax. Note, this option specifies a
                           single group. It can be supplied multiple times to specify multiple groups in one go.
   -i, --gitignore       Add the registry to .gitignore


.. note::

   Any subdirectory will automatically reference to this registry. However, new registries can be initialized. 
   On principle, a record is added to the closest upstream registry, relative to the current working directory.
   Different registries to *not* communicate with each other.

Adding records
--------------

To add new records (or update existing ones) use:

   >>> records comment <filename> -c <some comment> -f <some flag(s)>

The basic way add records is by using the `comment` command. This command will add a new record to the registry, or update an existing one. When updating,
new flags and comments are added to the file's records while preserving any existing ones.

.. code-block:: bash

   usage: records comment [-h] [-c COMMENT] [-f FLAGS [FLAGS ...]] [filename]

   Add comments to files or the registry itself.

   positional arguments:
   filename              The file to comment. If left blank the comments are applied to the registry itself

   optional arguments:
   -h, --help            show this help message and exit
   -c COMMENT, --comment COMMENT
                           Add a comment or description.
   -f FLAGS [FLAGS ...], --flags FLAGS [FLAGS ...]
                           Add flags.
                           

Flags can also be added using the `flag` comand instead. 

   >>> records flag <filename> -f <some flag(s)>

.. warning::

   Because `-f` (or `--flags`) accepts any number of flags as argument, they must come *after* the filename (or before the comment option `-c` in case of the `comment` command), otherwise the filename is considered one of the flags!

      >>> records comment -c <some comment> -f <some flag(s)> <filename> # WRONG

      >>> records comment <filename> -c <some comment> -f <some flag(s)> # CORRECT

      >>> records comment -f <some flag(s)> -c <some comment> <filename> # CORRECT

      >>> records flag -f <some flag(s)> <filename> # WRONG

      >>> records flag <filename> -f <some flag(s)> # CORRECT

.. code-block:: bash

   usage: records flag [-h] [-f FLAGS [FLAGS ...]] [-g GROUP [GROUP ...]] [filename]

   Add flags to files or the registry itself (can also be done with comment), and define flag groups (this command only).

   positional arguments:
   filename              The file to comment. If left blank the comments are applied to the registry itself

   optional arguments:
   -h, --help            show this help message and exit
   -f FLAGS [FLAGS ...], --flags FLAGS [FLAGS ...]
                           Add flags.
   -g GROUP [GROUP ...], --group GROUP [GROUP ...]
                           Add flag groups to the registry. Flag groups can be specified via '<name> : <flag1> <flag2>...' syntax. Note, this option specifies a
                           single group. It can be supplied multiple times to specify multiple groups in one go.


Flag groups
-----------

Flag groups are a way to group flags together. This is useful when you want to add multiple flags to a file, but don't want to type them all out.
For example, if you have a flag group called "my_group" that contains the flags "flag1" and "flag2", you can add them to a file by doing

   >>> records comment <filename> -f my_group

However, for this to work, "my_group" needs to be defined first. This is the second job of the `flag` command.

   >>> records flag -g my_group : flag1 flag2

This will create a new flag group called "my_group" that contains the flags "flag1" and "flag2". Note that the flag group name must be separated from the flags by a colon (`:`).
The group will contain the specified flags as well as an automatically generated flag called `group:my_group`. This group-label flag can later be used to easily find all records associated with this flag group.


Editing records
---------------

`filerecords` offers the `undo` command to either undo the last comment of a file or to remove a specific flag.

   >>> records undo <filename>  # undo the last comment

   >>> records undo <filename> -f <flag> # remove a specific flag 

.. code-block:: bash

   usage: records undo [-h] [-f FLAGS [FLAGS ...]] [filename]

   Remove flags or the latest comment from a file or directory.

   positional arguments:
   filename              The file whose metadata to undo. If left blank the actions are applied to the registry itself

   optional arguments:
   -h, --help            show this help message and exit
   -f FLAGS [FLAGS ...], --flags FLAGS [FLAGS ...]
                           Any flags to remove.


If a file needs to be moved to a different location, `filerecords` offers its own `mv` command that will move the file and adjust its records accordingly.

   >>> records mv <old_filename> <new_filename>

.. code-block:: bash

   usage: records mv [-h] [-k] current new

   Move / rename files or directories in the registry.

   positional arguments:
   current     The file to move / rename.
   new         The file\'s new path.

   optional arguments:
   -h, --help  show this help message and exit
   -k, --keep  Keep the file itself and only adjust the records. By default the file or directory itself is also moved.

Note that the `mv` command will also move the file itself. If you only want to adjust the records, use the `-k` option.
This is useful when a file has already been moved and now the records only need adjusting. 

   >>> records mv -k <old_filename> <new_filename> # will not touch the files themselves. Only the records will be adjusted.


On the other hand, if a file should be removed from the records, use `rm` command. 
This will by default also remove the file itself but offers the `-k` option to leave the file untouched but only remove its records.

   >>> records rm <filename> # will remove the file and its records

   >>> records rm -k <filename> # will only remove the records 

.. code-block:: bash

   usage: records rm [-h] [-k] filename

   Remove files from the registry.

   positional arguments:
   filename    The file to remove.

   optional arguments:
   -h, --help  show this help message and exit
   -k, --keep  Keep the file itself and only remove the records. By default the file or directory itself is also removed.


Accessing records
-----------------

To list all records in the registry, use:

   >>> records list

Specific files can be further filtered by using either the `-f` (`--flag`) option or the `-e` (`--pattern`) options.
The first allows to restrict the results to entries flagged with *one specific flag* - to search for multiple flags, make a flag group first (see above).
The second allows to match filenames based on a regular expression. 

   >>> records list -f <flag> # list all files flagged with <flag>

   >>> records list -e <pattern> # list all files matching <pattern>

   >>> records list -f <flag> -e <pattern> # list all files matching <pattern> AND flagged with <flag>

.. code-block:: bash

   usage: records list [-h] [-f FLAG] [-e PATTERN]

   List file records.

   optional arguments:
   -h, --help            show this help message and exit
   -f FLAG, --flag FLAG  The flag search for. Note, this may only be a single flag! To search for multiple flags at a time, define a flag group first and then
                           search for it\'s label using 'group:your_group'.
   -e PATTERN, --pattern PATTERN
                           The regular expression to search for.

To restrict the search to files found in the current working directory, use `ls` instead of `list`. 

   >>> records ls

will list all files from the current working directory for which records are available. This command supports the same filtering as `list`.

Reading records
---------------

`filerecords` offers two ways to quickly read records from command line. 
The first is `lookup` which will return the last added comment for a file.

   >>> records lookup <filename>

The second is `read` which will return a markdown representation of the file's entire records entry.

   >>> records read <filename>

There are no further options for either of these commands. 
But (just as a reminder) they both work on the registry itself as well by leaving the filename blank.

.. code-block:: bash

   usage: records lookup [-h] [filename]

   Lookup the last comment for a file or the registry itself.

   positional arguments:
   filename              The file to lookup. If left blank the registry itself is looked up.

   optional arguments:
   -h, --help            show this help message and exit

.. code-block:: bash

   usage: records read [-h] [filename]

   Read the records for a file or the registry itself.

   positional arguments:
   filename              The file to read. If left blank the registry itself is read.

   optional arguments:
   -h, --help            show this help message and exit

Exporting records
-----------------

`filerecords` offers the `export` command to export the entire registry to a YAML or markdown file.

   >>> records export md <filename> # export to markdown

   >>> records export yaml <filename> # export to YAML

.. code-block:: bash

   usage: records export [-h] [-f FILENAME] {md,yaml,both}

   Export the registry to a file manifest.

   positional arguments:
   {md,yaml,both}        The export format, which can be either yaml, markdown, or both.

   optional arguments:
   -h, --help            show this help message and exit
   -f FILENAME, --filename FILENAME
                           The filename to export to. If not specified, a default 'registry-{timestamp}' file will be created.

Destroying the registry
-----------------------

If the records are for some reason no longer needed, a registry can be deleted using the `destroy` command.
   
   >>> records destroy

.. code-block:: bash

   usage: records destroy [-h] [-e {yaml,md,both}] [-y]

   Remove the registry.

   optional arguments:
   -h, --help            show this help message and exit
   -e {yaml,md,both}, --export {yaml,md,both}
                           Export the registry before clearing. This will create a default 'registry-{timestamp}' file in either yaml or markdown format, or both, in
                           the current directory.
   -y                    Skip the confirmation prompt.

Alternatively, to keep a registry but remove all records from it, use the `clear` command.

   >>> records clear

.. code-block:: bash

   usage: records clear [-h] [-e {yaml,md,both}] [-y]

   Clear the registry.

   optional arguments:
   -h, --help            show this help message and exit
   -e {yaml,md,both}, --export {yaml,md,both}
                           Export the registry before clearing. This will create a default 'registry-{timestamp}' file in either yaml or markdown format, or both, in
                           the current directory.
   -y                    Skip the confirmation prompt.
