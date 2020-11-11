# MakeFile-Creator

MakeFile-Creator is an utility for managing makefiles in C/C++ projects.

# Getting started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

`Python >= 3.6`

### Installing

Install the package from Python Package Index using the command:

`pip3 install makefile-creator`

### Configuration

`cd /your/project/path`

You have to create a configuration file. For the first time it's good to let 
MakeFile-Creator to automatically generate configuration for you.

`python3 -m makefile-creator`

If there is no `mfc.config.json` file in current working directory, then a new one
will be created.

File content should be something like this:

```
{
  "TARGET": "my_project",
  "CC": "g++",
  "C_FLAGS": [
    "-Wall",
    "-c"
  ],
  "LD_FLAGS": [],
  "EXTENSIONS": [
    "c",
    "cc",
    "cpp"
  ],
  "IGNORE_PATHS": [],
  "CUSTOM_TARGETS": {},
  "VERBOSE": false,
  "RM": "rm -v",
  "CLEAN": false
}
```

Meaning:
* _**`target`:**_ you project name.
* **_`cc`:_** compiler command (`"g++"`, by default).
* _**`c_flags`:**_ list of compiler flags.
* _**`ld_flags`:**_ list of linker flags.
* **_`extensions`:_** source files extensions list (`["cpp"]`, by default).
* **_`ignore_paths`:_** list of paths to be ignored, for example you can put here all
directories you do not want MakeFile-Creator to scan.
* **_`custom_targets`:_** custom targets for `make`, in the following format:

```
"custom_targets": {
    "target_name": "command",
    "other_target": "other_command",
    ...
}"
````

* **_`verbose`:_** `true` if you want to print entire source tree while scanning.
* **_`rm`:_** command to use for **_`make clean`_** (`rm -v`, by default).
* **_`clean`:_** `true` if you want to clean redundant files (.d files, for example).

Run the script:

`python3 -m makefile_creator`

Now MakeFile-Creator will generate makefiles.

## Authors

* **Romulus-Emanuel Ruja <<romulus-emanuel.ruja@tutanota.com>>**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.