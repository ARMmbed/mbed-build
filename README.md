# mbed-build
Python package containing interfacing to toolchains and CMake preparation

# Sub directories:
## CMake Trial
A folder containing example code to experiment with different CMake control configurations.

## Top-level structure
For any CMake project there needs to be one ```CMakeLists.txt``` file at the root of the project tree. This containis information about the project and any rules required to generate the build commands for the final executable. Subordinate software component directories under the root may have their own ```CMakeLists.txt``` file to specify how they are constructed.

In our case we intend to generate a significant amount of the top-level CMake file to handle different target and tolchain combinations. Subordinate library ```CMakeLists.txt``` files are expected to be managed by the code development teams directly.

The top-level ```CMakeLists.txt``` file must contain the following lines:

```
cmake_minimum_required (VERSION 3.12.4)
project (<project_name>)
```

## Building
Use ```cmake .``` at the top level of the source tree (ie in the directory containing the ```CmakeLists.txt``` file.
## Customising the build
We recognise that many users will want to customise their builds, but this conflicts with the generation of a full ```CMakeLists.txt``` file (since any customisation would be lost on regeneration).

The proposal is to use a fairly minimal ```CMakeLists.txt``` at the top level that includes a second file containing only generated build commands. For new programs where the initial ```CMakeLists.txt``` file is not present we would generate one of these too.

The advantage of this approach is that users who wish to customise their installation can simply replace the top-level ```CMakeLists.txt``` and do anything they want. 

### Controlling library inclusion
An associated issue is that of controlling the (massive) list of component code that is compiled as part of a standard mbed OS build. We would seek to place a guard around all library code in the generated top-level file that is enabled by default. Should the user wish to remove this library then he can customise his ```CMakeLists.txt``` file to set the guard variable to exclude the library code.

## Running cmake for the first time
The recommended way of operating here is to generate the build system in a separate directory from that containing the source. This is called an out-of-tree build.

1. Create a ```build-dir``` directory at the top level of the source tree (ie in the directory containing the ```CmakeLists.txt``` file).   contain the generated build components, Typically this is inside the source tree but is added to the gitignore file to prevent built artefacts from being committed.
2. Run CMake from within this directory and reference the source dir.
3. When the build system has been generated, use cmake again to build the project executable using the generated build system.

Here are the commands

```
 mkdir build-dir
 cd build-dir
 cmake ..				# Generate the various make system control files
 cmake --build .		# Perform the actual build
```

Note that this example generates a build system based on ```make```, but CMake can be instructed to generate a build system for lots of different environments. This key feature will be used to allw many of our existing exporters to be eliminated.

## Fragments
### Specifying a library
Each separate lbrary must have a ```add_subdirectory (alib)``` in the parent cmake file so that the content of the library can be included.

### Specifying a #define entry
Use ```add_compile_definitions(FOO=1)``` to generate a ```-DFOO=1``` on the compiler command line.

# Generation requirements
The mbed build system will need to provide the following to enable the generation of the top-level ```CMakeLists.txt``` file:

* A list of resolved target configuration options for the selected target
* A list of libraries to include in the compilation
* A list of command line options for the selected toolchain
