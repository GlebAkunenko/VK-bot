import json

class Reader:

    user_data = {}

    """ Возвращает данные о пользователях """
    def read_users_data(self, path):
        memory_read = open(path, mode='r', encoding='utf-8')
        memory = memory_read.read()
        self.user_data = json.loads(memory)
        memory_read.close()


    """ Обновляет данные о пользователе """
    def write_user_data(self, path, id, add_number):
        if self.user_data.get(id):
            self.user_data[id].append(str(add_number))
        else:
            self.user_data[id] = [str(add_number)]
        string = json.dumps(self.user_data, sort_keys=True, indent=4)
        write_memory = open(path, 'w', encoding='utf-8')
        write_memory.write(string)
        write_memory.close()


    """ Заполняет список с теорией """
    def theory_read(self, path):
        photo = []
        file = open(path, mode='r', encoding='utf-8')
        full = file.read()
        full = full.split('\n')
        for one in full:
            two = one.split(';;')
            two[0] = two[0].replace(';;', '')
            tags = two[0].split('; ')
            list = {
                'tags': tags,
                'photo': two[1].strip()
            }
            photo.append(list)
        file.close()
        return photo


    """  """
    def tasks_read(self, path):
        tasks = []
        questf = open(path, mode='r', encoding='utf-8')
        quests = questf.read()
        quests = quests.split("\n\n\n\n\n")
        for quest in quests:
            first = quest.split("\n", 4)
            type = first[0]
            dano = first[1]
            result = first[2]
            image = first[3]
            if len(first) > 4:
                answer = first[4]
            else:
                answer = ""
            if answer.replace("\n", "").replace(" ", "").strip() == "":
                answer = ""
            dictionary = {
                'type': type,
                'dano': dano,
                'answer': answer,
                'result': result,
            }
            if image != 0:
                dictionary['image'] = image
            tasks.append(dictionary)
        questf.close()
        return tasks


    """ Получает словать со сторонними данными (операторы) из json файла """
    def read_options(self, path):
        file = open(path, mode='r', encoding='utf-8')
        string = file.read()
        options = json.loads(string)
        file.close()
        return options


    """ Обновляет json файл """
    def write_options(self, path, options):
        file = open(path, mode='w', encoding='utf-8')
        string = json.dumps(options, sort_keys=True, indent=4)
        file.write(string)
        file.close()