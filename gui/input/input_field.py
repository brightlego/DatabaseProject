"""Deals with the input box"""

import tkinter as tk
import tkcalendar

import gui.templates
import re


class InputField(gui.templates.Page):
    """The field where all input happens

    Inherits from gui.templates.Page

    Attributes:
        Private:
            __query (backend.query.Query)
                -- The query for querying
            __template
                -- The template of the inputfield

        Tkinter Widgets:
            __searchdata (gui.input.input_field.SearchData)
                -- The search data box
            __setdata (gui.input.input_field.SetData)
                -- The set data box
            __optionalbox (gui.input.input_field.OptionalBox)
                -- The optional data box
            __elements (list[gui.input.input_field.Input])
                -- The input elements of the input field
            __title (tkinter.Label)
                -- The title of the input field

    Methods:
        Overridden:
            _init_elements() -> None
        Public:
            set_template(template: xml.etree.ElementTree) -> None
                -- Sets the template to template
            get_query() -> backend.query.Query
                -- Accessor method for __query
            set_query() -> list[Exception]
                -- Sets the query to the data and returns the errors
                   encountered in the process.
            submit_query() -> None
                -- Submits the query for execution
        Private:
            __check_empty_widgets() -> None
                -- Checks if the widgets are empty and hides them if so
            __set_elements(parent: gui.templates.Page,
                           root: xml.etree.ElementTree.Element,
                           tag: str,
                           mode:str="vertical",
                           row:int=1)
                -- Sets the elements within root to widgets
            __add_item(parent: gui.templates.Page,
                       item: xml.etree.ElementTree.Element,
                       row: int,
                       column: int,
                       root: xml.etree.ElementTree.Element,
                       tag:str=None)
                -- Adds a widget
    """

    def _init_elements(self):
        """Initilises the Elements

        Arguments:
            None

        Returns:
            None
        """

        # Create the variables and widgets
        self.__searchdata = SearchData(self)
        self.__setdata = SetData(self)
        self.__optionalbox = OptionalBox(self.__searchdata)
        self.__elements = []
        self.__title = tk.Label(self)
        self.__query = None
        self.__submit_button = SubmitButton(self)
        self.__template = None

        # Grid them
        self.__title.grid(column=0, row=0)
        self.__searchdata.grid(column=0, columnspan=3, row=1, pady=5)
        self.__setdata.grid(column=0, columnspan=3, row=2, pady=5)
        self.__submit_button.grid(column=1000, row=3)
        self.__optionalbox.grid(column=1, columnspan=100, row=100, pady=2)

        # Hide the empty widgets
        self.__check_empty_widgets()

    def set_template(self, template):
        """Sets the template to template

        Arguments:
            template (xml.etree.ElementTree.Element)
                -- The template to set to

        Returns:
            None
        """

        self.__template = template

        # Destroy all existing elements
        for item in self.__elements:
            item.destroy()
        self.__elements = []

        # Get the root and set the title
        root = template.getroot()
        self.__title["text"] = root.attrib["title"]

        # Delete the old query and generate a new one
        del self.__query
        self.__query = self._parent.gen_new_query(root.attrib["type"])

        # Iterate through the items in the root
        for item in root:
            if item.tag == "search-data":
                self.__set_elements(self.__searchdata, item, item.tag)

            elif item.tag == "set-data":
                self.__set_elements(self.__setdata, item, item.tag)

            elif item.tag == "constraints":
                self.__set_elements(self, item, item.tag)

        # Hide the empty widgets
        self.__check_empty_widgets()

    def __check_empty_widgets(self):
        """Checks if the widgets are empty and hides them if they are

        Arguments:
            None

        Returns:
            None
        """

        # If the search data is empty, hide it. Otherwise show it.
        if self.__searchdata.is_empty():
            self.__searchdata.hide()
        else:
            self.__searchdata.show()

        # If the set data is empty, hide it. Otherwise show it.
        if self.__setdata.is_empty():
            self.__setdata.hide()
        else:
            self.__setdata.show()

        # If the optional data is empty, hide it. Otherwise show it.
        if self.__optionalbox.is_empty():
            self.__optionalbox.hide()
        else:
            self.__optionalbox.show()

    def __set_elements(self, parent, root, tag, mode="vertical", row=1):
        """Sets the elements in the input field

        Arguments:
            parent (gui.templates.Page)
                -- The parent to this InputField
            root (xml.etree.ElementTree.Element)
                -- The root which is iterated through
            tag (str)
                -- The tag of the root
            mode (str) default "vertical"
                -- The mode of whether to grid it.
            row (int) default 1
                -- The starting row

        Returns:
            None
        """
        # Set the column to 0
        column = 0

        # Iterate through all the children of the root
        for item in root:

            # If it switches to horizontal mode, parse it horizontally
            if item.tag == "horizontal":
                # Add the label
                self.__elements.append(Label(parent, item, row, column, tag))

                # Recursion!
                self.__set_elements(parent, item, tag, mode="horizontal", row=row)
            # The optional tag
            elif item.tag == "optional":

                # More Recursion!
                self.__set_elements(self.__optionalbox, item, item.tag)
            else:
                # Otherwise, add that item to the elements
                self.__add_item(parent, item, row, column, root, tag)

            # If in vertical mode, increment row
            if mode == "vertical":
                row += 1

            # Otherwise increment column by 10 (for safe measure)
            else:
                column += 10

    def get_query(self):
        """Accessor method for __query"""
        return self.__query

    def __add_item(self, parent, item, row, column, root, tag=None):
        """Adds a widget to the input field

        Arguments:
            parent (gui.templates.Page)
                -- The parent to the items
            item (xml.etree.ElementTree.Element)
                -- The item that is being added
            row (int)
                -- The row of the item
            column (int)
                -- The column of the item
            root (xml.etree.ElementTree.Element)
                -- The root XML tag

        Keyword Arguments:
            tag (str) default None
                -- The tag of the root element used in figuring out what the
                   element is part of.

        Returns:
            None
        """

        # If the tag is the default value, set it to the tag of the root
        if tag is None:
            tag = root.tag

        # This is basically a match statement but ifs and elifs because this
        # is made in python 3.8 and designed to be compatible with 3.6 and
        # match was introduced in 3.10
        if item.tag == "entry":
            self.__elements.append(Entry(parent, item, row, column, tag))
        elif item.tag == "phone":
            self.__elements.append(PhoneNum(parent, item, row, column, tag))
        elif item.tag == "email":
            self.__elements.append(Email(parent, item, row, column, tag))
        elif item.tag == "radio":
            self.__elements.append(Radio(parent, item, row, column, tag))
        elif item.tag == "date":
            self.__elements.append(Date(parent, item, row, column, tag))
        elif item.tag == "link":
            self.__elements.append(Link(parent, item, row, column, tag))
        elif item.tag == "get-data":
            self.__elements.append(Data(parent, item, row, column, tag))
        elif item.tag == "checkbox":
            self.__elements.append(Checkbox(parent, item, row, column, tag))
        elif item.tag == "number":
            self.__elements.append(Number(parent, item, row, column, tag))
        elif item.tag == "custom-constraint":
            self.__elements.append(CustomConstraint(parent, item, row, column, tag))
        elif item.tag == "custom-select":
            self.__elements.append(CustomSelect(parent, item, row, column, tag))
        elif item.tag == "custom-tail":
            self.__elements.append(CustomTail(parent, item, row, column, tag))

    def set_query(self):
        """Sets the query and returns errors if they are encountered

        Arguments:
            None
        Returns:
            errors (list[Exception])
                -- The errors that had been encountered
        """
        errors = []

        # Iterate through the errors
        for element in self.__elements:
            new_error = element.set_query()

            # If an error had happened, added to errors
            if new_error is not None:
                errors.append(new_error)
        return errors

    def submit_query(self):
        """Submits a query for execution

        Arguments:
            None

        Returns:
            None
        """

        # Set the query and get any errors that have happened
        errors = self.set_query()

        # If there are errors, abort!
        if errors:
            return

        # Submit the query to the parent
        self._parent.submit_query(self.__query)

        # Reset the input field
        self.set_template(self.__template)


