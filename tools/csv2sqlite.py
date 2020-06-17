#sqlite version
#onlyfor airwayfixs part
#left databases are under development...

import os
import sqlite3
import configparser
import json
import re
from readfile import read_file

#确定基础文件是否存在（tableResult.json，相应的db文件）
root = os.getcwd()
databases_dir = os.path.join(root,'Database')
#读取json文件
try:
    with open(os.path.join(root,"config","tableResult.json"),"r") as f:
        tables_cols = json.load(f)
except Exception as e:
    print(f"读取tableResult.json文件失败，请检查")
    raise e
#读取csv文件    
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

class csv2sqlite():
    def __init__(self,database,part):
        self.database = os.path.join(databases_dir,database)
        self.part  = part
        try:
            self.cols = tables_cols[self.part]
        except Exception as e:
            print(f"检查是否存在{self.part}")
            raise e
        if not os.path.exists(self.database):
            raise AttributeError(f"{database}不存在，请检查")
        else:
            self.connection = sqlite3.connect(self.database)
            self.cursor = self.connection.cursor()
            #显示是否存在需要的表
            self.cursor.execute(f"select name from sqlite_master where type='table'")
            self.tables = self.cursor.fetchall()
            print(self.tables)
            #开发版本
            if (self.part,) in self.tables:
                self.cursor.execute(f"drop table if exists {self.part};")
                self.cursor.execute(f"select name from sqlite_master where type='table'")
                self.tables = self.cursor.fetchall()
                print(self.tables)
            #使用版本
            if self.part in self.tables:
                print(f"已存在{self.part}表")
            else:
                #创建表
                base_sql = f'''CREATE TABLE {self.part} (ID TEXT PRIMARY KEY NOT NULL,'''
                for col in self.cols:
                    base_sql += f'''"{col}"''' + ''' TEXT,'''
                base_sql += '''series TEXT);'''
                print(base_sql)
                try :
                    self.cursor.execute(base_sql)
                except Exception as e:
                    print(f"创建表{self.part}出错！")
                    raise e
                else:
                    self.cursor.execute(f"select * from sqlite_master where type='table' and name='{self.part}';")
                    print(self.cursor.fetchall())

    def _read_csv(databases_dir=databases_dir):

        
        
if __name__ == '__main__':
    c2sqlite = csv2sqlite("honeywell.db","AirwayFixes")