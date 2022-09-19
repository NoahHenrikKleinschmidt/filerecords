
![](docs/source/logo_black.png)

[![CodeFactor](https://www.codefactor.io/repository/github/noahhenrikkleinschmidt/filerecords/badge)](https://www.codefactor.io/repository/github/noahhenrikkleinschmidt/filerecords)
[![Documentation Status](https://readthedocs.org/projects/filerecords/badge/?version=latest)](https://filerecords.readthedocs.io/en/latest/?badge=latest)

`filerecords` is a python command line tool to better keep track of files and directories for data science projects (or any kind of big directory structure). 
It works similar to GIT but instead of keeping track of the actual file contents it keeps a registry of comments and flags. This allows users to comment their important files and directories to add more detailed descriptions than just a good file name or directory name. 

![example](https://user-images.githubusercontent.com/89252165/188868989-3d9b0682-c455-4ff2-a36e-0113d7049c3a.gif)

## Short overview

This is a brief listing of all commands. More details on their use can be found in the [documentation on readthedocs](https://filerecords.readthedocs.io/en/latest/).

To create a new registry within a directory use:

```
records init 
```

To add a comment about a file or directory use:
This will add *new* comments to file entries while preserving the old ones.

```
records comment the_file -c "the comment" -f flag1 flag2 ...
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
