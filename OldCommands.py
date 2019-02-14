import Reader, vk_api
class Commands:

    @staticmethod
    def write_message(self, vk, id, message, photo_id = ""):
        """ Упращённая функция для вызова сообщений """
        if photo_id != "":
            vk.method('messages.send', {'user_id': id, 'message': message, 'attachment': photo_id})
        else:
            vk.method('messages.send', {'user_id': id, 'message': message})

    @staticmethod
    def analis(self, vk, id, string, options_path):
        data = Reader.Reader()
        body = string
        options = data.read_options(options_path)

        if body == "/op":
            if options['operators'] != None and id not in options['operators']:
                options['operators'].append(id)
                vk.method('messages.send', {'user_id': id, 'message': "Операция успешно выполнена. Вы оператор"})
            elif id not in options['operators']:
                options['operators'] = [id]
                vk.method('messages.send', {'user_id': id, 'message': "Операция успешно выполнена. Вы оператор"})
            else:
                vk.method('messages.send', {'user_id': id, 'message': "Операция не выполнена, так как вы уже оператор"})
            data.write_options("Options.json", options)
        if body == "/deop":
            if options['operators'] != None and id in options['operators']:
                for i in range(0, options['operators'].count(id)):
                    options['operators'].remove(id)
                vk.method('messages.send',
                          {'user_id': id, 'message': "Операция успешно выполнена. Терерь вы не оператор"})
            else:
                vk.method('messages.send',
                          {'user_id': id, 'message': "Операция не выполнена, так как вы не были оператором"})
            data.write_options("Options.json", options)