class SearchData(gui.templates.HollowPage, gui.templates.HideablePage):
    """The box which holds the data to seach

    Inherits from gui.tempates.HollowPAte then gui.templates.HideablePage

    Attributes:
        None

    Methods:
        is_empty() -> bool
            -- Is the box empty?
    """

    def is_empty(self):
        """Returns true if the box is empty

        Arguments:
            None

        Returns:
            is_empty (bool)
                -- Whether the box is empty
        """
        # If there is 1 child and that child is an optionalbox
        if len(self.winfo_children()) == 1 and isinstance(
            self.winfo_children()[0], OptionalBox
        ):
            # Return true if that box is empty, otherwise return false
            return self.winfo_children()[0].is_empty()

        # Otherwise, return if there are no elements in this box
        return len(self.winfo_children()) == 0


class SetData(gui.templates.HollowPage, gui.templates.HideablePage):
    """The box which holds the data to seach

    Inherits from gui.tempates.HollowPAte then gui.templates.HideablePage

    Attributes:
        None

    Methods:
        Public:
            is_empty() -> bool
                -- Is the box empty?
    """

    def is_empty(self):
        """Returns true if the box is empty

        Arguments:
            None

        Returns:
            Public:
                is_empty (bool)
                    -- Whether the box is empty
        """

        # Return true if there are no children in this box
        return len(self.winfo_children()) == 0


