# Import the os module, for the os.walk function
import os
from jinja2 import Template

# Set the directory you want to start from
root_dir = '../full-trial'
program_name = "full-trial"

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

#
template_content = ""
with open('template_cmakelists.j2') as t_file:
    template_content = t_file.read()

t = Template(template_content)

for library in libraries:
    # Expand the library content
    library.evaluate_content()

    cml_file = os.path.join(library.root_dir, "CMakeLists.txt")
    if os.path.exists(cml_file):
        with open(cml_file, "w") as cmake_lists_file:
            cmake_lists_file.write(t.render(program_name=program_name, library=library))
    else:
        print(f"Not overwriting {cml_file}")

# Write the top level CMakeLists.txt file
template_content = ""
with open('top-level-cml.j2') as t_file:
    template_content = t_file.read()

t = Template(template_content)
with open(os.path.join(root_dir, "CMakeLists.txt"), "w") as top_level_cmake_lists_file:
    top_level_cmake_lists_file.write(t.render(program_name=program_name))

print("All done")
