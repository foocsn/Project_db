#!bash/bin/python
#__auth__ = kevin
#Date 2020/5/26

#
# ********...开头的是header
# summary开头的是总表，列出表名字 table_list
# 从table_list中找出不同的表明
# match方式：表名 + 下一行是 ---------固定长度
# 表的列名
# 数据

"""
注意：读取cvs文件，在第6行“Report compiled on 星期四 五月 14 2020”有可能会出错，utf-8无法解码！
"""
import csv
import re
import logging



#读取一个csv文件
def read_file(csv_filename):
    """
    paras: csv_filename
    returns: database + data +column's name
    """
    
    database = csv_filename[-14:-11] #数据库名称
    print(f'正在读取{csv_filename}...')
    data = {} #数据
    cols_name = {} #列名
    now = None
    # summary = {}
    b = False #数据块开始标志
    try:
        with open(csv_filename,'r')  as f:
            try:
                reader = csv.reader(f,delimiter=',')
                [next(reader) for _ in range(20)]

                reader = list(reader)
            except Exception as e:
                raise e
                print(f'读取csv文件{csv_filename}出错！(有可能是编码错误！)')
                return None
            for i,row in enumerate(reader):
                #已经在读数据
                if b and now!=None:
                    #结束读取
                    if row[0] == '' or re.match(r'<<<.*',row[0]):
            
                        b = False
                        now = None
                        print(f'已完成{int(i/len(reader)*100)}%',end='\r')
                        # print(f'已完成{csv_filename}中的表{now}',flush=True)
                        # print('\r')
                        continue
                    #已经获取了列
                    data[now].append(row[:len(cols_name[now])-1]+['series'])
                
                #还没有获取数据
                else:
                    if now == None:
                        if row!=[] and row[0] =='-------------------------':
                            now = reader[i-1][0]
                            now = now.replace(' ','_')
                            cols_name[now] = []
                            continue
                    else:
                        for r in row:
                            if r != '':
                                cols_name[now].append(r)
                            else:
                                cols_name[now].append('Database')
                                break
                        b = True
                        data[now] = []
    except Exception as e:
        raise e
        return None
    print(f'读取{csv_filename}完成！')
    return database,data,cols_name
            
if __name__ == '__main__':
    database,data,cols_name=read_file('/Users/likevin/Desktop/Project_db/Database/CZ72006001.csv')
    print(data['Airports'][0])
    # print(data['Airports'][0])
    # print(cols_name['Airports'])