class OptionalBox(gui.templates.HollowPage, gui.templates.HideablePage):
    """The box which holds the data to seach

    Inherits from gui.tempates.HollowPAte then gui.templates.HideablePage

    Attributes:
        None

    Methods:
        Overridden:
            _init_elements() -> None
        Public:
            is_empty() -> bool
                -- Is the box empty?
    """

    def _init_elements(self):
        """Initiates the elements in the box"""
        self.__label = tk.Label(self, text="Pick Any:")
        self.__label.grid(column=0, columnspan=10, row=0)

    def is_empty(self):
        """Returns true if the box is empty

        Arguments:
            None

        Returns:
            is_empty (bool)
                -- Whether the box is empty
        """
        # Return true if there is only the label in the box
        return len(self.winfo_children()) <= 1


class Input:
    """An input field

    It does not inherit from gui.templates.Page because then the labels and
    boxes can line up in the input field.

    Attributes:
        Protected:
            _parent (gui.templates.Page)
                -- The parent to this input
            _item (xml.etree.ElementTree.Element)
                -- The item this input represents
            _type (str)
                -- The tag of the parent node.
            _row (int)
                -- The row of the input field
            _column (int)
                -- The column of the input field
            _entryvar (tkinter.StringVar)
                -- The variable used in _entry
        Tkinter Widgets:
            _entry (tkinter.Entry)
                -- The entry box
            _label (tkinter.Label)
                -- The label to the entry box

    Methods:
        Magic:
            __init__(self,
                     parent: gui.templates.Page,
                     item: xml.etree.ElementTree.Element,
                     row: int,
                     column: int,
                     type_: str) -> None
        Overridden:
            _init_elements() -> None
        Public:
            destroy() -> None
                -- Destroys the elemnts in the input
            get() -> str
                -- Gets the value of the string
            set_query() -> Exception
                -- Sets the query
        Protected:
            _validate() -> bool
                -- Checks if the input is valid

    """

    def __init__(self, parent, item, row, column, type_):
        """The constructor for Input

        Arguments:
            parent (gui.templates.Page)
                -- The parent element
            item (xml.etree.ElementTree.Element)
                -- The item which this is an input from
            row (int)
                -- The row of the input
            column (int)
                -- The column of the input
        """

        # Remember the arguments
        self._parent = parent
        self._item = item
        self._type = type_
        self._row = row
        self._column = column

        # Initiate the elements
        self._init_elements()

    def _init_elements(self):
        """Initiates the elements of Input

        Arguments:
            None
        Returns:
            None
        """
        # Get the attributes of the item.
        attrib = self._item.attrib

        # The variable of the input
        self._entryvar = tk.StringVar()

        # Create a label for the input
        self._label = tk.Label(self._parent, text=attrib["label"])

        # Create an entry box for the input
        self._entry = tk.Entry(self._parent, textvariable=self._entryvar)

        # Grid them
        self._label.grid(column=self._column + 1, row=self._row, sticky=tk.E)
        self._entry.grid(column=self._column + 2, row=self._row)

    def destroy(self):
        """Destroys the input

        Arguments:
            None

        Returns:
            None
        """
        # Destroy the label and the entry box
        self._label.destroy()
        self._entry.destroy()

    def get(self):
        """Relay for _entryvar

        Arguments:
            None

        Returns:
            value (str)
                -- The value in _entryvar
        """
        return self._entryvar.get()

    def set_query(self):
        """Sets the query

        Arguments:
            None

        Returns:
            err (Exception)
                -- Any errors encountered
        """
        # There is no error by default
        err = None

        # If the validation fails
        if not self._validate():
            # Change the label colour to red and add an error
            self._label.config(fg="#c00")
            err = ValueError()
        else:
            # Otherwise make the label black
            self._label.config(fg="#000")

        # Get the query from the parent
        query = self._parent.get_query()

        # if get is None (it should never be) return the error
        if self.get() is None:
            return err

        # If this is in a search-data box
        if self._type == "search-data":
            # If self.get is empty set the label to red and add an error
            if self.get() == "":
                self._label.config(fg="#c00")
                err = ValueError()
            # Otherwise set the label to black
            else:
                self._label.config(fg="#000")

            # Add the relevent constraint to the query
            query.update_constraint(
                self._item.attrib["field"], self._item.attrib["table"], self.get(),
            )

        # If the Input is in an OptionalBox
        elif self._type == "optional":

            # If self.get() is empty, return any errors encountered but don't
            # add a new one
            if self.get() == "":
                return err
            # Otherwise, add the relevent constraint
            else:
                query.update_constraint(
                    self._item.attrib["field"], self._item.attrib["table"], self.get(),
                )
        # If the Input is in a Search Box
        else:
            # If self.get is empty set the label to red and add an error
            if self.get() == "":
                self._label.config(fg="#c00")
                err = ValueError()
            # Otherwise set the label to black
            else:
                self._label.config(fg="#000")

            # Add the relevent data to the query
            query.update_data(
                self._item.attrib["field"], self._item.attrib["table"], self.get(),
            )
            # If the entry is empty
            if self.get() == "":
                self._label.config(fg="#c00")
                err = ValueError()
            else:
                self._label.config(fg="#000")
        # Return any errors encountered
        return err

    def _validate(self):
        """Validates the input.

        Arguments:
            None

        Returns:
            is_valid (bool)
                -- whether the input is valid
        """

        # All possible inputs to the basic input are valid
        return True


