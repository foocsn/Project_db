#!bash/bin/python
#__auth__ = kevin
#Date 2020/5/26

import os
import sys
import pymysql
from readfile import read_file
import asyncio

root = os.getcwd()
databases_dir = os.path.join(root,'Database')

def _read_files(dir):
	try:
		files = os.listdir(databases_dir)
	except Exception as e:
		raise e
		return None
	finally:
		return files

def dump_to_db(files):
	connection = pymysql.connect(
		hos='',
		user='',
		password='',
		)
	cursor = con.cursor()
	files = _read_files(databases_dir)
	for file in files:
		database,data,cols_name = read_file(os.path.join(databases_dir,file))
		# 创建数据库
		try:
    		sql = 'create database if exists'+database
    		cursor.execute(sql)
        except Exception as e:
            print(f'创建数据库{database}失败')
            continue
        sql = 'use ' + database
        cursor.execute(sql)
        for table_name in data:
            #创建表
            sql = f'create table `{table_name}` (`id` int not null auto_increment, '
            for col in cols_name[table_name]:
                sql += f'`{col}` varchar(45),'
            sql += 'primary key (`id`) )'
            try:
                cursor.execute(sql)
            except Exception  as e:
                print(f'创建表{table_name}失败！')
                cursor.rollback()
                continue
            #写入数据
            for rows in data[table_name]:
                sql = f"insert into `{table_name}` ("
                for col in cols_name[table_name]:
                    sql += f"`{col}`,"
                sql += ") values ("
                for d in rows:
                    for index,i in enumerate(d):
                        sql += f"'{i}',"
                    sql += ')'
                    try : 
                        cursor.execute(sql)
                    except Exception as e:
                        print('插入数据失败！')
                        cursor.rollback()
                        break
        connection.commit()






if __name__ == '__main__':
	files = _read_files(databases_dir)
	print(files)
