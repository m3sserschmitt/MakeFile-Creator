# MakeFile-Creator

MakeFile-Creator is an utility for managing makefiles in C/C++ projects.

# Getting started

These instructions will get you a copy of the project up and running on your local machine.

### Prerequisites

`Python >= 3.6`

### Installing

Install the package from Python Package Index:

`pip3 install makefile-creator`

### Configuration

`cd /your/project/path`

You have to create a configuration file. For the first time it's good to let 
MakeFile-Creator to automatically generate configuration for you.

`python3 -m makefile_creator -config`

A new `mfc.config.json` file will be created in current working directory.

File content should be something like this:

```
{
  "TARGET": "my_project",
  "CC": "gcc",
  "LD": "gcc"
  "C_FLAGS": [
    "-c",
    "-Wall"
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
  "BUILD_DIRECTORY": "./build",
  "BIN_DIRECTORY": "./build/bin"
}
```

Meaning:
* _**`target`:**_ Project name.
* **_`cc`:_** Compiler command (`"gcc"`, by default).
* **_`ld`:_** Linker command (`"gcc"`, by default).
* _**`c_flags`:**_ List of compiler flags.
* _**`ld_flags`:**_ List of linker flags.
* _**`libs`:**_ Libs to be used to compile the project.
* _**`include_paths`**_ Paths to search for headers.
* **_`extensions`:_** Source files extensions list.
* **_`ignore_paths`:_** List of paths to be ignored, for example you can put here all
directories you do not want MakeFile-Creator to scan.
* **_`custom_targets`:_** Custom targets for `make`, in the following format:

```
"custom_targets": {
    "target_name": "command",
    "other_target": "other_command",
    ...
}"
````

* **_`verbose`:_** `true` if you want to print entire source tree while scanning.
* **_`rm`:_** Command to use for **_`make clean`_** (`rm -v`, by default).
* **_`build_directory`:_** Path where you want to build the project.
* **_`bin_directory`:_** Binary output file (e.g. where you want to put final executable).

For more details:

`python3 -m makefile_creator -h`

Run the script:

`python3 -m makefile_creator`

Now MakeFile-Creator will generate makefiles. Feel free to change this setting in 
`mfc.config.json` according to your requirements.

## Authors

* **Romulus-Emanuel Ruja <<romulus-emanuel.ruja@tutanota.com>>**

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

* **_New in version v0.0.9-beta (November 2020):_**
    * Added libs support (`libs`).
    * Added include paths support (`include_paths`).
    * All makefiles and deps files are now put into `build` directory.
    * Code refactoring.

* **_New in version v0.0.8-beta (November 2020):_**
    * Added **command line arguments**. Now you can generate configuration file from command line
    and also update, or override settings.
    * Build files are now put in a separate directory (`build_directory`).
    * Added separate **command for Linker** (`ld`).
    * Other code refactoring and bugs fixed.