class Entry(Input):
    """The basic entry widget. Inherits all from Input"""

    pass


class Label(Input):
    """A label. It does not have an entry.

    Methods:
        Overridden:
            _init_elements() -> None
            get() -> str
            set_query() -> None
            destroy() -> None
    """

    def _init_elements(self):
        """Initilises the elements.

        Arguments:
            None
        Returns:
            None
        """

        # Get the attributes of the XML item
        attrib = self._item.attrib

        # Create a label
        self._label = tk.Label(self._parent, text=attrib["label"])

        # Grid it
        self._label.grid(column=self._column + 1, row=self._row, sticky=tk.E)

    def get(self):
        """Gets the relevent data"""

        # There is no relevent data
        pass

    def set_query(self):
        """Sets the query"""

        # This does not affect the query
        pass

    def destroy(self):
        """Destroys all the elements in the label"""
        # Destroy the label
        self._label.destroy()


class PhoneNum(Input):
    """A phone number input field.

    Inherits from Input

    Methods:
        Overriden:
            _validate() -> bool
    """

    def _validate(self):
        """Validates the input box.

        Arguments:
            None

        Returns:
            is_valid (bool)
                -- Whether the phone number is valid
        """
        # Get the text
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

        # If the regular expression matches return True
        if re.match(r"^\+?((\(?\d+\)?)?(-|\s+)?)+$", text):
            return True
        # If there is other text return False
        elif text:
            return False
        # If it is empty return True
        else:
            return True


class Email(Input):
    """An email input field.

    Inherits from Input

    Methods:
        Overriden:
            _validate() -> bool
    """

    def _validate(self):
        """Validates the input box.

        Arguments:
            None

        Returns:
            is_valid (bool)
                -- Whether the phone number is valid
        """
        # The only way to validate an email without sending a confirmation
        # message or excluding valid emails.

        # Return true if and only if it is either empty or there is an @
        return "@" in self._entryvar.get() or self._entryvar.get() == ""


class Number(Input):
    """An email input field.

    Inherits from Input

    Methods:
        Overriden:
            _validate() -> bool
    """

    def _validate(self):
        """Validates the input box.

        Arguments:
            None

        Returns:
            is_valid (bool)
                -- Whether the phone number is valid
        """
        # Return true if and only if it is either empty or there are only
        # digits
        return self._entryvar.get().isnumeric() or self._entryvar.get() == ""


