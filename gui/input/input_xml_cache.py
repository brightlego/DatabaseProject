import os
import xml.etree.ElementTree as ET

DIR = os.path.split(os.path.realpath(__file__))[0]


class XMLCache:
    def __init__(self):
        self.add_cache = self.__setup_cache("add")
        self.get_cache = self.__setup_cache("get")
        self.chg_cache = self.__setup_cache("change")
        self.rem_cache = self.__setup_cache("remove")

    def __setup_cache(self, cache_dir):
        path = os.path.join(DIR, "templates", cache_dir)
        if not os.path.exists(path):
            raise FileNotFoundError(f"Missing {cache_dir} from templates.")
        cache = {}

        with os.scandir(path) as it:
            is_empty = True
            for entry in it:
                is_empty = False
                if not os.path.splitext(entry.name)[1] == ".xml":
                    print("Warning: Non XML file in templates folder")
                    continue
                try:
                    tree = ET.parse(entry.path)
                    root = tree.getroot()
                    name = root.attrib["title"]
                    cache[name] = tree

                except ET.ParseError:
                    print(f"Error encountered when parsing {entry.path}:")
                    raise

                except IndexError:
                    print("Missing Attribute:")
                    raise

            if is_empty:
                print(f"Warning: directory {path} is empty")
        return cache
