"""The file which contains the query objects"""

import copy

from backend.sqlescape import escape


class Query:
    """The base query object

    Attributes:
        Protected:
            _tables (set[str])
                -- The tables in use
            _fields (dict[str:list[str]])
                -- The fields of those tables
            _data (dict[str:Any])
                -- The data used in SELECT * FROM or (...) VALUES (...) etc.
            _constraints (dict[str:any])
                -- The constraints used after WHERE
            _custom_constraints (list[str])
                -- Any custom constraints
            _custom_select (list[str])
                -- Any custom between SELECT and FROM
            _custom_tail (list[str])
                -- Any custom after the WHERE
            _links (dict[str:str])
                -- Links between tables
            _order_by (str)
                -- What to order by
            _order_asc (bool)
                -- Whether to order ascending
            _limit (int)
                -- What the limit to ordering is

    Methods:
        Magic:
            __init__(order_by:str=None, order_asc:bool=True, limit:int=1)
        Public:
            update_constraint(field: str, table: str, value: any) -> None
                -- Updates a constraint
            add_link(field1: str, field2: str, table1: str, table2: str) -> None
                -- Adds a link between two tables
            add_custom_constraint(constraint: str) -> None
                -- Adds a custom constraint
            add_custom_select(field: str, get_text: str) -> None
                -- Adds a custom select
            add_custom_tail(tail: str) -> None
                -- Adds a custom tail
            update_data(field: str, table: str, value:Any=None) -> None
                -- Updates the data
            generate_query() -> (str, list[Any])
                -- Generates the query
            get_fields() -> dict[str:list[str]]
                -- Gets the fields used
            execute(conn: sqlite3.Connection) -> sqlite3.Cursor
                -- Executes the query
            changed_db() -> bool
                -- Whether the query has changed the database
        Protected:
            _gen_data_query() -> str
                -- Generates the data part of the query
            _gen_constraint_query() -> str
                -- Generates the constraint part of the query
            _gen_table_query() -> str
                -- Generates the table part of the query
            _gen_tail() -> str
                -- Generates the tail of the query
    """

    def __init__(self, order_by=None, order_asc=True, limit=1):
        """The constructor for Query

        Arguments:
            None

        Keyword Arguments:
            order_by (str) default None
                -- What to order by
            order_asc (bool) default True
                -- Whether to order ascending
            limit (int) default 1
                -- What the limit should be

        Returns None
        """

        # Initilise the various attributes
        self._tables = set()
        self._fields = {}
        self._data = {}
        self._constraints = {}

        self._custom_constraints = []
        self._custom_select = []
        self._custom_tail = []

        self._links = {}

        self._order_by = order_by
        self._order_asc = order_asc
        self._limit = limit

    def update_constraint(self, field, table, value):
        """Updates a constraint for a table, field pair

        Arguments:
            field (str)
                -- The field
            table (str)
                -- The table
            value (Any)
                -- The value

        Returns:
            None
        """
        self._constraints[f"{escape(table)}.{escape(field)}"] = value
        self._tables.add(table)

    def add_link(self, field1, field2, table1, table2):
        """Adds a link between two tables

        Arguments:
            field1 (str)
                -- The first field
            field2 (str)
                -- The second field
            table1 (str)
                -- The  first table
            table2 (str)
                -- The  second table

        Returns:
            None
        """
        # Make sure to escape!
        self._links[
            f"{escape(table1)}.{escape(field1)}"
        ] = f"{escape(table2)}.{escape(field2)}"
        self._tables.add(table1)
        self._tables.add(table2)

    def add_custom_constraint(self, constraint):
        """Adds a custom constraint

        Arguments:
            constraint (str)
                -- The constraint to add

        Returns:
            None
        """
        self._custom_constraints.append(constraint)

    def add_custom_select(self, field, get_text):
        """Adds a custom select

        Arguments:
            field (str)
                -- The name of the field it is selecting for table purposes
            get_text (str)
                -- The select text to add

        Returns:
            None
        """
        self._custom_select.append((field, get_text))

    def add_custom_tail(self, tail):
        """Adds a custom tail

        Arguments:
            tail (str)
                -- The tail to add

        Returns:
            None
        """
        self._custom_tail.append(tail)

    def update_data(self, field, table, value=None):
        """Updates the data for a table, field pair

        Arguments:
            field (str)
                -- The field
            table (str)
                -- The table

        Keyword Arguments
            value (Any) default None
                -- The value

        Returns:
            None
        """

        # If the value is none, add it to _fields
        if value is None:
            if table in self._fields:
                self._fields[table].append(field)
            else:
                self._fields[table] = [field]

        # Otherwise add it to _data
        self._data[f"{escape(table)}.{escape(field)}"] = value
        self._tables.add(table)

    def _gen_data_query(self):
        """Generates the data part of the query

        Arguments:
            None

        Returns:
            text (str)
                -- The data part of the query
        """
        pass

    def _gen_constraint_query(self):
        """Generates the constraint part of the query

        Arguments:
            None

        Returns:
            text (str)
                -- The constraint part of the query
        """
        out = []

        # Add WHERE {field} = ? for each field
        for field in self._constraints:
            out.append(f"{field}=?")

        # Add WHERE {link1} = {link2} for each link
        for field in self._links:
            out.append(f"{field}={self._links[field]}")

        # Add the custom constraints
        for constraint in self._custom_constraints:
            out.append(f"({constraint})")

        # Join the outputs with an AND statement
        out = " AND ".join(out)
        if out:
            out = "WHERE " + out
        return out

    def _gen_table_query(self):
        """Generates the table part of the query

        Arguments:
            None

        Returns:
            text (str)
                -- The table part of the query
        """
        out = []
        # Add the escaped table for each of the tables
        for table in self._tables:
            out.append(escape(table))
        return ",".join(out)

    def generate_query(self):
        """Generates the query

        Arguments:
            None

        Returns:
            qtext (str)
                -- The query text
            params (list[Any])
                -- The parameters of the query
        """
        return "", []

    def _gen_tail(self):
        """Generates the tail part of the query

        Arguments:
            None

        Returns:
            text (str)
                -- The tail part of the query
        """
        return " ".join(self._custom_tail)

    def get_fields(self):
        """Accessor method for _fields"""
        return None

    def execute(self, conn):
        """Executes a query

        Arguments:
            conn (sqlite3.Connection)
                -- The connection to the database

        Returns:
            result (sqlite3.Cursor)
                -- The result of executing the query
        """
        qtext, param = self.generate_query()
        return conn.execute(qtext, param)

    def changed_db(self):
        """Whether the query has changed the database

        Arguments:
            None

        Returns:
            has_changed_db (bool)
                -- Whether the query has changed the database
        """
        return True


