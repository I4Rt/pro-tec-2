import os
import subprocess
import shutil
import pathlib

# print(os.scandir('C:\\Users\\kipov\\Downloads'))
# open('C:\\Users\\kipov\\Downloads')

mtp_path = r"Этот компьютер\S23 FE пользователя Андрей\Внутреннее хранилище\DCIM"
# subprocess.run(["explorer", mtp_path], shell=True)
# subprocess.run(["explorer", '..'], shell=True)

# shutil.copy(mtp_path, 'C:\\Users\\kipov\\Downloads')

for file in pathlib.Path(mtp_path).rglob("*.*"):
    print(file)