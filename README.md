# mbed-build
Python package containing interfacing to toolchains and CMake preparation

# Sub directories:
## CMake Trial
A folder containing example code to experiment with different CMake control configurations.

## Top-level structure
For any CMake project there needs to be one ```CMakeLists.txt``` file at the root of the project tree. This containis information about the project and any rules required to generate the build commands for the final executable. Subordinate software component directories under the root may have their own ```CMakeLists.txt``` file to specify how they are constructed.

In our case we intend to generate a significant amount of the top-level CMake file to handle differnt target and tolchain combinations. Subordinate library ```CMakeLists.txt``` files are expected to be managed by the code development teams directly.

The top-level ```CMakeLists.txt``` file must contain the following lines:

```
cmake_minimum_required (VERSION 3.12.4)
project (<project_name>)
```

## Building
Use ```cmake .``` at the top level of the source tree (ie in the directory containing the ```CmakeLists.txt``` file.
## Running cmake for the first time
Use ```cmake .``` at the top level of the source tree (ie in the directory containing the ```CmakeLists.txt``` file). This will generate the makefiles throughout the source hierarchy that are used to instruct the build process. 

When the makefiles have been generated, running ```make``` should build the project executable.

## Fragments
### Specifying a library
Each separate lbrary must have a ```add_subdirectory (alib)``` in the parent cmake file so that the content of the library can be included.

### Specifying a #define entry
Use ```add_compile_definitions(FOO=1)``` to generate a ```-DFOO=1``` on the compiler command line.
