import pypyodbc


class SQL_server:

    """ Возвращает список, картёжей. Без разбора и всякой систематизации """
    @staticmethod
    def read_all_data_from_bd(SQL_server_name, Table_name, *columns):

        if len(columns) == 1:
            columns = columns[0]

        string_columns = ""
        for i, column in enumerate(columns):
            if i != 0:
                string_columns += ", [" + column.replace('[', '').replace(']', '') + "]"
            else:
                string_columns += "[" + column.replace('[', '').replace(']', '') + "]"

        SQL_query = "SELECT " + string_columns + " FROM [VkBot_databaze].[dbo].[" + Table_name + "]"
        connection = pypyodbc.connect(
            'Driver={SQL Server};'
            'Server=' + SQL_server_name + ';'
            'Databaze=VkBot_databaze;'
        )
        cursor = connection.cursor()
        cursor.execute(SQL_query)
        return cursor.fetchall()

    """ Возвращает список словарей. Всё как и должно быть! Без мусора"""
    @staticmethod
    def read_dictionary_from_bd(SQL_server_name, Table_name, *columns_):

        if len(columns_) == 1:
            columns_ = columns_[0]

        destroy_bracket = lambda s: s.replace('[', '').replace(']', '')
        columns = tuple(map(destroy_bracket, columns_))

        pile = SQL_server.read_all_data_from_bd(SQL_server_name, Table_name, columns)
        tasks = []
        for pile_task in pile:
            task = dict()
            for i in range(len(pile_task)):
                task[columns[i]] = pile_task[i]
            tasks.append(task)
        return tasks


"""
SQL_server = "LENOVO-G700\SQLEXPRESS"
data_baze = "a"
connection = pypyodbc.connect(
    'Driver={SQL Server};'
    'Server=' + SQL_server + ';'
    'Databaze=' + data_baze + ';'
)
cursor = connection.cursor()

cursor.execute(SQL_query)
connection.commit()
connection.close()
"""
