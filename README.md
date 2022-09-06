
![](docs/source/logo_black.png)

[![CodeFactor](https://www.codefactor.io/repository/github/noahhenrikkleinschmidt/filerecords/badge)](https://www.codefactor.io/repository/github/noahhenrikkleinschmidt/filerecords)

`filerecords` is a python command line tool to better keep track of files and directories. It works similar to GIT but instead of keeping track of the actual file contents it keeps a registry of comments and flags. This allows users to comment their files and directories to add more detailed descriptions than just a good file name or directory name. 


## Example and why to use records...


Assume we have a large project directory containing various data directories, a scripts directory with subfolders, and directories for the results of analyses. Maybe something like this below:

```
├─── base_directory
      ├─── data
      ├─── raw
         ├─── ...
      ├─── normalised
         ├─── ...
      ├─── QC
         ├─── ...
      ├─── gencode
         ├─── ...
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
```

If we name our files and directories properly we will ideally know everything about the contents just from looking at the filenames.
However, what could be the purpose of the "reports" directory within results? Or why did we develop _my\_custom\_package_ again? And what files are inside the "archive" - are they important or is it more of a dump for stuff we don't need (anymore) but didn't want to delete? 

We can probably answer most of these questions instantly while actively working on the project, but what if we went on holiday or have moved on to the next project and now need to look something up, maybe months later?

That is where `filerecords` can help out. It allows versatile on-the-run commenting of files and directories and stores all metadata in a central registry (which should be located in the project's base directory - but separate sub-registries can be made of course...)


Let us see how it works. We will now go through a possible use of commenting for our project.

In order to be able to use records we must initialize a new registry.
We can use `records init` to do so. At this point we can also add comments to the base directory (i.e. our project as a whole). Perhaps
our project is about analysing gene set enrichments from some RNA-seq data, so we add a comment (`-c` option) to the project as well.

```
records init -c "the GSEA project from August 2022"
```

Now that our registry is initialized we can use `records comment` and `records flag` to add files / directories to the registry.

To start of we declare that the "archive" is a dump for stuff we don't need anymore but didn't want to delete.

```
records comment archive/ -f archive dump -c "Only add .tar.gz in here! the archive is for unneeded directories or scripts from experiments that did not go anywhere and serves as a 'cold storage'." 
```

With the above command we added a description about what our "archive" directory means and how we want to add contents to it. 
In addition to the comments which is a free text, we added 2 flags (`-f` option). These flags are the "shorthand" version of the comment and can be specified on-the-run as well. They are searchable in the registry, so they are handy to find conceptually similar files and directories.


Perhaps we figured that the "only add .tar.gz" part in the comment is so important that we might want to also add a flag for that. We can do so easily with either the `comment` command again or using the `flag` command.

```
records flag archive/ -f compress_only
```

Now we wish to record that all of the analyses pipelines are inside the _scripts/workflows/_ directory.

```
records comment scripts/workflows/ -f workflow analysis main pipeline -c "these are *all* the main analyses workflows from pre-processing to results evaluation"
```

And now we remember that one of our preprocessing steps
is automated by a package we wrote ourselves (that's why we wrote _my\_custom\_package_ :​bulb:). So we add this comment to the workflows as well and also add a comment about _my\_custom\_package_ as well.

```
cd scripts

records comment workflows/ -c "this requires that my_custom_package is installed! Should be handled if the environment from the scripts/env/ is properly set up."

records comment dev/my_custom_package -f preprocessing -c "this package is required to automate step X in the preprocessing. It should be installed in the environment by default."
```

Since we mentioned so much about the "environment" in 
the above comments, perhaps we also add a comment about that.

```
records comment env/ -f environment main -c "the conda environment in which this project is run."
```

Now that we have added some comments we can rest knowing that we have noted everything down we need to know. We can look up our metadata in a number of ways now.

For once we can `list` all entries for which we have records using

```
records list
```

this will tell us what files / directories within the project have records associated with them. If we are, for instance, only interested in files in the current working directory that are flagged as _main_ we can instead use

```
records ls -f main
```

Listing files may not be the most interesting. We care more about the comments associated with them. We can quickly check the latest comment of a file using `lookup` or read all records using `read`. So if we forgot why we have _my\_custom\_package_ we can do:

```
records read my_custom_package/
```

We shall leave this example here. Below you can find a complete list of the commands available. 

## Full CLI

This is a brief listing of all commands. Use their `--help` pages for all details on their use. 

To create a new registry within a directory use:

```
records init 
```

To add a comment about a file or directory use:
This will add *new* comments to file entries while preserving the old ones.

```
records comment the_file -m "the message" -f flag1 flag2 ...
```

To remove a file or directory from the registry use:
(by default this will also remove the file in the filesystem!)

```
records rm the_file
```

To move a file or directory while keeping the records use:
(by default this will also move the file in the filesystem!)

```
records mv the_current_path the_new_path
```

To remove/undo the last comment from a file or directory use:

```
records undo the_file
```

This also works for flags:

```
records undo the_file -f the_flag_to_remove 
```

To get a file's records use:

```
records lookup the_file
```

this will print the latest comment to the terminal.

To read the entire records of a file use:

```
record read the_file
```

To search for files and directories based on flags or regex patterns use:

```
records list -f flag1 -e the_regex_pattern
```

This can be restricted to files in the current working directory by:

```
records ls 
```

instead of the full `list` command.

To only add a flag (but no comment) to a file use:

```
records flag the_file -f flag1 
```

> This could also be achieved using
>
> ```
> records comment the_file -f flag1 
> ```

To define new flag groups to the registry use:

```
records flag -g group1 : flag1 flag2 -g group2 : flag3 flag4
```

To remove all file records from the registry use:

```
records clear
```

To completely remove a registry use:

```
records destroy
```

To export the registry either in YAML or markdown format use:

```
records export yaml|md|both
```