# Building mbed-os as a library

- Generate a CMakeLists.txt file at the top level using the mbed export facility
- Create a new CMakeLists.txt in mbed-os. 
  - Cut the 'add_executable()' directive from the top level make file and paste it back into the mbed-os make file.
  - Change the add_executable into a 'add_library(mbed_os ...)'. 
  - Remove all the 'mbed-os/' prefixes from the file paths.
- Cut the include_directories() directive from the top level file and paste it in below the add_library() in the mbed-os cmake file.
   - Rename include_directories(full-trial ... ) to target_include_directories(mbed_os PUBLIC ...)
   - Remove all the 'mbed-os/' prefixes from the file paths.
   - Add . to the list to replace the bare mbed-os entry
   - Add .. to pull
- Add a 'add_subdirectory(mbed_os) directive to the top level make file to include the new mbed OS library.
 
* Add a new add_executable(full-trial main.cpp) to th top level makefile to build the main exdcutable.
* Add mbed_os to the target_link_libraries() directive in the top level. This registers the mbed_os library as a dependency on the full-trial target.

