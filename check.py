import win32api
import time
import psutil
from ppadb.client import Client as AdbClient
import wmi
import os
import subprocess
import win32com.client

def check_wmi():
    print('check c')
    c = wmi.WMI()
    device_list = [dev.Name for dev in c.Win32_PnPEntity()]
    new_devices = []
    while True:
        device_list_new = [dev.Name for dev in c.Win32_PnPEntity()]
        if len(device_list_new) > len(device_list):
            decr = list(set(device_list_new) - set(device_list))
            # print('decr', decr)
            new_devices = decr
            for new_dev in new_devices:
                try:
                    print(os.scandir(f'Этот компьютер\\{new_dev}\\Внутреннее хранилище'))
                    # subprocess.run(["explorer", f'Этот компьютер\\{new_dev}\\Внутреннее хранилище'], shell=True)
                except Exception as e:
                    print('e', e)  
        print(len(new_devices), new_devices, len(device_list), len(device_list_new))
        device_list = device_list_new
        
        time.sleep(1)
    
def find_phone_directory():
    folder_pc_path = r"C:\Users\kipov\Downloads\test_folder_download"
    shell = win32com.client.Dispatch("Shell.Application")
    mtp_devices = shell.Namespace(17)
    for item in mtp_devices.Items():
        if item.Path[:2] == '::': 
            try:
                folders = item.GetFolder.Items()
                inside_folders = folders[0].GetFolder.Items()
                for inside_folder in inside_folders:
                    if inside_folder.Name == 'Documents':
                        doc_folder = inside_folder.GetFolder.Items()
                        for audio_folder in doc_folder:
                            if audio_folder.Name == 'Audio':
                                audio_items = audio_folder.GetFolder.Items()
                                shell.Namespace(folder_pc_path).CopyHere(audio_items)
                                print([audio_file.Name for audio_file in audio_items])
            except Exception as e:
                print('e', e)

find_phone_directory()
