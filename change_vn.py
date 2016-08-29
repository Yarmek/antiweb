from optparse import OptionParser
import sys
import os.path
import logging

logger = logging.getLogger('change_vn')

__version__ = "0.1.1"

def change_vnumber(vnumber, pattern,  file_path):

    linenumber = None
    content = None

    with open(file_path,  'r') as file:
            for num,  line in enumerate(file):
                if pattern in line:
                    linenumber = num

                if linenumber:
                    file.seek(0, 0)
                    content = file.readlines()
                    content_check = content
                    del content[linenumber]
                    content.insert(linenumber,  pattern+vnumber)

    # Check, if the lenght of the new content matches the lenght of the old content.
    # This makes sure that the new content will not be written when there is an error during the process.
    if len(content)==len(content_check):
        with open(file_path, "w") as file:
                    for item in content:
                        file.write(item)

    else:
        print("Could not write in file: ", file_path)


def parsing():

    parser = OptionParser("usage: %prog repo_path -n version_number",
                          description="Small script to change the version number from a central point.",
                          version="%prog " + __version__)

    parser.add_option("-n", "--vnumber", dest="vnumber", default="",
                      type="string", help="The version number to insert")

    options,  args = parser.parse_args()

    if not args[0]:
        args.append(os.getcwd())

    return (options, args, parser)
#@(parsing)

def main():

    options, args, parser = parsing()

    repo_path = args[0]

    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)

    if not options.vnumber:
        parser.print_help()
        sys.exit(1)
    os.chdir(os.path.dirname(__file__))

    # Changes the version number for antiweb
    anti_number = "\""+options.vnumber+"\"\n"
    anti_pattern = "__version__ = "
    file_path = os.path.abspath(os.path.join(repo_path, "antiweb.py"))

    change_vnumber(anti_number, anti_pattern, file_path)

    # Changes the version number for antiweb in its own doc
    anti_number = options.vnumber+"\n"
    anti_pattern = "Version: "
    file_path = os.path.abspath(os.path.join(repo_path, "antiweb.py"))

    change_vnumber(anti_number, anti_pattern, file_path)


    # Changes the version number in the package info
    pkg_number = options.vnumber+"\n"
    pkg_pattern = "Version: "
    file_path = os.path.abspath(os.path.join(repo_path, "PKG-INFO"))

    change_vnumber(pkg_number, pkg_pattern, file_path)

    # Changes the version number in the readme file
    readme_number = pkg_number
    readme_pattern = pkg_pattern
    file_path = os.path.abspath(os.path.join(repo_path, "README.md"))

    change_vnumber(readme_number, readme_pattern, file_path)


    # Changes the version number in the setup file (needed for installation)
    setup_number = "\'"+options.vnumber+"\',\n"
    setup_pattern = "    version="
    file_path = os.path.abspath(os.path.join(repo_path, "setup.py"))

    change_vnumber(setup_number,  setup_pattern, file_path)


    # Changes the version number in Sphinx config file
    setup_number = "\'"+options.vnumber+"\'\n"
    setup_pattern = "version = "
    file_path = os.path.abspath(os.path.join(repo_path, "documentation\source\conf.py"))

    change_vnumber(setup_number,  setup_pattern, file_path)


if __name__ == "__main__":
    main()
