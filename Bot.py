from vk_api import *
from Teacher import Dialogue
from SQL_server import SQL_server
from FileManager import FileManager

welcome = """
          Vk bot 2.1 запущен
          Используемая версия vk_api 5.85 (11.2.1)
          by Gleb1000
          """

SQL_server_name = "LENOVO-G700\SQLEXPRESS"
options_file_path = "Options.json"


vk = VkApi(token='6df58faf8ccfbacb0ee4ced66e5a58db084e482ee499a6ffe4b3f42f5be082d28ab19fe07c53f8b85dea9')
vk._auth_token()

dialogues = dict()  # хранит объекты диалога и id
data_baze = dict()    # ключ - название таблицы, значение - список с колонками этой таблицы
tables = FileManager.read_data_from_json(options_file_path)['tables']
for table_name in tables:
      


print(welcome)

timer = 0
while True:
    question = vk.method("messages.getConversations", {"offset": 0, "count": 200, "filter": "unanswered"})
    if question["count"] >= 1:
        for i in range(0, len(question["items"])):
            id = question["items"][i]["last_message"]["from_id"]
            message = question["items"][i]["last_message"]["text"]
            if dialogues.get(str(id)):
                #dealogs[id]
                pass
            else:
                pass
                #new_dealog = Dialogue(id, SQL_server_name, options_file_path)
                #new_dealog.answer(message, )