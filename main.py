import yaml
import time
import os
import json
import numpy as np
from utils import get_ak, get_file_name, address_to_gps
import argparse
import pandas as pd

def transformation(config):
    ak_path = config['ak_path']
    key_id = config['key_id']
    file_path = config['file_path']
    target_path = config['target_path']
    group_id = config['group_id']
    split_id = config['split_id']
    log_path = config['log_path']
    error_path = config['error_path']
    group_path = config['group_path']
    
    # get the file name
    # the name of logs, ERROR_FILE, transformed file are corresponding to the file name
    file_name = get_file_name(group_id, split_id, file_path)
    config['file_name'] = file_name
    log_path = os.path.join(log_path,'{}.json'.format(file_name.split('.')[0]))
    error_path = os.path.join(error_path,'{}_error.csv'.format(file_name.split('.')[0]))
    transformed_path = os.path.join(target_path, file_name)
    print(log_path)
    print(error_path)
    print(transformed_path)
    
    # get the ak
    ak = get_ak(key_id, ak_path)
    config['ak'] = ak
    
    # get time
    begin_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    start_time = time.time()
    
    # load data
    data = pd.read_csv(os.path.join(file_path, file_name), dtype={"企业机构类型":str, "行业代码":str})
    data_len = len(data)
    list_of_address = data['住所'].values
    config['data_len'] = data_len
    
    # get the province of the data
    data_group = pd.read_csv(group_path)
    original_file_name = '{}.dta'.format(file_name.split('_')[1])
    province = data_group[data_group.file_name==original_file_name].province.values[0]
    config['province'] = province
    
    # initialize the list to store longitude and latitude
    longitude = []
    latitude = []
    
    # to record the error information
    error_address = []
    error_info = []
    error_record = pd.DataFrame(columns=['error_address','error_info'])
    error_num = 0
    
    logs = [config, 'Begin time: {}'.format(begin_time), 'Begin Transformation——————']
    with open(log_path, "w") as fp:
        json.dump(logs, fp)
    trans_log = {}
    
    print(logs)
    for add in list_of_address:
        flag, result = address_to_gps(add, ak, province)
        if flag:
            longitude.append(result['lng'])
            latitude.append(result['lat'])
        else: 
            error_num += 1
            error_address.append(add)
            error_info.append(result)
            longitude.append(-1)
            latitude.append(-1)
    assert len(longitude) == data_len
    assert len(latitude) == data_len
    
    data['longitude'] = longitude
    data['latitude'] = latitude
    data.to_csv(transformed_path, index=False)
    
    error_record['error_address'] = error_address
    error_record['error_info'] = error_info
    error_record.to_csv(error_path,index=False)
    
    trans_log['duration'] = time.time()-start_time
    trans_log['error_num'] = error_num
    logs.append(trans_log)
    
    end_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    logs.append(end_time)
    
    print("error number: {}".format(error_num))
    print("end time: {}".format(end_time))
    
    with open(log_path, "w") as fp:
        json.dump(logs, fp)
        

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', type=str, required=True, help='path to the config')
    args = parser.parse_args()

    with open(args.config, 'r') as stream:
        config = yaml.safe_load(stream)

    transformation(config)
