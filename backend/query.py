QUERY_TYPES = ["add", "get", "remove", "change"]


class Query:
    def __init__(self, table, order_by=None, order_asc=True):
        self._table = table
        self._data = {}
        self._constraints = {}
        self._order_by = order_by
        self._order_asc = order_asc

    def update_constraint(self, field, value):
        self._constraints[field] = value

    def update_data(self, field, value=None):
        self._data[field] = value

    def _gen_data_query(self):
        pass

    def _gen_constraint_query(self):
        out = []
        for _ in self._constraints:
            out.append("WHERE ?=?")
        return " AND ".join(out)

    def generate_query(self):
        pass


class AddQuery(Query):
    def _gen_data_query(self):
        fields = []
        for _ in self._data:
            fields.append("?")
        fields = ",".join(fields)

        values = fields

        return f"({fields}) VALUES ({values})"

    def generate_query(self):
        text = f"""INSERT INTO ? {self._gen_data_query()}"""
        params = []
        params.append(self._table)
        for field in self._data:
            params.append(field)
        for field in self._data:
            params.append(self._data[field])

        return text, params


class GetQuery(Query):
    def _gen_data_query(self):
        fields = []
        for _ in self._data:
            fields.append("?")
        fields = ",".join(fields)
        return fields

    def generate_query(self):
        text = f"""SELECT {self._gen_data_query()} FROM ?
                         WHERE {self._gen_constraint_query()}"""
        params = []

        for field in self._data:
            params.append(field)

        params.append(self._table)

        for field in self._constraints:
            params.append(field)
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
    def generate_query(self):
        text = f"""DELTE FROM ? WHERE {self._gen_constraint_query()}"""
        params = []

        params.append(self._table)

        for field in self._constraints:
            params.append(field)
            params.append(self._constraints[field])

        return text, params
