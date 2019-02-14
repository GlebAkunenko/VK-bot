from vk_api import *
import random, time, json
class Dealogue:
    wait = ""
    others = {} # словарь в котором ключ - id, а значение - список задач, решение которых было показано пользователь с данным id
    readytasks = [] # список задач, которые можно предоставить пользователю

    def __init__(self, vk, users_info, photo_library, tasks, words_list_path_json):
        self.vk = vk
        self.photo = photo_library
        self.data = users_info
        self.tasks = tasks
        words_file = open(words_list_path_json, mode='r', encoding='utf-8')
        words_string = words_file.read()
        self.words = json.loads(words_string)
        words_file.close()


    def write_message(self, id, string, photoid=""):
        """ Упращённая функция для вызова сообщений """
        if photoid != "":
            self.vk.method('messages.send', {'user_id': id, 'message': string, 'attachment': photoid})
        else:
            self.vk.method('messages.send', {'user_id': id, 'message': string})


    def find(self, string, tags):
        """ Функция возвращающая True, если в string найдётся tag """
        ret = False
        for tag in tags:
            if string.lower().count(tag) != 0:
                ret = True
        return ret


    """ Возвращает список всех нерешённых задач, исключая задачи решения которых были даны """
    def selection(self, id):
        first = self.data.get(id)
        if first == None:
            self.data[id] = []
            complite = []   # содержит решённые тесты и тесты, решения которых выдавались пользователю (1)
        else:
            complite = self.data[id].copy()
        if self.others.get(id):
            complite.extend(self.others[id])    # (1)
        newtests = []
        for i in range(0, len(self.tasks)):
            if i not in complite:
                newtests.append(i)
        return newtests


    """ Основная функция, решающая какое действие предпримет бот в определённой ситуации """
    def controll(self, question, number, options={}):
        self.options = options
        id = question["items"][number]["last_message"]["from_id"]
        body = question["items"][number]["last_message"]["text"]
        if self.wait == "":
            if self.find(body, self.words['sentences']['test']):
                self.get_theme(id, body, self.words)
            elif not self.send_theory(id, body, self.photo):
                r = random.choice(self.words['sentences']['what'])
                self.write_message(id, r)
        elif self.wait == "continuation":
                self.wait_continuation(body, self.words)
                print("!!!")
        elif self.wait == "tema":
            self.send_tasks(id, body, self.words)
        elif self.wait == "result":
            if self.find(body, self.words['sentences']['how']):
                self.send_decision(id, self.tasks, self.words)
            else:
                if self.check_result(id, body, self.tasks, self.words):
                    return self.task_number


    """ Отправляет теорию, найдя необходимые теги в сообщении. Если не найдёт тег, то return False """
    def send_theory(self, id, body, theory_library):
        ret = False
        for i in range(0, len(theory_library)):  # проверка фразы на поиск ключевых слов в словаре/списке theory_library
            for tag in theory_library[i]['tags']:
                if body.lower().count(tag) > 0:
                    self.write_message(id, "", theory_library[i]['photo'])
                    ret = True
        return ret


    """ Спрашивает пользователя о теме """
    def get_theme(self, id, body, words_library):
        if self.find(body, words_library['sentences']['test']):
            r = random.choice(words_library['sentences']['go'])
            self.write_message(id, r)
            time.sleep(1)
            r = random.choice(words_library['sentences']['tema'])
            self.write_message(id, r)
            self.wait = "tema"
            self.readytasks = self.selection(id)  # заполняем readytasks см. выше


    """ Принимает сообщение, и отправляет случайное задание по темам, найденым в сообщение (body). Заполнет  """
    def send_tasks(self, id, body, words_library):
        types = []
        finishtasks = []  # тесты учавствующие в подборе.
        all_types = False   # небоходимо для структуры (2)
        if self.find(body, words_library['tags']['tag']['random']):
            for i in range(0, len(words_library['tags']['tags_list'])):
                types.append(words_library['tags']['tags_list'][i])
        for i in range(0, len(words_library['tags']['tags_list'])):
            if self.find(body, words_library['tags']['tag'][words_library['tags']['tags_list'][i]]):
                if all_types:
                    types.clear()   # если в тексте найдут слово из 'random' и слово из отдельного тега, напимер "любой из прд", бот примнимает только 'прд'
                    all_types = True
                types.append(words_library['tags']['tags_list'][i])
        if types == []:
            self.wait = ""  # если бот признаёт сообщение непонятным, то возвращается к своему основному режиму
            r = random.choice(words_library['sentences']['what'])
            self.write_message(id, r)
        for i in self.readytasks:
            if self.tasks[i]['type'] in types:
                finishtasks.append(i)  # заполнение finishtasks
        if finishtasks != []:
            self.task_number = random.choice(finishtasks)
            string = self.tasks[self.task_number]['dano']
            if self.options.get("operators"):
                if id in self.options["operators"]:
                    string += "    (" + str(self.tasks[self.task_number]['result']) + ")"
            self.write_message(id, string)
            self.wait = "result"
        elif types != []:
            for i in self.others[id]:
                if self.tasks[i]['type'] in types:
                    finishtasks.append(i)
            if finishtasks == []:
                self.write_message(id, "Поздравляю! Ты прорешал все тесты по этой теме!")
                time.sleep(1.5)
                self.write_message(id, "Какую тему выберешь?")
                self.wait = "tema"
            else:
                self.task_number = random.choice(finishtasks)
                self.write_message(id, self.tasks[self.task_number]['dano'], "")
                self.wait = "result"


    """ Отправляет решение обробатываемой задачи пользователю """
    def send_decision(self, id, tasks_library, words_library):
        if tasks_library[self.task_number].get('image') != None and tasks_library[self.task_number]['answer'] == "":
            self.write_message(id, "", tasks_library[self.task_number]['image'])
        if tasks_library[self.task_number].get('image') == None:
            self.write_message(id, tasks_library[self.task_number]['answer'], "")
        r = random.choice(words_library['sentences']['restart'])
        self.write_message(id, r)
        self.others[id].append(self.task_number)


    """ Проверка ответа по обробатываемой задаче (self.task_number) """
    def check_result(self, id, body, tasks_library, words_library):
        if body.lower().strip().replace(',', '.') == tasks_library[self.task_number]['result'].replace(',', '.'):
            r = random.choice(words_library['sentences']['right'])
            self.write_message(id, r)
            if self.data.get(id):
                self.data[id].append(self.task_number)
            else:
                self.data[id] = [self.task_number]
            if self.task_number in self.others:
                self.others[id].remove(self.task_number)
            time.sleep(1)
            r = random.choice(words_library['sentences']['next'])
            self.write_message(id, r)
            self.wait = "continuation"
            return True
        else:
            r = random.choice(words_library['sentences']['wrong'])
            self.write_message(id, r)
            return False



    """ Принимает ответ да/нет, на вопрос: "Продолжать опрос" """
    def wait_continuation(self, body, words_library):
        if self.find(body, words_library['sentences']['yes2']) or self.find(body.replace(",", "").replace(".", ""),"да нет"):
            self.wait = "tema"
        else:
            self.wait = ""