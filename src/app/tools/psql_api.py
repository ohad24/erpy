# ver: 0.2
class PostgresAPI:
    # TODO: lang method
    def __init__(self, pg_con):
        self.pg_con = pg_con

    def exec_query(self, query, d_sql_parameters=None, one=False):
        if d_sql_parameters is None:
            d_sql_parameters = {}
        self.cur = self.pg_con.cursor()
        self.one = one
        self.cur.execute(query, None if d_sql_parameters is None else (d_sql_parameters))
        self.pg_con.commit()
        try: # FIXME: when no result set returns
            self.data = tuple(x for x in self.cur.fetchall())
            self.desc = tuple(x for x in self.cur.description)
        except self.pg_con.ProgrammingError:
            pass


    def data_size(self):
        rows = len(self.data)
        cols = len(self.data[0]) if rows != 0 else 0
        return rows, cols

    def lod(self):
        data_list = []
        for row in self.data:
            tmp = []
            for i, val in enumerate(row):
                tmp.append((self.desc[i][0], val))
            d_row = dict(tmp)
            data_list.append(d_row)
        if self.one and len(data_list) != 0:
            data_list = data_list[0]
        return data_list

    def raw_data(self):
        return self.data
