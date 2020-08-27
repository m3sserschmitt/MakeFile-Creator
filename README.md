# MakeFile Creator

MakeFile-Creator is an utility for managing makefiles in C/C++ projects.

## How it works?

Install the package from Python Package Index using the command:

`pip3 install mfc`

Then:

`cd /your/project/path`

## Configuration

You have to create a configuration file, using JSON format as follows:
You may want to use this command from terminal (or open your favourite text editor, and after you've done, save as `mfc.config.json`):

`touch mfc.config.json`

File content should be something like this:

```
{
    "target": "your_project_name", 
	"c_flags": [list, of, compiler, flags],
    "cc": "g++",
    "extensions": ["cc", "cpp"],
    "rm": "rm -v",
	"ignore_paths": [
		"comma/separated/list/of/paths/you/want/to/ignore",
        "path1",
        "path2",
        "and/so/on/..."
	    ]
}
```

Meaning:
* _**`target`:**_ you project name.
* _**`c_flags`:**_ a list of compiler flags, like:
    
    `["-Wall", "-lpthread", "-other_flags..."]`.
* **_`cc`:_** compiler command (`"g++"`, by default).
* **_`extensions`:_** source files extensions list (`["cpp"]`, by default).
* **_`rm`:_** command to use for **_`make clean`_** (`rm -v`, by default).
* **_`ignore_paths`:_** paths into project source tree to ignore.

##### Other commands:

* _**`clean`:**_ `true`, if you want to clean redundant dependencies .d files (`false`, by default).
##### **Make sure to save the file as `mfc.config.json` !**