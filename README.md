# filerecords

`filerecords` is a python command line tool to better keep track of files and directories. It works similarly to GIT in that it keeps hidden record files and users can add files to the records database, edit the entries, and more.

> Note <br>
> This is still in early development so the below section describes the planned usage.
## Usage

To create a new registry within a directory use:

```
records init 
```

To add a comment about a file or directory use:
This will add *new* comments to file entries while preserving the old ones.

```
records comment the_file -m "the message" -f flag1 flag2 ...
```

or 

```
records add the_file -m "the message" -f flag1 flag2 ...
```

To remove a file or directory from the registry use:

```
records remove the_file
```

To move a file or directory while keeping the records use:
(This will also perform the file moving operation `mv ...`)

```
records move the_current_path the_new_path
```

To remove/undo the last comment from a file or directory use:

```
records undo the_file
```

To read a file's records use:

```
records lookup the_file
```

or

```
records read the_file
```

To search for files and directories based on flags or regex patterns use:

```
records search -f flag1 -e the_regex_pattern
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
records export the_filename
```