
.. image:: logo_black.png



This is `filerecords` - a command line tool to store metadata for files and directories to keep an easy overview over large projects.

Inspired by GIT, `filerecords` allows adding files or directories to a "registry" that stores comments and flags. These can be later used to 
search for files within a project. File entries or the entire registry itself can be easily exported to files for other purposes. 

Although the package is primarily designed for command line usage, there is a code-API that allows 
records generation, lookup, and editing directly from within python scripts as well.


Why filerecords?
----------------

I study bioinformatics and keep project directories that are slightly too large for my taste, so I feel they become convoluted and not as easy to navigate as I would like (especially when revisiting a project after it has been finished).
Hence, I usually keep some files in my project directories with descriptions about the important files and subdirectories, while moving unimportant / unneeded ones to "archive" directories.
This is all a bit cumbersome, however, so I wrote this package to help standardize and automate the process a little.

The basic idea behind it is that the user is able add comments and flags to their important directories or files as they are created, and then later search and read them - all directly from command line,
without needing to worry where to save comments or how to format them. 


Why use records - a short example
---------------------------------

Assume we have a large project directory containing various data directories, a scripts directory with subfolders, and directories for the results of analyses, and more. 
Maybe something like this below:


.. code-block:: 
   
   ├─── base_directory
      ├─── data
         ├─── raw
            ├─── ...
         ├─── normalised
            ├─── ...
         ├─── QC
            ├─── ...
         ├─── gencode
      ├─── scripts
         ├─── workflows
            ├─── ...
         ├─── env
         ├─── dev
            ├─── my_custom_package
            ├─── ...
      ├─── results
         ├─── gsea
            ├─── ...
         ├─── reports
            ├─── ...
      ├─── archive


If we name our files and directories properly we would ideally know everything about the contents just from looking at the filenames.
However, we are usually not that perfect, so what could be the purpose of the "reports" directory within results? 
Or why did we develop my\_custom\_package again? And what files are inside the "archive" - are they important or is it a dump for stuff we don't need anymore but didn't want to delete? 

We can probably answer most of these questions instantly while actively working on the project, but what if we went on holiday or have moved on to the next project and now need to look something up, maybe months later?

This is where `filerecords` can help out. It allows versatile on-the-run commenting of files and directories and stores all metadata in a central registry.

Let us see how it works. We will now go through a possible use of commenting for our project.

In order to be able to use records we first initialize a new registry.
We can use `records init` to do so. At this point we can also add comments to the base directory (i.e. our project as a whole). Perhaps
our project is about analysing gene set enrichments from some RNA-seq data, so we add this as a comment (`-c` option) to the project.

.. code-block:: bash

   records init -c "the GSEA project from August 2022"


.. note::

   On a technical note it is not required to first initialize a registry. This is because `filerecords` will search the filesystem
   for a an existing registry, and if none is found a new registry is automatically created in the current working directory. 
   However, to make sure that a project has only one dedicated registry it is advisable to first initialize it in the project's main directory -
   all records from subdirectories will automatically be recorded in that main registry, unless subdirectories got their own registris. On principle, 
   a record is always added to the nearest upstream registry.

Now that our registry is initialized we can use `records comment` and `records flag` to add files / directories to the registry.

To start we declare that the "archive" is a dump for stuff we don't need anymore but didn't want to delete.

.. code-block:: bash

   records comment archive/ -f archive dump -c "Only add .tar.gz in here! the archive is for unneeded directories or scripts from experiments that did not go anywhere and serves as a 'cold storage'." 


With the above command we added a description about what our "archive" directory means and how we want to add contents to it. 
In addition to the comment which is a free text, we added 2 flags (`-f` option). These flags are the "shorthand" version of the comment and can be specified on-the-run as well. 
They are searchable in the registry, so they are handy to find conceptually similar files and directories.


Perhaps we figured that the "only add .tar.gz" part in the comment is so important that we might want to also add a flag for that. 
We can do so easily with either the `comment` command again or using the `flag` command.


.. code-block:: bash

   records flag archive/ -f compress_only


Now the records for "archive" have been updated to also include the `compress_only` flag.


Next we may wish to record that all of the analyses pipelines are inside the `scripts/workflows/` directory.

.. code-block:: bash

   records comment scripts/workflows/ -f workflow analysis main pipeline -c "these are *all* the main analyses workflows from pre-processing to results evaluation"


And now we remember that one of our preprocessing steps
is automated by a package we wrote ourselves (that's why we wrote my\_custom\_package). 
So we add this comment to the workflows as well and also add a comment about my\_custom\_package as well.

.. code-block:: bash

   cd scripts

   records comment workflows/ -c "this requires that my_custom_package is installed! Should be handled if the environment from the scripts/env/ is properly set up."

   records comment dev/my_custom_package -f preprocessing -c "this package is required to automate step X in the preprocessing. It should be installed in the environment by default."

Now that we have added some comments we can rest knowing that we have recorded everything we need to know. 

Now it may be time to look up our records again. We can do so in a number of ways.

For once we can `list` all entries for which we have any records using


.. code-block:: bash

   records list


this will tell us what files / directories within the project have either comments or flags associated with them. 
If we are, for instance, only interested in files in the current working directory that are flagged as `main` we can instead use


.. code-block:: bash

   records ls -f main


`ls` is the local equivalent of the global `list`, and the `-f` option selects the `main` flag as search criteria.

Listing files may not be the most interesting. We care more about the comments associated with them. 
We can quickly check the latest comment of a file using `lookup` or read all records using `read`. So if we forgot why we have my\_custom\_package we can do:


.. code-block:: bash

   records read my_custom_package/


Finally, if we require a more complete overview over our records we can easily export the registry either to a YAML or markdown file. 
This can be done using the `export` command. For instance, if we want to export the registry to a markdown file we can do:

.. code-block:: bash

   records export md

This will generate a markdown manifest of all comments and flags from both 
the registry itself (base directory) as well as all sub-files and -directories recorded therein.

.. toctree::
   :maxdepth: 3
   :caption: Contents:

   filerecords.cli
   filerecords.api


Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
