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
    
def find_phone():
    phone = None
    shell = win32com.client.Dispatch("Shell.Application")
    mtp_devices = shell.Namespace(17)
    for item in mtp_devices.Items():
        if item.Path[:2] == '::': 
            for i in item.Items():
                print(i)
            # print('item', item.Name, item.Path) 
            # phone = item.InvokeVerb('Open')
            # print(phone.Items())
            # print('phone\n', [item for item in phone.Items()])
    # device_list_path  = [item.Path for item in mtp_devices.Items()]
    # device_list_name = [item.Name for item in mtp_devices.Items()]
    # print(device_list_path, '\n\n', device_list_name)
    # try:
    #     print(os.scandir('Этот компьютер\\::{20D04FE0-3AEA-1069-A2D8-08002B30309D}\\\\\\?\\usb#vid_04e8&pid_6860&ms_comp_mtp&samsung_android#6&f1ec039&0&0000#{6ac27878-a6fa-4155-ba85-f98f491d4f33}\\Внутреннее хранилище'))
    # except Exception as e:
    #     print('e', e)

find_phone()



#     # partitions = psutil.disk_partitions()
#     client = AdbClient(host="127.0.0.1", port=5037) 
#     devices = client.devices()
#     # drives = win32api.GetLogicalDriveStrings().split('\000')[:-1]
#     print(devices)
#     time.sleep(1)