class NullQuery(Query):
    """This query does nothing.

    Inherits from Query
    """

    def update_constraint(self, field, table, value):
        """Does nothing"""
        pass

    def add_link(self, field1, field2, table1, table2):
        """Does nothing"""
        pass

    def add_custom_constraint(self, constraint):
        """Does nothing"""
        pass

    def add_custom_select(self, field, get_text):
        """Does nothing"""
        pass

    def update_data(self, field, table, value=None):
        """Does nothing"""
        pass

    def generate_query(self):
        """Does nothing"""
        return "", []

    def changed_db(self):
        """It did not change the database"""
        return False


class AddQuery(Query):
    """A query for addition

    Methods:
        Overridden:
            _gen_data_query() -> str
            update_data(field: str, table: str, value: Any) -> None
            generate_data() -> (str, list[Any])
    """

    def _gen_data_query(self):
        """Generates the data part of the query

        Arguments:
            None

        Returns:
            text (str)
                -- The data part of the query
        """

        # Generate the fields and the values
        fields = []
        values = []
        for field in self._data:
            fields.append(field)
            values.append("?")

        fields = ",".join(fields)
        values = ",".join(values)

        return f"({fields}) VALUES ({values})"

    def update_data(self, field, table, value=None):
        """Updates the data for a table, field pair

        Arguments:
            field (str)
                -- The field
            table (str)
                -- The table

        Keyword Arguments
            value (Any) default None
                -- The value

        Returns:
            None
        """
        self._data[f"{escape(field)}"] = value
        self._tables.add(table)

    def generate_query(self):
        # Standard INSERT INTO query
        text = f"""INSERT INTO
            {self._gen_table_query()}
            {self._gen_data_query()}
            {self._gen_tail()}"""

        params = []
        for field in self._data:
            params.append(self._data[field])

        return text, params


