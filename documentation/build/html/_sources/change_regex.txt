.. default-domain:: python

.. highlight:: python3
   :linenothreshold: 4

#####################
Change Version Number
#####################

This standalone script will search for all occurencies of version statements and replace them with a new version number.

.. py:method:: parsing()

    This class sets the available input options for the script. Currently there is only one additional
    option available, `-p` to set the repository path to search in.

::

    def parsing():
    
        parser = OptionParser("usage: %prog version_number -p repository path",
                              description="Small script to change the version number from a central point.",
                              version="%prog " + __version__)
    
        parser.add_option("-p", "--path", dest="repo_path", default="",
                          type="string", help="The path to the repository")
    
        options,  args = parser.parse_args()
    
        return (options, args, parser)


.. py:method:: main()

    This is the main class. It contains the regex search, as well as the replacement of the old version number.


The options coming from `parsing()` are set. If there is no repo_path set by the user, we take the current path.
If there is a repo_path set by the user, we change into that path.


::

    
    def main():
    
        options, args, parser = parsing()
    
        if options.repo_path:
            os.chdir(os.path.abspath(repo_path))
    
        if not args:
            parser.print_help()
            sys.exit(1)
    

The regex search pattern is defined. The directories in which we do not want to search for occurencies of the
version number are defined.


::

    
        p = re.compile(r'version.*(\d+\.\d+\.\d+)', re.IGNORECASE)
        exclude = set(['.git', '__pycache__', 'dist', 'doctrees', 'build'])
    

We recursively search through the current directory and sub-directories for occurencies of a version number.
If there is a line that matches our criteria, we save it as a `match`. The user then gets notified that there
is a matching line in a file and that we change it to the selected (new) version number the user set. After that
we actually change the version number.


::

    
        for root, dirs, files in os.walk(os.getcwd(), topdown=True):
            dirs[:] = [d for d in dirs if d not in exclude]
    
            for filename in files:
                fname = os.path.join(root, filename)
    
                if os.path.isfile(fname) and not fname.endswith('.rst'):
                    with open(fname, "r", encoding="utf8") as f:
    
                        lines = f.read()
                        lines_check = lines
                        match = re.search(p, lines)
    
                        if match:
                            print(fname, match.group(1), "-->", args[0], "\n")
    
                            with open(fname, "w") as f:
                                f.write(re.sub(match.group(1), args[0], lines))
    




