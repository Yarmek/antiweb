from optparse import OptionParser
import sys
import os.path
import logging

logger = logging.getLogger('change_vn')

__version__ = "0.1"

def change_vnumber(vnumber, pattern,  in_file):
    file_path = os.path.join(os.getcwd(), in_file)

    linenumber = None
    content = None

    with open(file_path,  'r') as file:
            for num,  line in enumerate(file):
                if pattern in line:
                    linenumber = num

                if linenumber:
                    file.seek(0, 0)
                    content = file.readlines()
                    del content[linenumber]
                    content.insert(linenumber,  pattern+vnumber)

    if content:
        with open(file_path, "w") as file:
                    for item in content:
                        file.write(item)

def parsing():

    parser = OptionParser("usage: %prog -n version_number",
                          description="Small script to change the version number from a central point.",
                          version="%prog " + __version__)

    parser.add_option("-n", "--vnumber", dest="vnumber", default="",
                      type="string", help="The version number to insert")

    options,  args = parser.parse_args()

    return (options, args, parser)
#@(parsing)

def main():

    options, args, parser = parsing()

    logger.addHandler(logging.StreamHandler())
    logger.setLevel(logging.INFO)

    if not options.vnumber:
        parser.print_help()
        sys.exit(1)
    os.chdir(os.path.dirname(__file__))


    anti_number = "\""+options.vnumber+"\"\n"
    anti_pattern = "__version__ = "

    change_vnumber(anti_number, anti_pattern, "antiweb.py")



    pkg_number = options.vnumber+"\n"
    pkg_pattern = "Version: "

    change_vnumber(pkg_number, pkg_pattern, "PKG-INFO")


    readme_number = pkg_number
    readme_pattern = pkg_pattern

    change_vnumber(readme_number, readme_pattern, "README.md")


    setup_number = "\'"+options.vnumber+"\',\n"
    setup_pattern = "    version="

    change_vnumber(setup_number,  setup_pattern, "setup.py")

    anti_number = options.vnumber+"\n"
    anti_pattern = "Version: "

    change_vnumber(anti_number, anti_pattern, "antiweb.py")


if __name__ == "__main__":
    main()
