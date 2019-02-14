from FileManager import FileManager


class Commands:


    """ Изменяет файлы внутри бота. Возвращает результат (в виде ответа) """
    @staticmethod
    def analysis(id, string, file_options_path):

        result = None

        options = FileManager.read_data_from_json(file_options_path)

        if string == "/op":
            if options['operators'] and id not in options['operators']:
                options['operators'].append(id)
                result = "Операция успешно выполнена. Вы оператор"
            elif id not in options['operators']:
                options['operators'] = [id]
                result = "Операция успешно выполнена. Вы оператор"
            else:
                result = "Операция не выполнена, так как вы уже оператор"
            FileManager.write_data_to_json(file_options_path, options)
        if string == "/deop":
            if options['operators'] and id in options['operators']:
                for i in range(0, options['operators'].count(id)):
                    options['operators'].remove(id)
                result = "Операция успешно выполнена. Терерь вы не оператор"
            else:
                result = "Операция не выполнена, так как вы не были оператором"
            FileManager.write_data_to_json(file_options_path, options)

        return result