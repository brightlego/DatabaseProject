import tkinter as tk
import tkcalendar
import gui.templates
import re


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
        self.__elements = []
        root = template.getroot()
        self.__title["text"] = root.attrib["title"]
        del self.__query
        self.__query = self._parent.gen_new_query(root.attrib["type"])
        for item in root:
            if item.tag == "search-data":
                self.__set_data(self.__searchdata, item)
            elif item.tag == "set-data":
                self.__set_data(self.__setdata, item)
            elif item.tag == "constraints":
                self.__set_data(self, item)

        self.__check_empty_widgets()

    def __check_empty_widgets(self):
        if len(self.__searchdata.winfo_children()) <= 1:
            self.__searchdata.grid_remove()
        else:
            self.__searchdata.grid()

        if len(self.__setdata.winfo_children()) == 0:
            self.__setdata.grid_remove()
        else:
            self.__setdata.grid()

        if len(self.__optionalbox.winfo_children()) <= 1:
            self.__optionalbox.grid_remove()
        else:
            self.__optionalbox.grid()

    def __set_data(self, parent, root):
        row = 1
        for item in root:
            if item.tag == "entry":
                self.__elements.append(Entry(parent, item, row, root.tag))
            elif item.tag == "phone":
                self.__elements.append(PhoneNum(parent, item, row, root.tag))
            elif item.tag == "email":
                self.__elements.append(Email(parent, item, row, root.tag))
            elif item.tag == "radio":
                self.__elements.append(Radio(parent, item, row, root.tag))
            elif item.tag == "date":
                self.__elements.append(Date(parent, item, row, root.tag))
            elif item.tag == "link":
                self.__elements.append(Link(parent, item, row, root.tag))
            elif item.tag == "get-data":
                self.__elements.append(Data(parent, item, row, root.tag))
            elif item.tag == "custom":
                self.__elements.append(Custom(parent, item, row, root.tag))
            elif item.tag == "optional":
                self.__set_data(self.__optionalbox, item)
            row += 1

    def get_query(self):
        return self.__query

    def set_query(self):
        for element in self.__elements:
            error = element.set_query()
            if error is ValueError:
                return ValueError
        return None

    def submit_query(self):
        error = self.set_query()
        if error is ValueError:
            return
        self._parent.submit_query(self.__query)
        self.__query = type(self.__query)()


class SearchData(gui.templates.HollowPage):
    pass


class SetData(gui.templates.HollowPage):
    pass


class OptionalBox(gui.templates.HollowPage):
    def _init_elements(self):
        self.__label = tk.Label(self, text="Optional:")
        self.__label.grid(column=0, columnspan=10, row=0)


class Input:
    def __init__(self, parent, item, row, type_):
        self._parent = parent
        self._item = item
        self._type = type_
        self._row = row
        self._init_elements()

    def _init_elements(self):
        attrib = self._item.attrib
        self._label = tk.Label(self._parent, text=attrib["label"])
        self._entryvar = tk.StringVar()
        self._entry = tk.Entry(self._parent, textvariable=self._entryvar)

        self._label.grid(column=1, row=self._row, sticky=tk.E)
        self._entry.grid(column=2, row=self._row)

    def destroy(self):
        self._label.destroy()
        self._entry.destroy()

    def get(self):
        self._entryvar.get()

    def set_query(self):
        if not self._validate():
            self._label.config(fg="#c00")
            return ValueError
        else:
            self._label.config(fg="#000")
        query = self._parent.get_query()
        if self._type == "search-data":
            query.update_constraint(
                self._item.attrib["field"], self._item.attrib["table"], self.get(),
            )
        else:
            query.update_data(
                self._item.attrib["field"], self._item.attrib["table"], self.get(),
            )
        return None

    def _validate(self):
        return True


class Entry(Input):
    pass


class PhoneNum(Input):
    def _validate(self):
        text = self._entryvar.get()
        # \+? -- The number may start with a plus
        # ((\(?\d+\)?)(-|\s+))+ -- It is followed by at least one:
        #     (\(?\d+\)?)? -- Maybe some digits which might be in brackets
        #     (-|\s+) -- a hyphen or some whitespace
        # e.g.
        #   +44 1865 242191
        #   01865 253432
        #   +1 (201) 4132-7351
        #   +389-326-385-0068
        if re.match(r"^\+?((\(?\d+\)?)?(-|\s+)?)+$", text):
            return True
        else:
            return super()._validate()


class Email(Input):
    def _validate(self):
        # The only way to validate an email without sending a confirmation
        # message or excluding valid emails.
        return "@" in self._entryvar.get()


class Radio(Input):
    def _init_elements(self):
        attrib = self._item.attrib
        self._label = tk.Label(self._parent, text=attrib["label"])
        self._entryvar = tk.StringVar()
        self._label.grid(row=self._row, column=0)
        column = 1
        self._radios = []
        for item in self._item:
            value = item.attrib["value"]
            radio = tk.Radiobutton(
                self._parent, text=item.text, variable=self._entryvar, value=value,
            )
            radio.grid(row=self._row, column=column)
            self._radios.append(radio)
            column += 1

    def get(self):
        value = self._entryvar.get()
        dtype = self._item.attrib["dtype"]
        if dtype == "int":
            try:
                value = int(value)
            except ValueError:
                value = 0
        elif dtype == "bool":
            value = value == "True"
        elif dtype == "float":
            value = float(value)
        return value

    def destroy(self):
        self._label.destroy()
        for radio in self._radios:
            radio.destroy()


class Date(Input):
    def _init_elements(self):
        attrib = self._item.attrib
        self._label = tk.Label(self._parent, text=attrib["label"])
        self._label.grid(row=self._row, column=0)
        self._entryvar = tk.StringVar()
        self._calendar = tkcalendar.Calendar(
            self._parent,
            year=2023,
            month=1,
            day=1,
            date_pattern="y-mm-dd",
            variable=self._entryvar,
        )
        self._calendar.grid(row=self._row, column=1, pady=10, padx=10)

    def get(self):
        return self._calendar.get_date()

    def destroy(self):
        self._label.destroy()
        self._calendar.destroy()


class Custom(Input):
    def _init_elements(self):
        return

    def set_query(self):
        query = self._parent.get_query()
        query.add_custom_constraint(self._item.text)

    def destroy(self):
        return


class Link(Input):
    def _init_elements(self):
        return

    def set_query(self):
        query = self._parent.get_query()
        table1 = self._item[0].attrib["table"]
        field1 = self._item[0].attrib["field"]
        table2 = self._item[1].attrib["table"]
        field2 = self._item[1].attrib["field"]

        query.add_link(field1, field2, table1, table2)

    def destroy(self):
        return


class Data(Input):
    def _init_elements(self):
        return

    def set_query(self):
        query = self._parent.get_query()
        table = self._item.attrib["table"]
        field = self._item.attrib["field"]

        query.update_data(field, table)

    def destroy(self):
        return


class SubmitButton(gui.templates.Button):
    def _get_text(self):
        return "Submit"

    def _command(self):
        self._parent.submit_query()
