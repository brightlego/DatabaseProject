import tkinter as tk
import gui.templates


class InputField(gui.templates.Page):
    def _init_elements(self):
        self.__searchdata = SearchData(self)
        self.__setdata = SetData(self)
        self.__optionalbox = OptionalBox(self.__searchdata)
        self.__elements = []
        self.__title = tk.Label(self)
        self.__query = None

        self.__title.pack()
        self.__searchdata.pack(expand=True, fill=tk.BOTH, pady=10)
        self.__setdata.pack(expand=True, fill=tk.BOTH, pady=10)
        self.__optionalbox.grid(column=1, columnspan=100, row=100, pady=10)

    def set_template(self, template):
        for item in self.__elements:
            item.destroy()
        root = template.getroot()
        self.__title["text"] = root.attrib["title"]
        self.__query = self._parent.gen_new_query(root.attrib["type"])
        for item in root:
            if item.tag == "search-data":
                self.__set_data(self.__searchdata, item)
            elif item.tag == "set-data":
                self.__set_data(self.__setdata, item)

    def __set_data(self, parent, root):
        row = 1
        for item in root:
            if item.tag == "entry":
                self.__elements.append(Entry(parent, item, row, root.tag))
            elif item.tag == "optional":
                self.__set_data(self.__optionalbox, item)
            row += 1

    def get_query(self):
        return self.__query

    def set_query(self):
        for element in self.__elements:
            element.set_query()


class SearchData(gui.templates.HollowPage):
    pass


class SetData(gui.templates.HollowPage):
    pass


class OptionalBox(gui.templates.HollowPage):
    def _init_elements(self):
        self.__label = tk.Label(self)
        self.__label.grid(column=0, columnspan=10, row=0)


class Entry:
    def __init__(self, parent, item, row, type_):
        self.__parent = parent
        self.__item = item
        self.__type = type_
        attrib = item.attrib
        self.__label = tk.Label(parent, text=attrib["label"])
        self.__entryvar = tk.StringVar()
        self.__entry = tk.Entry(parent, textvariable=self.__entryvar)

        self.__label.grid(column=1, row=row, sticky=tk.E)
        self.__entry.grid(column=2, row=row)

    def destroy(self):
        self.__label.destroy()
        self.__entry.destroy()

    def set_query(self):
        query = self.__parent.get_query()
        if self.__type == "search-data":
            query.update_constraint(
                self.__item.attrib["field"],
                self.__item.attrib["table"],
                self.__entryvar.get(),
            )
        else:
            query.update_data(
                self.__item.attrib["field"],
                self.__item.attrib["table"],
                self.__entryvar.get(),
            )
