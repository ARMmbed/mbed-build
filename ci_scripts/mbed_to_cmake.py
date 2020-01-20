"""********* WIP *********
Covert Mbed OS 5 and Mbed OS 5 projects from the current build system to CMake for Mbed 6.

This applies and in situ, replacement of the build files (optionally removing the originals), ensure all changes are
committed before running.
"""

import logging
import os
import sys
import argparse
import json
import jinja2

logger = logging.getLogger(__name__)

jinja2_env = jinja2.Environment(
    loader=jinja2.PackageLoader('ci_scripts.mbed_to_cmake', 'templates'),
    autoescape=jinja2.select_autoescape(['html', 'xml'])
)


class BuildCMakeLists:
    """Container and renderer for Mbed OS build results."""

    def __init__(self, input_dir, dryrun, delete_originals):
        """Create CMakeList file builder.
        :param str input_dir: Root directory start looking for Mbed OS 5 build files.
        """
        self._input_dir = os.path.expanduser(input_dir)
        self._current_dir = input_dir

    def _render_templates(self, template_files, **template_kwargs):
        """Render one or more jinja2 templates.

        The output name is based on the template name (with the final extension removed).

        :param list(str) template_files: List of of template file names.
        :param **dict template_kwargs: Keyword arguments to pass to the render method.
        """
        for template_name in template_files:
            output_name = template_name.rsplit('.', 1)[0]
            output_path = os.path.join(self._output_dir, output_name)
            logger.info(f"Rendering template from '{template_name}' to '{output_path}'")
            template = jinja2_env.get_template(template_name)
            rendered = template.render(**template_kwargs)
            with open(output_path, "w") as output_file:
                output_file.write(rendered)

    def _render_cmake_list_file(self):
        """Render summary results page in html."""
        # Setup the key word arguments to pass to the jinja2 template
        template_kwargs = {
            "data": None
        }

        # Re-render the index templates to reflect the new verification data.
        self._render_templates(("CMakeLists.txt.jinja2",), **template_kwargs)

    def _generate_cmake_list_file(self, directory, mbed_lib_file_name):
        mbed_lib_file_path = os.path.join(directory, mbed_lib_file_name)

        with open(mbed_lib_file_path, "r") as mbed_lib_file:
            try:
                json_data = json.loads(mbed_lib_file.read())
            except json.decoder.JSONDecodeError as error:
                print(f"ERROR in {mbed_lib_file_path}")
                print(error)
            else:
                try:
                    library_name = json_data["name"]
                except KeyError:
                    logging.error("Invalid definition in '%s'", mbed_lib_file_path)
                else:
                    print(mbed_lib_file_path, library_name)
                    # Next find the list of all source files and all header files

    def replace_mbed_lib_files(self):
        print(self._input_dir)
        for directory, sub_directories, file_list in os.walk(self._input_dir):
            for file_name in file_list:
                if file_name.lower() == "mbed_lib.json":
                    self._generate_cmake_list_file(directory, file_name)


def main():
    """Handle command line arguments"""
    parser = argparse.ArgumentParser()

    parser.add_argument("input_dir", metavar='input-directory', type=str,
                        help="The root directory of the project which to convert.")
    parser.add_argument("-v", "--verbose", action='count', default=0,
                        help="Increase verbosity (by default errors are reported) e.g. -vvv will show debug messages.")
    parser.add_argument("--delete-originals", action='store_true',
                        help="Delete original Mbed OS 5 build files")
    parser.add_argument("--dryrun", action='store_true',
                        help="Perform a dry run, do not modify or create any files.")
    arguments = parser.parse_args()

    if arguments.verbose > 2:
        log_level = logging.DEBUG
    elif arguments.verbose > 1:
        log_level = logging.INFO
    elif arguments.verbose > 0:
        log_level = logging.WARNING
    else:
        log_level = logging.ERROR

    logging.basicConfig(level=log_level, format='%(levelname)s: %(message)s')

    build = BuildCMakeLists(arguments.input_dir, arguments.dryrun, arguments.delete_originals)
    build.replace_mbed_lib_files()


if __name__ == "__main__":
    sys.exit(main())
