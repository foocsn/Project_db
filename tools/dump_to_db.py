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
        




if __name__ == '__main__':
	files = _read_files(databases_dir)
	print(files)
