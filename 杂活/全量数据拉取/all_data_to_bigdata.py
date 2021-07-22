# -*- coding: utf-8 -*-
"""
function：extract_all_data_from_server

@author：lezhipeng

email: 2399809590@qq.com

date:2021/7/16
"""
import pandas as pd
from impala.dbapi import connect
from tqdm import tqdm
import os
import pymysql
import logging


def extract_data(db_name,db2,table,ip):
    dir_path = os.path.join(path_base, 'all_data/{t}/'.format(t=table))
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    extract_sql = "select * from {db}.{table}".format(db=db_name,table=table)
    try:
        data_iter = pd.read_sql(extract_sql,db2,chunksize=chunksize)
        max_i = max([i for i, data_ods_e3 in enumerate(data_iter)])
        data_iter = pd.read_sql(extract_sql, db2, chunksize=chunksize)
        data_ods_e2 = []
        z = 0
        for i,data_ods_e3 in enumerate(data_iter):
            data_ods_e2.append(data_ods_e3)
            if len(data_ods_e2) == batch_size:
                z += 1
                data_ods_e1 = pd.concat(data_ods_e2,ignore_index=True)
                data_ods_e = data_ods_e1.astype('str')

                path = os.path.join(dir_path, '{t}_{db_name}_{ip}_{z}.parquet'.format(t=table, db_name=db_name,ip=ip, z=z))
                data_ods_e.drop_duplicates(subset=['id', 'log_user'], inplace=True)
                data_num = len(data_ods_e)
                # 保存parquet
                data_ods_e.to_parquet(path, compression='snappy', index=None)
                data_ods_e2 = []
                logger.info('ip:{ip},db_name:{db_name},取数:{data_num}'.format(ip=ip,db_name=db_name,
                                                                                    data_num=data_num))
            elif len(data_ods_e2) <= batch_size and i == max_i:
                data_ods_e1 = pd.concat(data_ods_e2, ignore_index=True)
                data_ods_e = data_ods_e1.astype('str')
                path = os.path.join(dir_path,
                                    '{t}_{db_name}_{ip}_{z}.parquet'.format(t=table, db_name=db_name, ip=ip, z='end'))
                data_ods_e.drop_duplicates(subset=['id', 'log_user'], inplace=True)
                data_num = len(data_ods_e)
                # 保存parquet
                data_ods_e.to_parquet(path, compression='snappy', index=None)
                data_ods_e2 = []
                logger.info('ip:{ip},db_name:{db_name},取数:{data_num}'.format(ip=ip, db_name=db_name,
                                                                             data_num=data_num))
            else:
                continue
#         return data_ods_e
    except Exception as e:
        logger.info(e)
        logger.info('ip:{ip},db_name:{db_name},取数:{data_num}'.format(ip=ip, db_name=db_name,
                                                                     data_num=0))
    return

def main():
    sql_ = """
    select distinct inner_ip from eoms.game_assets where  project_id=1 and channel_id=7
    """
    all_ip = pd.read_sql(sql_, db1)
    pbar = tqdm(total=len(all_ip), desc='get_data_{}'.format(table))
    for ip in all_ip.inner_ip.values:
        db2 = pymysql.connect(host="{}".format(ip), user="maxwell", port=3336,
                              password="maxwell",
                              charset="utf8")
        db_sql = 'show databases;'
        dbs = pd.read_sql(db_sql, db2).Database.values
        for db in dbs:
            if db[:6] == 'yx_log':
                logger.info('ip:{ip},db_name:{db_name}'.format(ip=ip, db_name=db))

                extract_data(db,db2,table,ip)
        pbar.update(1)
        logger.info('ip:{ip} 取数完成！'.format(ip=ip))

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description='manual to this script')
    parser.add_argument('--file', type=str, default=None)
    args = parser.parse_args()
    table_name = args.file
    # 参数
    table = table_name
    chunksize = 2000
    batch_size = 100
    path_base = os.path.abspath(".")

    log_path = os.path.join(path_base, 'log/get_data_{table}.log'.format(table=table))
    logging.basicConfig(level=logging.INFO,
                        filename=log_path, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger = logging.getLogger(__name__)

    conn = connect(host='172.16.16.149', port=21050)
    # 公网和私网ip
    db1 = pymysql.connect(host="134.175.106.193", user="maxwell", port=3336,
                          password="maxwell",
                          charset="utf8")
    main()
    logger.info('全量取数完成！')
