import random
from Commands import Commands
from FileManager import FileManager

class Dialogue:

    @staticmethod
    def find(string, tags):
        """ Функция возвращающая True, если в string найдётся tag """
        ret = False
        for tag in tags:
            if string.lower().count(tag) != 0:
                ret = True
        return ret


    @staticmethod
    def send_theory(string, theory_library):
        """ Возвращает список [string, photo], найдя необходимые теги в сообщении. Если не найдёт тег, то return False  """
        ret = None
        for i in range(0, len(theory_library)):  # проверка фразы на поиск ключевых слов в словаре/списке theory_library
            for tag in theory_library[i]['tags']:
                if string.lower().count(tag) > 0:
                    ret = theory_library[i]['photo']
        return ret

    def __init__(self, id, SQL_server_name, databaze_name, options_file_path):
        self.id = id
        self.SQL_server = SQL_server_name
        self.databaze = databaze_name
        self.options_file_path = options_file_path

        self.wait = "work"


    def answer(self, message, word_list, photo_dictionary, tasks_dictionary):
        """
        Возвращает список [string, photo], где стринг - текст сообщения, а photo - фотография
        Если string = '$gotema$', то отправляются 2 сообщения с ожиданием в 1с.
        """


        def get_theme(id, body, words_library):
            """ Спрашивает пользователя о теме """
            if Dialogue.find(body, words_library['sentences']['test']):

                self.wait = "tema"
                self.readytasks = self.selection(id)  # заполняем readytasks см. выше



        result = []     # то, что будет выдано в return

        if message.strip()[0] == '/':
            command = Commands.analysis(self.id, message, self.options_file_path)   # проверка на наличие каких-либо команд в тексте отправителя (например: /op, /deop)
            if command:
                return [result, ""]

        if self.wait == "work":
            if self.find(message, word_list['sentences']['test']):
                pass #self.get_theme(id, body, self.word_list)
            elif not self.send_theory(id, message, photo):
                r = random.choice(word_list['sentences']['what'])
                self.write_message(id, r)