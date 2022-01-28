import shutil
import os

import secrets

def save_file(files):
    for file in files:
        random_hex = secrets.token_hex(8)
        _, file_ext = os.path.splitext(file.filename)
        file_name = random_hex + file_ext
        file_path = os.path.join(os.getcwd(), 'static\\files', file_name)
        print(file_path)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    return file_path
