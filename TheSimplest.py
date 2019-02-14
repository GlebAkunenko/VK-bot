import pypyodbc

cursor = conection.cursor()
SQL_query = (
    """
    insert into [Test].[dbo].[a]
    ([UserLogin], [Password], [RealName], [RegistrationDate])
    values  ('python_born', 'ican', null, null)
    """
)
cursor.execute(SQL_query)
conection.commit()
conection.close()


class Test:
    def __init__(self, SQL_server_name, data_baze_name):
        conection = pypyodbc.connect(
            'Driver={SQL Server};'
            'Server=' + SQL_server_name + ';'
            'Databaze=' + data_baze_name + ';'
        )
        self.cursor = conection.cursor()