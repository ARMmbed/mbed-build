# mbed-build
Python package containing interfacing to toolchains and CMake preparation

# Sub directories:
## CMake Trial
A folder containing example code to experiment with different CMake control configurations.

## Top-level structure
For any CMake project there needs to be one ```CMakeLists.txt``` file at the root of the project tree. This contains information about the project and any rules required to generate the build commands for the final executable. Subordinate software component directories under the root may have their own ```CMakeLists.txt``` file to specify how they are constructed.

In our case we intend to generate a significant amount of the top-level CMake file to handle different target and toolchain combinations. Subordinate library ```CMakeLists.txt``` files are expected to be managed by the code development teams directly.

The top-level ```CMakeLists.txt``` file must contain the following line as a minimum:

```
project (<project_name>)
```

## Building
Use ```cmake .``` at the top level of the source tree (ie in the directory containing the ```CmakeLists.txt``` file.
It is desirable to also include a minimum version requirement on CMake itself:

```cmake_minimum_required (VERSION 3.12.4)```

One or more ```add_executable()``` entries must also appear but these will be generated as described below.

## Customising the build
We recognise that many users will want to customise their builds, but this conflicts with the generation of a full ```CMakeLists.txt``` file (since any customisation would be lost on regeneration).

The proposal is to use a fairly minimal ```CMakeLists.txt``` at the top level that includes a second file ```CMakeLists-<target-id>.inc``` containing only generated build commands for a specific target device. For new programs where the initial ```CMakeLists.txt``` file is not present we would generate one of these too.

The advantage of this approach is that users who wish to customise their installation can simply replace the top-level ```CMakeLists.txt``` and do anything they want. 

### Multiple target hardware support
It is possible to describe multiple build targets in a single CMake file. This seems to be tyically used to support different configurations (eg release, debug) and is probably better associated with the mbed OS concept of build profiles.

Propose that each target device has its own separate build configuration. The generated part in ```CMakeLists-<target-id>.inc``` will be hardware target specific and will be included as appropriate into ```CMakeLists.txt```

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

Note that this example generates a build system based on ```make```, but CMake can be instructed to generate a build system for lots of different environments. This key feature will be used to allow many of our existing exporters to be eliminated.

## Fragments
### Specifying a library
Each separate component must have a ```add_subdirectory (path/to/library)``` in the parent cmake file so that the content of the 
component can be included. The ```add_subdirectory``` directive appears to tell CMAKE to expect a ```CMakeLists.txt``` file in that directory.

### Specifying a #define entry
Use ```add_compile_definitions(FOO=1)``` to generate a ```-DFOO=1``` on the compiler command line.

# Generation requirements
The mbed build system will need to provide the following to enable the generation of the top-level ```CMakeLists.txt``` file:

* A list of resolved target configuration options for the selected target
* A list of libraries to include in the compilation
* A list of command line options for the selected toolchain

The code for these operations must already exist inside the current tools codebase somewhere.

# Development approach
There is a simple example in ```simple-trial``` that was built to allow some ideas to be prototyped.
```full-trial``` is a full checkout of a blinky project with the git repositories removed from mbed-os. It now contains experimental changes to add CMake to be trialled on a full mbed build.

## What do we already have?
Start with the existing mbed export for a CMake project. This is pretty crude at the moment; it simply adds every C and H file to the ``add_executable()`` section. A ```include_directories()``` section is constructed from a recursive traversal of the project tree, adding every directory in the project.
```add_definitions()``` section is filled with definitions derived from the configuration system (these appear to be the same as those in ```mbed_config.h```).

However, this does produce a valid build. Note that the content of the ```CMakeLists.txt``` file generated by the existing exporter is highly dependent on the chosen target, toolchain and configuration.

There is a script called ```export_samples.sh``` in the ```scripts``` directory that will do exports for multiple targets and allows the differences to be compared and investigated.

## How to change
Looking at the existing exported ```CMakeLists.txt``` as a starting point, there are two major sections: ```include_directories()``` and ```add_executable()```. It 
appears as though ```include_directories()``` contains almost every directory within the whole of the mbed-os hierarchy, and ```add_executable()``` contains almost every
header and every source file in the whole of mbed-os. Note the 'almost' here; the actual choice seems to be dependent on target, config and toolchain.

Look for all those directories that appear to contain components. These should be identifiable as they generally contain a file called ```mbed_lib.json``` at the top-level of their tree. Each of these becomes a library in its own right. Note that the library name is going to be global throughout the project, so it needs to be unique. We need to find a naming scheme that will ensure this.

Replacing these with an appropriate ```CMakeLists.txt``` file could then allow that whole tree to be managed as a component. The corresponding directories can then be removed from the top level directories list, and files removed from the add_executable in favour of the generated archive.

This change can be done over a period of time. The ```CMakeLists.txt``` files can be initially generated as placeholders.


### Refactoring components
* Create a ```CMakeLists.txt``` file in the component directory next to the existing ```mbed_lib.json``` file
* Register this as a library, using all of the source files mentioned in the existing top-level ```CMakeLists.txt``` file. The source files need not include headers; and should
be relative to the top of the library tree.
   * ```add_library(libname source1 source2...)```
   
* Reference the header files exported by this component using ```target_include_directories()```. Note that they will all be PUBLIC at this stage, until reviewed by the mbed-os team
   
The top-level ```CMakeLists.txt``` file needs to be modified to include the new component:

* Add a ```add_subdirectory(/path/to/component)``` directive below ```include_directories()```. Order matters; putting the ```add_subdirectory()``` directive after 
the top-level ```include_directories()``` allows the 'global' ```mbed_config.h``` to be found
* Add the name of the new library to the ```target_link_libraries()``` directive.
* Remove the corresponding file references in the existing ```include_directories()``` directive
* Remove the corresponding file references in the ```add_executable()``` directive

Note that this should not alter the build in any way, other than to put the structure in place.

### Compiler flags
Suggestion from [here](https://pabloariasal.github.io/2018/02/19/its-time-to-do-cmake-right/) is not to alter ```CMAKE_CXX_FLAGS``` directly. Instead 
we should be using one of the following directives: 

* ```target_compile_options()``` for options that are required to build the current target
* ```target_compile_features()``` for options that are to be propagated to users of this target

## A gotcha
Creating a separate .inc file for the generated content does not work as expected at the top level. The set() statements have a different effect and do not correctly pick up the cross compiler if they are in an included file. No idea why at the moment.

## Build times
This is a comparison of build times for various configurations. In each case we build blinky with mbed-os 5.15 for the K64F target on a MacBook Pro (2 core). This is the baseline; opefully we might be able to improve on these times by breaking up mbed-os.

### Exported cmake build
Building with the original CMakeLists.txt exported from mbed OS tools using ```mbed export -i eclipse_gcc_arm -m K64F```
Build command: ```time cmake --build .```

* real	5m40.395s
* user	3m25.836s
* sys	2m0.438s

This does not include the short 10 seconds or so that cmake requires to run the initial ```cmake ..```
### Original build system with gcc compiler toolchain
Build command: ```time mbed compile -t GCC_ARM -m K64F```

* real	2m12.723s
* user	4m29.475s
* sys	2m0.357s

### Original build system with armcc6 compiler toolchain
Build command: ```time mbed compile -t ARMC6 -m K64F```

* real	1m37.021s
* user	3m55.278s
* sys	1m2.505s

# Flags
### ```CMAKE_CROSSCOMPILING```
Set to TRUE to indicate that CMake is cross compiling. Note that this need note be set now, since setting ```CMAKE_SYSTEM_NAME``` implies cross compilation. See [here](https://cmake.org/cmake/help/latest/variable/CMAKE_CROSSCOMPILING.html)
### ```CMAKE_SYSTEM_NAME```
Set to the name of the operating system for which CMake is building. If set, then also set ```CMAKE_SYSTEM_VERSION```. See [here](https://cmake.org/cmake/help/latest/variable/CMAKE_SYSTEM_NAME.html)
### ```CMAKE_SYSTEM_VERSION```
The version of the operating system for which CMake is to build. See [here](https://cmake.org/cmake/help/latest/variable/CMAKE_SYSTEM_VERSION.html)

# Resources
* https://pabloariasal.github.io/2018/02/19/its-time-to-do-cmake-right/

# Existing Export Function