class GetQuery(Query):
    """A query for getting data

    Methods:
        Overridden:
            _gen_data_query() -> str
            update_data(field: str, table: str, value: Any) -> None
            generate_data() -> (str, list[Any])
    """

    def __init__(self, order_by=None, order_asc=True, limit=1000):
        super().__init__(order_by=order_by, order_asc=order_asc, limit=limit)

    def get_fields(self):
        """Accessor method for _fields"""
        fields = copy.deepcopy(self._fields)
        fields[" "] = []
        for field, _ in self._custom_select:
            fields[" "].append(field)
        return fields

    def _gen_data_query(self):
        """Generates the data part of the query

        Arguments:
            None

        Returns:
            text (str)
                -- The data part of the query
        """
        fields = []
        for table in self._fields:
            for field in self._fields[table]:
                fields.append(f"{escape(table)}.{escape(field)}")

        for _, get_text in self._custom_select:
            fields.append(get_text)

        fields = ",".join(fields)
        return fields

    def generate_query(self):
        """Generates the query

        Arguments:
            None

        Returns:
            qtext (str)
                -- The query text
            params (list[Any])
                -- The parameters of the query
        """
        text = f"""
            SELECT {self._gen_data_query()}
            FROM {self._gen_table_query()}
            {self._gen_constraint_query()}
            {self._gen_tail()}"""
        params = []

        for field in self._constraints:
            params.append(self._constraints[field])

        if self._order_by is not None:
            text += " ORDER BY ?"
            if self._order_asc:
                text += "ASC"
            else:
                text += "DESC"
            params.append(self._order_by)

        return text, params

    def changed_db(self):
        return False


class RemoveQuery(Query):
    """A query for removing

    Methods:
        Overridden:
            _gen_data_query() -> str
            update_data(field: str, table: str, value: Any) -> None
            generate_data() -> (str, list[Any])
    """

    def generate_query(self):
        """Generates the query

        Arguments:
            None

        Returns:
            qtext (str)
                -- The query text
            params (list[Any])
                -- The parameters of the query
        """
        text = f"""
            DELETE FROM {self._gen_table_query()}
            {self._gen_constraint_query()} {self._gen_tail()}"""
        params = []

        for field in self._constraints:
            params.append(self._constraints[field])

        return text, params


class ChangeQuery(Query):
    """A query for changing data

    Methods:
        Overridden:
            _gen_data_query() -> str
            update_data(field: str, table: str, value: Any) -> None
            generate_data() -> (str, list[Any])
    """

    def update_data(self, field, table, value=None):
        """Generates the data part of the query

        Arguments:
            None

        Returns:
            text (str)
                -- The data part of the query
        """
        self._data[f"{escape(field)}"] = value
        self._tables.add(table)

    def _gen_data_query(self):
        """Generates the data part of the query

        Arguments:
            None

        Returns:
            text (str)
                -- The data part of the query
        """
        out = []
        for field in self._data:
            out.append(f"{field}=?")
        out = ", ".join(out)
        return out

    def generate_query(self):
        """Generates the query

        Arguments:
            None

        Returns:
            qtext (str)
                -- The query text
            params (list[Any])
                -- The parameters of the query
        """
        text = f"""
            UPDATE {self._gen_table_query()}
            SET {self._gen_data_query()}
            {self._gen_constraint_query()}
            {self._gen_tail()}"""
        params = []

        for field in self._data:
            params.append(self._data[field])

        for field in self._constraints:
            params.append(self._constraints[field])

        return text, params
