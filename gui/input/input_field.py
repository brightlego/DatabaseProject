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
        self.__submit_button = SubmitButton(self)

        self.__title.grid(column=0, row=0)
        self.__searchdata.grid(column=0, columnspan=3, row=1, pady=5)
        self.__setdata.grid(column=0, columnspan=3, row=2, pady=5)
        self.__submit_button.grid(column=2, row=3)
        self.__optionalbox.grid(column=1, columnspan=100, row=100, pady=2)

        self.__check_empty_widgets()

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

        self.__check_empty_widgets()

    def __check_empty_widgets(self):
        print(self.__searchdata.winfo_children())
        if len(self.__searchdata.winfo_children()) <= 1:
            self.__searchdata.grid_remove()
        else:
            self.__searchdata.grid()

        if len(self.__setdata.winfo_children()) == 0:
            self.__setdata.grid_remove()
        else:
            self.__setdata.grid()

        if len(self.__optionalbox.winfo_children()) == 0:
            self.__optionalbox.grid_remove()
        else:
            self.__optionalbox.grid()

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

    def submit_query(self):
        self.set_query()
        self._parent.submit_query(self.__query)


class SearchData(gui.templates.HollowPage):
    pass


class SetData(gui.templates.HollowPage):
    pass


class OptionalBox(gui.templates.HollowPage):
    def _init_elements(self):
        self.__label = tk.Label(self, text="Optional:")
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


class SubmitButton(gui.templates.Button):
    def _get_text(self):
        return "Submit"

    def _command(self):
        self._parent.submit_query()
