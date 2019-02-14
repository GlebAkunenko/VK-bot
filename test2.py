from SQL_server import SQL_server


a = SQL_server.read_dictionary_from_bd("LENOVO-G700\SQLEXPRESS", "Physics_theory_library", '[Photo]', '[Tag]', '[Priority]')
for b in a:
    print(b)
