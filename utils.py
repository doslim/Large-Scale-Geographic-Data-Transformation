# utils.py
# define the function to get the ak, the file name of data
# define the function to transform the data

import pandas as pd
import os
import requests
import numpy as np

def get_ak(key_id, ak_path='key.xls'):
    my_ak = pd.read_excel(ak_path, header=None)
    my_ak.columns = ['ak']
    return my_ak.ak.values[key_id]


def get_file_list(path):
    for root, _, files in os.walk(path):
        return files
            

def get_file_name(group_id, split_id, file_path='./data/new_data'):
    '''
    Sort the file in each group in alphabetical order
    Get the name of the file according to the split_idx
    '''
    
    # get the list of all files
    files = get_file_list(file_path)
    file_name_list = []
    for file in files:
        if str(group_id) in file.split('_'):
            file_name_list.append(file)
    file_name_list.sort()
    return file_name_list[split_id]


def address_to_gps(address, my_ak, province):
    if address is np.nan or address is None:
        return False, "Null address"
    
    special_str = '!@#$%^&*'
    replace_str = ' '*len(special_str)
    trantab = str.maketrans(special_str, replace_str)
    
    address = address.translate(trantab)
    address = address.replace(" ",'')
    
    base_url = '''
    https://api.map.baidu.com/geocoding/v3/?address={}&output=json&ak={}&callback=showLocation
    '''
    url = base_url.format(province+address, my_ak)
    # print(url)
    try:
        html = requests.get(url)
    except requests.exceptions.ConnectionError:
        print("Connection Error")
        return False, "Connection Error"
    except:
        print("Unknown Error")
        return False, "Unknown Error"

    if html.status_code == 200:
        result = html.json()
    else:
        return False, None

    if result['status']==0:
        return True, result['result']['location']
    else:
        return False, result['status']