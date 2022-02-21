QUERY_TYPES = ["add", "get", "remove", "change"]

class Query:
    def __init__(self, table, order_by=None, order_asc=True):
        self._table = table
        self._data = {}
        self._constraints = {}
        self._order_by = order_by
        self._text = ""
        self._params = []

    def update_constraint(self, field, value):
        self._constraints[field] = value

    def update_data(self, field, value=None):
        self._data[field] = value

    def _gen_data_query(self):
        pass

    def _gen_constraint_query(self):
        out = []
        for field in self._constraints:
            out.append("WHERE ?=?")
        return " AND ".join(out)

    def generate_query(self):
        if self._order_by is not None:
            self._text += " ORDER BY ?"
            if order_asc:
                self._text += "ASC"
            else:
                self._text += "DESC"
            self._params.append(self._order_by)

class AddQuery(Query):
    def _gen_data_query(self):
        fields = []
        for field in self._data:
            fields.append("?")
        fields = ','.join(fields)

        values = fields

        return f"({fields}) VALUES ({values})"

    def generate_query(self):
        self._text = f"""INSERT INTO ? {self._gen_data_query()}"""
        self._params = []
        self._params.append(self._table)
        for field in self._data:
            self._params.append(field)
        for field in self._data:
            self._params.append(self._data[field])

        return self._text, self._params

class GetQuery(Query):
    def _gen_data_query(self):
        fields = []
        for field in self._data:
            fields.append("?")
        fields = ','.join(fields)
        return fields

    def generate_query(self):
        self._text = f"""SELECT {self._gen_data_query()} FROM ? WHERE {self._gen_constraint_query()}"""
        self._params = []

        for field in self._data:
            self._params.append(field)

        self._params.append(self._table)

        for field in self._constraints:
            self._params.append(field)
            self._params.append(self._constraints[field])

        super().generate_query()

        return self._text, self._params

class RemoveQuery(Query):
    def generate_query(self):
        self._text = f"""DELTE FROM ? WHERE {self._gen_constraint_query()}"""
        self._params = []

        self._params.append(self._table)

        for field in self._constraints:
            self._params.append(field)
            self._params.append(self._constraints[field])

        return self._text, self._params