class Radio(Input):
    """A radio button input field.

    Attributes:
        Protected:
            _radios (list[tkinter.RadioButton])
                -- The Radio Buttons
    Methods:
        Overridden:
            _init_elements() -> None
            get() -> str
            destroy() -> None
    """

    def _init_elements(self):
        """Initilises the elements

        Arguments:
            None

        Returns:
            None
        """

        # Get the attributes
        attrib = self._item.attrib

        # The variable in use
        self._entryvar = tk.StringVar()

        # Create the label for the radio button
        self._label = tk.Label(self._parent, text=attrib["label"])

        # Grid it
        self._label.grid(row=self._row, column=self._column)

        # Start at column the column + 1 (1 for the label)
        column = self._column + 1
        self._radios = []

        # For each child of _item
        for item in self._item:

            # Get the value
            value = item.attrib["value"]

            # Create the radiobutton
            radio = tk.Radiobutton(
                self._parent, text=item.text, variable=self._entryvar, value=value,
            )

            # Grid it
            radio.grid(row=self._row, column=column)

            # Append it to _radios
            self._radios.append(radio)

            # Increment the column
            column += 1

    def get(self):
        """Gets the data in the radio

        Arguments:
            None

        Returns:
            value (str)
                -- The data in the radio
        """

        # Get the value and the datatype
        value = self._entryvar.get()
        dtype = self._item.attrib["dtype"]

        # If the datatype is an int, convert it to an int but default to 0
        if dtype == "int":
            try:
                value = int(value)
            except ValueError:
                value = 0

        # If the data type is bool, check if it is the literal "true"
        elif dtype == "bool":
            value = value.lower() == "true"

        # If the data type is float, convert it to a float but default to 0
        elif dtype == "float":
            try:
                value = float(value)
            except ValueError:
                value = 0.0

        # Otherwise don't change it
        return value

    def destroy(self):
        """Destroys the elements inside this Input.

        Arguments:
            None

        Returns:
            None
        """
        # Destroy the label
        self._label.destroy()

        # Destroy all the radio buttons
        for radio in self._radios:
            radio.destroy()


class Date(Input):
    """A Date input box

    Attributes:
        _calendar (tkcalendar.Calendar)
            -- The calendar

    Methods:
        Overridden:
            _init_elements() -> None
            get() -> str
            destroy() -> None
    """

    def _init_elements(self):
        """Constructor for Date

        Arguments:
            None

        Returns:
            None
        """
        # Get the attributes of the XML item
        attrib = self._item.attrib

        # Create and grid the label
        self._label = tk.Label(self._parent, text=attrib["label"])
        self._label.grid(row=self._row, column=self._column + 1)

        # The variable used to store the data in the calendar
        self._entryvar = tk.StringVar()

        # The calendar
        self._calendar = tkcalendar.Calendar(
            self._parent,
            year=2023,  # Start at 2023-01-01
            month=1,
            day=1,
            date_pattern="y-mm-dd",  # Actually yyyy-mm-dd
            variable=self._entryvar,
        )
        # Grid the calendar
        self._calendar.grid(row=self._row, column=self._column + 2, pady=10, padx=10)

    def get(self):
        """gets the data of the calendar

        Arguments:
            None

        Returns:
            date (str)
                -- The date as specified by the calendar
        """
        return self._calendar.get_date()

    def destroy(self):
        """Destroys the Input box

        Arguments:
            None
        Returns:
            None
        """
        # Destroy the label
        self._label.destroy()

        # Destory the calendar
        self._calendar.destroy()


class Checkbox(Input):
    """Check box input fields.

    Methods:
        Overridden:
            _init_elements() -> None
            destroy() -> None
            get() -> str
    """

    def _init_elements(self):
        """Initilises the elements inside the Input

        Arguments:
            None
        Returns:
            None
        """
        # Get the attributes
        attrib = self._item.attrib

        # The variable attached to the tickbox (1 is ticked, 0 is unticked)
        self._entryvar = tk.IntVar()

        # The label
        self._label = tk.Label()

        # The tick box
        self._entry = tk.Checkbutton(
            self._parent, text=attrib["label"], variable=self._entryvar
        )

        # Grid it
        self._entry.grid(column=self._column + 2, row=self._row)

    def destroy(self):
        """Destroys the entry.

        Attributes:
            None
        Returns:
            None
        """
        # Destroy the entry
        self._entry.destroy()

    def get(self):
        """Gets the data if the entrybox has been ticked

        Arguments:
            None
        Returns:
            value (str)
                -- The value of the input box
        """

        # Get whether it is checked
        is_checked = bool(self._entryvar.get())

        # If it has been checked, set value to the appropriate value
        if is_checked:
            value = self._item.attrib["tickedvalue"]
        # Otherwise give it the default value
        else:
            value = self._item.attrib["defaultvalue"]

        # Get the dtype of the value (default string)
        try:
            dtype = self._item.attrib["dtype"]
        except KeyError:
            dtype = "str"

        # If the datatype is int, make it an int default 0
        if dtype == "int":
            try:
                value = int(value)
            except ValueError:
                value = 0

        # If it is a bool, check if it is the literal "true"
        elif dtype == "bool":
            value = value.lower() == "true"

        # If it is a float, make it a float default 0.0
        elif dtype == "float":
            try:
                value = float(value)
            except ValueError:
                value = 0.0

        # Otherwise, keep it a string
        return value


