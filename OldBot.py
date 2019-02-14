import Reader
from vk_api import *
from Dealogue import *
from Commands import *

welcome = "\n" \
          "Vk bot 2.0 запущен \n" \
          "Используемая версия vk_api 5.85 (11.2.1) \n" \
          "by Gleb1000 \n"

vk = VkApi(token='6df58faf8ccfbacb0ee4ced66e5a58db084e482ee499a6ffe4b3f42f5be082d28ab19fe07c53f8b85dea9')
vk._auth_token()

data = Reader.Reader()

photo = data.theory_read("theory.txt")
tasks = data.tasks_read("Tasks.txt")
data.read_users_data("Users data.json")
options = data.read_options("Options.json")
dealogs = {}


print(welcome)
while True:
    question = vk.method("messages.getConversations", {"offset": 0, "count": 200, "filter": "unanswered"})
    if question["count"] >= 1:
        for i in range(0, len(question["items"])):
            id = question["items"][i]["last_message"]["from_id"]
            if dealogs.get(id):
                update = dealogs[id].controll(question, i, options)
                if update:
                    data.write_user_data("Users data.txt", id, update)
            else:
                answer = Dealogue(vk, data.user_data, photo, tasks, "Words_list.json")
                update = answer.controll(question, i, options)
                if update:
                    data.write_user_data("Users data.txt", id, update)
                dealogs[id] = answer