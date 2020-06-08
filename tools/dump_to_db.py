#!bash/bin/python
#__auth__ = kevin
#Date 2020/5/26

"""
airline policy 中间的空格用_代替
"""
import os
import sys
import pymysql
from readfile import read_file
import asyncio
import re
import configparser

root = os.getcwd()
databases_dir = os.path.join(root,'Database')
config = configparser.ConfigParser()
config_file = os.path.join(root,'config','config.ini')
config.read(config_file)
try:  
    db_username=config.get('DB','UserName')
    db_password =  config.get('DB','PassWord')
except Exception as e:
    print('请核对数据库用户名和密码(config文件中)')

def _read_files(dir):
    try:
        files = os.listdir(databases_dir)
        res = []
        for i in range(len(files)):
            if re.match(r'.*\.csv',files[i]):
                res.append(files[i])


    except Exception as e:
        raise e
        return None
    else:
        return res



def dump_to_db(host='localhost',port=3306):
    try:
        connection = pymysql.connect(
        host=host,
        port=port,
        user=db_username,
        password=db_password,
        )
    except Exception as e:
        raise e
        print('Mysql连接失败！')
        return None
    else:
        print('Mysql连接成功')
    cursor = connection.cursor()
    files = _read_files(databases_dir)
    if not files:
        print('Database文件夹为空')
        return None
    #读取所有数据库
    query = "show databases"
    cursor.execute(query)
    _databases = cursor.fetchall()
    for file in files:
        try:
            database,data,cols_name = read_file(os.path.join(databases_dir,file))
        except Exception as e:
            raise e
            print(f'处理{file}出错！')
            continue
        if (database,) in _databases:
            print(f"数据库{database}已存在")
            continue
        # 创建数据库
        try:
            sql = "create database " + f"`{database}`"
            cursor.execute(sql)
        except Exception as e:
            print(f'创建数据库{database}失败!')
            continue
        
        print(f'数据库{database}创建成功!')
        sql = 'use ' + f"`{database}`"
        cursor.execute(sql)
        for table_name in data:
            try:
                sql = "drop table if exists " + f"{table_name}"
                cursor.execute(sql)
                #创建表
                sql = f'create table `{table_name}` (`id` int not null auto_increment, '
                for col in cols_name[table_name]:
                    sql += f'`{col}` varchar(45),'
                sql += 'primary key (`id`) )'
                try:
                    cursor.execute(sql)
                except Exception  as e:
                    print(f'创建表{table_name}失败！')
                    continue
                else:
                    print(f'创建表{table_name}成功！')
                #写入数据 row是某一个表的一行数据
                for i,rows in enumerate(data[table_name]):
                    
                    #插入数据库
                    base_sql = f"insert into `{table_name}` ("
                    for col in cols_name[table_name]:
                        base_sql += f"`{col}`,"
                    base_sql = base_sql[:-1]
                    base_sql += ") values ("
                    sql = ""
                    for d in rows:
                        d = d.replace("'","\\'")
                        sql += f"'{d}'," #机场信息里面带有"'"
                    sql = sql[:-1]
                    sql += ")"
                    try : 
                        #插入一条数据
                        cursor.execute(base_sql+sql)
                    except Exception as e:
                        raise e
                        break
                    else:
                        print(f'表{table_name}已完成{int((i+1)/len(data[table_name])*100)}%',end='\r')
            except Exception as e:
                print(f'表{table_name}插入数据失败！')
        try:
            connection.commit()
        except Exception as e:
            print(f"数据库{database}:表{table_name} 插入数据失败！")
            connection.rollback()
    connection.close()


if __name__ == '__main__':
    dump_to_db()