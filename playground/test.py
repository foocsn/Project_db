import pymysql
import configparser
import os

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
try:
    connection = pymysql.connect(
    host='localhost',
    port=3306,
    user=db_username,
    password=db_password,
    )

    cursor = connection.cursor()

    query_sql = "show databases"
    cursor.execute(query_sql)
    a = cursor.fetchall()
    print(a)
finally:
    connection.close()