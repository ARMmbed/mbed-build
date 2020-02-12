# Import the os module, for the os.walk function
import os
from jinja2 import Template

# Set the directory you want to start from
root_dir = '../full-trial'
program_name = "full-trial"

OVERWRITE_TOP = True
OVERWRITE_LIBS = True


class Library:
    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.sub_dirs = []

    def evaluate_content(self):
        for dir_name, sub_dir_list, file_list in os.walk(self.root_dir):
            # Make the path relative tot he library location
            self.sub_dirs.append(os.path.relpath(dir_name, self.root_dir))


# ====================================================
libraries = []
current_library = None

# Locate all the libraries from directories that contain an mbed_lib.json file
for dir_name, sub_dir_list, file_list in os.walk(root_dir):

    # print(f'Evaluating directory: {dir_name}')

    if os.path.exists(os.path.join(dir_name, "mbed_lib.json")):
        print(f"---Directory {dir_name} is a lib root")
        sub_dir_list.clear()
        libraries.append(Library(dir_name))

# Read in the two templates...
with open('library_cmakelists_cmake.j2') as t_file:
    inc_template = Template(t_file.read())

with open('library_cmakelists_txt.j2') as t_file:
    txt_template = Template(t_file.read())

# Write out the CMakeLists.{inc|txt} file for each library
for library in libraries:
    # Expand the library content
    library.evaluate_content()

    # The include file can be overwritten every time; it should not be edited
    cml_file = os.path.join(library.root_dir, "CMakeLists-gen.cmake")
    with open(cml_file, "w") as cmake_lists_file:
        cmake_lists_file.write(inc_template.render(program_name=program_name, library=library))

    # This file is only written if it doesn't already exist
    cml_file = os.path.join(library.root_dir, "CMakeLists.txt")
    if not OVERWRITE_LIBS and os.path.exists(cml_file):
        print(f"Not overwriting {cml_file}")
    else:
        with open(cml_file, "w") as cmake_lists_file:
            cmake_lists_file.write(txt_template.render(program_name=program_name, library=library))

# Regenerate the top level CMakeLists.inc file every time
with open(os.path.join(root_dir, "CMakeLists-gen.cmake"), "w") as top_level_cmake_lists_file:
    with open('top_cmakelists_cmake.j2') as t_file:
        template = Template(t_file.read())

    top_level_cmake_lists_file.write(template.render(program_name=program_name))

# Regenerate the top level CMakeLists.inc file if it doesn't already exist
cml_file = os.path.join(root_dir, "CMakeLists.txt")
if not OVERWRITE_TOP and os.path.exists(cml_file):
    print(f"Not overwriting {cml_file}")
else:
    with open(cml_file, "w") as top_level_cmake_lists_file:
        with open('top_cmakelists_txt.j2') as t_file:
            template = Template(t_file.read())

        top_level_cmake_lists_file.write(template.render(program_name=program_name))

print("All done")
