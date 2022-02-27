from backend.sqlescape import escape

QUERY_TYPES = ["add", "get", "remove", "change"]


class Query:
    def __init__(self, order_by=None, order_asc=True, limit=1):
        self._tables = set()
        self._fields = {}
        self._data = {}
        self._constraints = {}
        self._custom_constraints = []
        self._links = {}
        self._order_by = order_by
        self._order_asc = order_asc
        self._limit = limit
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

    def add_custom_constraint(self, constraint):
        self._custom_constraints.append(constraint)

    def update_data(self, field, table, value=None):

        if value is None:
            if table in self._fields:
                self._fields[table].append(field)
            else:
                self._fields[table] = [field]
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
        for constraint in self._custom_constraints:
            out.append(f"({constraint})")
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

    def _finalise_query(self, query):
        query += f" LIMIT {self._limit}"
        return query

    def _get_fields(self):
        return None


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

        text = self._finalise_query(text)
        return text, params


class GetQuery(Query):
    def _gen_antiquery(self):
        self._antiquery = AntiGetQuery()

    def get_fields(self):
        return self._fields

    def _gen_data_query(self):
        fields = []
        for table in self._fields:
            for field in self._fields[table]:
                fields.append(f"{escape(table)}.{escape(field)}")
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

        text = self._finalise_query(text)

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

        text = self._finalise_query(text)
        return text, params


class ChangeQuery(Query):
    def update_data(self, field, table, value):
        self._data[f"{escape(field)}"] = value
        self._tables.add(table)

    def _gen_data_query(self):
        out = []
        for field in self._data:
            out.append(f"{field}=?")
        out = ", ".join(out)
        return out

    def generate_query(self):
        text = f"""UPDATE {self._gen_table_query()} SET {self._gen_data_query()} {self._gen_constraint_query()}"""
        params = []

        for field in self._data:
            params.append(self._data[field])

        for field in self._constraints:
            params.append(self._constraints[field])

        text = self._finalise_query(text)

        return text, params

    def _gen_antiquery(self):
        self._antiquery = AntiChangeQuery()


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
