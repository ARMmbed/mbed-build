# mbed-build
Python package containing interfacing to toolchains and CMake preparation

# Sub directories:
## CMake Trial
A folder containing example code to experiment with different CMake control configurations.

Each separate lbrary must have a ```add_subdirectory (alib)``` in the parent cmake file so that the content of the library can be included.

The top-level ```CMakeLists.txt``` file must contain the following lines:

```
cmake_minimum_required (VERSION 3.12.4)
project (<project_name>)
```

## Building
Use ```cmake .``` at the top level of the source tree (ie in the directory containing the ```CmakeLists.txt``` file.