class CustomConstraint(Input):
    """A custom constraint.

    Methods:
        Overridden:
            _init_elements() -> None
            set_query() -> None
            destroy() -> None
    """

    def _init_elements(self):
        """Intilise the elements

        Arguments:
            None

        Returns:
            None
        """
        pass

    def set_query(self):
        """Sets the query.

        Arguments:
            None

        Returns:
            None
        """
        # Get the query and add a custom constraint on what is inside the tag
        query = self._parent.get_query()
        query.add_custom_constraint(self._item.text)

    def destroy(self):
        """Destroys all the non-existant elements inside the input

        Arguments:
            None

        Returns:
            None
        """
        pass


class CustomSelect(Input):
    """A custom select.

    Methods:
        Overridden:
            _init_elements() -> None
            set_query() -> None
            destroy() -> None
    """

    def _init_elements(self):
        """Intilise the elements

        Arguments:
            None

        Returns:
            None
        """
        pass

    def set_query(self):
        """Sets the query.

        Arguments:
            None

        Returns:
            None
        """
        # Get the query and add a custom select on what is inside the tag
        query = self._parent.get_query()
        query.add_custom_select(self._item.attrib["label"], self._item.text)

    def destroy(self):
        """Destroys all the non-existant elements inside the input

        Arguments:
            None

        Returns:
            None
        """
        pass


class CustomTail(Input):
    """A custom constraint.

    Methods:
        Overridden:
            _init_elements() -> None
            set_query() -> None
            destroy() -> None
    """

    def _init_elements(self):
        """Intilise the elements

        Arguments:
            None

        Returns:
            None
        """
        pass

    def set_query(self):
        """Sets the query.

        Arguments:
            None

        Returns:
            None
        """
        # Get the query and add a custom tail on what is inside the tag
        query = self._parent.get_query()
        query.add_custom_tail(self._item.text)

    def destroy(self):
        """Destroys all the non-existant elements inside the input

        Arguments:
            None

        Returns:
            None
        """
        pass


class Link(Input):
    """Links (otherwise known as joins) two tables together

    Methods:
        Overridden:
            _init_elements() -> None
            set_query() -> None
            destroy() -> None
    """

    def _init_elements(self):
        """Intilise the elements

        Arguments:
            None

        Returns:
            None
        """
        pass

    def set_query(self):
        """Sets the query.

        Arguments:
            None

        Returns:
            None
        """

        # Get the Query and the relevent attributes from the _item
        query = self._parent.get_query()
        table1 = self._item[0].attrib["table"]
        field1 = self._item[0].attrib["field"]
        table2 = self._item[1].attrib["table"]
        field2 = self._item[1].attrib["field"]

        # Add the link based on these attributes
        query.add_link(field1, field2, table1, table2)

    def destroy(self):
        """Destroys all the non-existant elements inside the input

        Arguments:
            None

        Returns:
            None
        """
        pass


class Data(Input):
    """Sets which data fields to get.

    Methods:
        Overridden:
            _init_elements() -> None
            set_query() -> None
            destroy() -> None
    """

    def _init_elements(self):
        """Intilise the elements

        Arguments:
            None

        Returns:
            None
        """
        pass

    def set_query(self):
        """Sets the query.

        Arguments:
            None

        Returns:
            None
        """
        query = self._parent.get_query()
        table = self._item.attrib["table"]
        field = self._item.attrib["field"]

        query.update_data(field, table)

    def destroy(self):
        """Destroys all the non-existant elements inside the input

        Arguments:
            None

        Returns:
            None
        """
        pass


class SubmitButton(gui.templates.Button):
    """The button used when submitting a query

    Inherits from gui.templates.Button

    Methods:
        Overridden:
            _get_text() -> str
            _command() -> None
    """

    def _get_text(self):
        """Gets the text displayed on the button.

        Arguments:
            None
        Returns:
            text (str)
                -- The text displayed on the button
        """
        return "Submit"

    def _command(self):
        """The command that is run when the button is pressed

        Arguments:
            None

        Returns:
            None
        """

        # Submits the query
        self._parent.submit_query()
