import pypyodbc
import OldReader

connection = pypyodbc.connect(
    'Driver={SQL Server};'
    'Server=LENOVO-G700\SQLEXPRESS;'
    'Databaze=VkBot_databaze;'
)
cursor = connection.cursor()
data = OldReader.Reader()
data2 = data.theory_read("Theory.txt")







"""
for i in range (0, len(data2)):
    for tag in data2[i]['tags']:
        querty = "INSERT INTO [VkBot_databaze].[dbo].[Physics_theory_library] ([Photo], [Tag], [Priority])" \
                 " VALUES " \
                 "('" + tag + "', '" + data2[i]['photo'] + "', '" + str(i) + "')"
        cursor.execute(querty)
cursor.commit()
connection.close()
"""

"""
"INSERT INTO [VkBot_databaze].[dbo].[Tasks] ([Theme], [The task], [Answer], [Decision])" \
             " VALUES " \
             "('" + task['type'] + "', '" + task['dano'] + "', '" + task['result'] + "', '" + task['image'] + "')"
"""