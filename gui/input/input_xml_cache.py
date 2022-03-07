"""Deals with the cache of the XML data"""

import os
import xml.etree.ElementTree as ET

# The directory this file is stored in
DIR = os.path.split(os.path.realpath(__file__))[0]


class XMLCache:
    """The cache for the XML data

    Attributes:
        Public:
            add_cache (dict[str:xml.etree.ElementTree.ElementTree])
                -- Cache of add tabs
            get_cache (dict[str:xml.etree.ElementTree.ElementTree])
                -- Cache of get tabs
            chg_cache (dict[str:xml.etree.ElementTree.ElementTree])
                -- Cache of change tabs
            rem_cache (dict[str:xml.etree.ElementTree.ElementTree])
                -- Cache of remove tabs

    Methods:
        Magic:
            __init__() -> None

        Private:
            __setup_cache(cache_dir:str)
                -> dict[str:xml.etree.ElementTree.ElementTree]
                -- Sets up a cache

    """

    def __init__(self):
        """Constructor for XMLCache

        Arguments:
            None

        Returns:
            None
        """

        # Setup all the caches
        self.add_cache = self.__setup_cache("add")
        self.get_cache = self.__setup_cache("get")
        self.chg_cache = self.__setup_cache("change")
        self.rem_cache = self.__setup_cache("remove")

    def __setup_cache(self, cache_dir):
        """Sets up the cache for a certain directory

        Arguments:
            cache_dir (str)
                -- The directory of the caches

        Returns:
            cache (dict[str:xml.etree.ElementTree.ElementTree])
                -- The cache
        """
        # Join the path
        path = os.path.join(DIR, "templates", cache_dir)

        # If the path does not exist, raise a FileNotFoundError
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing {cache_dir} from templates.")

        # The cache
        cache = {}

        # Scan that directory
        with os.scandir(path) as iterator:
            is_empty = True  # Used to check if the directory is empty

            # For each entry in the directory
            for entry in iterator:
                # Remember the directory not being empty
                is_empty = False

                # If the file does not end in a .xml, ignore it and warn
                if not os.path.splitext(entry.name)[1] == ".xml":
                    print("Warning: Non XML file in templates folder")
                    continue

                try:
                    # Parse the file
                    tree = ET.parse(entry.path)

                    # Get the title of the root
                    root = tree.getroot()
                    name = root.attrib["title"]

                    # Cache the tree
                    cache[name] = tree

                # If there is a parsing error, notify which file its in
                except ET.ParseError:
                    print(f"Error encountered when parsing {entry.path}:")
                    raise

                # If root has no title, raise an error
                except IndexError:
                    print("Missing Attribute:")
                    raise

            # Warn if the directory is empty
            if is_empty:
                print(f"Warning: directory {path} is empty")

        # Return the cache
        return cache
