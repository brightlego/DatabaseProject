from backend.sqlescape import escape

QUERY_TYPES = ["add", "get", "remove", "change"]


class Query:
    def __init__(self, order_by=None, order_asc=True):
        self._tables = set()
        self._data = {}
        self._constraints = {}
        self._links = {}
        self._order_by = order_by
        self._order_asc = order_asc
        self._gen_antiquery()

    def update_constraint(self, field, table, value):
        self._constraints[f"{escape(table)}.{escape(field)}"] = value
        self._tables.add(table)

    def add_link(self, field1, field2, table1, table2):
        self._links[
            f"{escape(table1)}.{escape(field1)}"
        ] = f"{escape(table2)}.{escape(field2)}"
        self._tables.add(table1)
        self._tables.add(table2)

    def update_data(self, field, table, value=None):
        self._data[f"{escape(table)}.{escape(field)}"] = value
        self._tables.add(table)

    def _gen_data_query(self):
        pass

    def _gen_constraint_query(self):
        out = []
        for field in self._constraints:
            out.append(f"{field}=?")
        for field in self._links:
            out.append(f"{field}={self._links[field]}")
        out = " AND ".join(out)
        if out:
            out = "WHERE " + out
        return out

    def _gen_table_query(self):
        out = []
        for table in self._tables:
            out.append(escape(table))
        return ",".join(out)

    def generate_query(self):
        pass

    def _gen_antiquery(self):
        self._antiquery = NullQuery()


class NullQuery(Query):
    def _gen_antiquery(self):
        self._antiquery = self

    def generate_query(self):
        return "", []


class AddQuery(Query):
    def _gen_antiquery(self):
        self._antiquery = AntiAddQuery()

    def _gen_data_query(self):
        fields = []
        values = []
        for field in self._data:
            fields.append(field)
            values.append("?")
        fields = ",".join(fields)
        values = ",".join(values)

        return f"({fields}) VALUES ({values})"

    def update_data(self, field, table, value=None):
        self._data[f"{escape(field)}"] = value
        self._tables.add(table)

    def generate_query(self):
        text = f"""INSERT INTO {self._gen_table_query()} {self._gen_data_query()}"""
        params = []
        for field in self._data:
            params.append(self._data[field])

        return text, params


class GetQuery(Query):
    def _gen_antiquery(self):
        self._antiquery = AntiGetQuery()

    def _gen_data_query(self):
        fields = []
        for field in self._data:
            fields.append(field)
        fields = ",".join(fields)
        return fields

    def generate_query(self):
        text = f"""SELECT {self._gen_data_query()} FROM {self._gen_table_query()} {self._gen_constraint_query()}"""
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


class RemoveQuery(Query):
    def _gen_antiquery(self):
        self._antiquery = AntiRemoveQuery()

    def generate_query(self):
        text = (
            f"""DELTE FROM {self._gen_table_query()} {self._gen_constraint_query()}"""
        )
        params = []

        for field in self._constraints:
            params.append(self._constraints[field])

        return text, params


class ChangeQuery(Query):
    def _gen_antiquery(self):
        self._antiquery = ChangeQuery()


class AntiAddQuery(RemoveQuery):
    def _gen_antiquery(self):
        pass


class AntiGetQuery(NullQuery):
    def _gen_antiquery(self):
        pass


class AntiRemoveQuery(AddQuery):
    def _gen_antiquery(self):
        pass


class AntiChangeQuery(ChangeQuery):
    def _gen_antiquery(self):
        pass
