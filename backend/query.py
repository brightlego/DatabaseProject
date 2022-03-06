import copy

from backend.sqlescape import escape


class Query:
    def __init__(self, order_by=None, order_asc=True, limit=1):
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

    def add_custom_select(self, field, get_text):
        self._custom_select.append((field, get_text))

    def add_custom_tail(self, tail):
        self._custom_tail.append(tail)

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
        return "", []

    def _finalise_query(self, query):
        return query

    def _gen_tail(self):
        return " ".join(self._custom_tail)

    def get_fields(self):
        return None

    def execute(self, conn):
        qtext, param = self.generate_query()
        return conn.execute(qtext, param)

    def changed_db(self):
        return True


class NullQuery(Query):
    def update_constraint(self, field, table, value):
        pass

    def add_link(self, field1, field2, table1, table2):
        pass

    def add_custom_constraint(self, constraint):
        pass

    def add_custom_select(self, field, get_text):
        pass

    def update_data(self, field, table, value=None):
        pass

    def generate_query(self):
        return "", []

    def changed_db(self):
        return False


class AddQuery(Query):
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
        text = f"""INSERT INTO
            {self._gen_table_query()}
            {self._gen_data_query()}
            {self._gen_tail()}"""
        params = []
        for field in self._data:
            params.append(self._data[field])

        return text, params


class GetQuery(Query):
    def __init__(self, order_by=None, order_asc=True, limit=1000):
        super().__init__(order_by=order_by, order_asc=order_asc, limit=limit)

    def get_fields(self):
        fields = copy.deepcopy(self._fields)
        fields[" "] = []
        for field, _ in self._custom_select:
            fields[" "].append(field)
        return fields

    def _gen_data_query(self):
        fields = []
        for table in self._fields:
            for field in self._fields[table]:
                fields.append(f"{escape(table)}.{escape(field)}")

        for _, get_text in self._custom_select:
            fields.append(get_text)

        fields = ",".join(fields)
        return fields

    def generate_query(self):
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

        text = self._finalise_query(text)

        return text, params

    def changed_db(self):
        return False


class RemoveQuery(Query):
    def generate_query(self):
        text = f"""
            DELTE FROM {self._gen_table_query()}
            {self._gen_constraint_query()} {self._gen_tail()}"""
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

        text = self._finalise_query(text)

        return text, params
