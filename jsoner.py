import json
import shutil
import os


from tempfile import NamedTemporaryFile


encoding = "utf8"


def save_json(path, data, sort = False):
    mode = 'w'

    while True:
        temp_file = NamedTemporaryFile(mode = mode, encoding = encoding, delete = False)

        try:
            json.dump(obj = data, fp = temp_file, sort_keys = sort)

            temp_file.close()

            shutil.move(temp_file.name, path)
            
            break
        except Exception as e:
            print(e)
            print(path)
            print('save json problem\n------------------------------------')


def save_json_with_ident(path, data, sort = False, ascii_ = True):
    mode = 'w'

    while True:
        temp_file = NamedTemporaryFile(mode = mode, encoding = encoding, delete = False)

        try:
            json.dump(data, temp_file, sort_keys = sort, indent = 4, ensure_ascii = ascii_)

            temp_file.close()

            shutil.move(temp_file.name, path)

            break
        except Exception as e:
            os.remove(temp_file.name)


def return_json(path):
    result = {"success": False, "except": "BASE ERROR"}
    mode = 'r'

    try:
        with open(file = path, mode = mode, encoding = encoding) as file_:
            data = json.loads(file_.read())

        result = {"success": True, "data": data}
    except Exception as e:
        if type(e).__name__ != 'FileNotFoundError':
            print(e)
            print(path)
            print('return json problem\n------------------------------------')
        
    return result
