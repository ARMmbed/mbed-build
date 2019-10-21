# Mbed OS configuration
Each application has an ```mbed_app.json``` file at the root of the project. This can provide per-target values for configuration variables declared by mbed-os and any other libraries included by the program.

Each library has a file ```mbed_lib.json``` at the root of the library (or in ```platform``` for the mbed-os codebase). Each entry in these files represents a configuration parameter that affects some aspect of that library's operation. A complex set of rules governs the final value, including:

* Default value in the ```mbed_lib.json``` file
* the contents of ```targets.json```???
* Compiler profiles???
* The build system code???

A pre-build step determines the final value, generating a file ```mbed_config.h``` in the ```BUILD``` directory for the current build. The configuration is based on the chosen set of configuration values derived from all of the possible options presented in each included library, plus the platform. One ```#define``` entry is generated per configuration value.

When exporting, an ```mbed_config.h``` file is generated for the target specified in the export command. However this file does not appear to be referenced in the build.

## mbed_config.py rules
From mbed_toolchain.py: 

"The config file is located in the build directory

- if there is no configuration data, ```mbed_config.h``` will not exists.
- if there is configuration data and ```mbed_config.h``` does not exist,
          it is created.
- if there is configuration data that is the same as the previous
          configuration data, ```mbed_config.h``` is left untouched.
- if there is new configuration data, ```mbed_config.h``` is overriden.
"        

### Problem
Changing any configuration value causes any existing build to be invalidated, requiring a full rebuild irrespective of whether the value(s) changed affect the code.

### Proposal
The configuration should be divided up into sections such that configuration changes are isolated to those parts of the code that are affected. One possible scheme is to generate multiple ```mbed_config.h``` files, one per library, and put them in a central place for the code to access. Only regenerate the files that change, and hence no need to invalidate the whole build.

### Migrating existing code
Generate a revised ```mbed_config.h``` that is simply a collection of all sub-configs. Generate sub-configs based on the presence of ```mbed_lib.json```.

* Note: Diagrams are drawn using [http://plantuml.com/activity-diagram-beta](plantUML)


# More stuff
There are two parts to this configuration story. mbed OS can be considered as a collection of software components/libraries/features and a collection of targets. This lot is combined with a chunk of generic operating system code. 

When building for a specific target the build system consults the collection of configuration files and forms a set of configuration parameters with specific values defined.
