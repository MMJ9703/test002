# 添加所需要的库
import os
# 添加自己编写的算法
from Import_data import mainf
from read_data import read_xml
from DWPB_denoising import DWPB
# Web应用程序设置
from flask_executor import Executor
import pandas as pd
from threading import Thread

from sqlalchemy import create_engine


from flask import Flask
application = Flask(__name__)
executor = Executor(application)
# 获取mysql环境变量
env = os.environ
# MYSQL_URI   mysql+pymysql://test:test@172.30.238.185:3306/test
mysql_uri = env.get('MYSQL_URI')

sqlEngine = create_engine(mysql_uri, pool_recycle=3600)

print ('=== mysql uri: ' + mysql_uri)

# rest  api（应用执行端口）
@application.route('/')
def hello():
    executor.submit(threaded_task,'data')
    return b'mainf '

@application.route('/api')
def hello1():
    executor.submit(threaded_task,'data')
    return b'mainf '
if __name__ == '__main__':

    application.run()

def threaded_task(data):  
    try:

        print ('===== run task')

        # 机组信息
        ID = 150817080435211
        # tpye = 'vib'
        Input_Time = '2020-6-20 00:00:00'
        days = 1
        #ID,Input_Time,days = read_xml()
        # 算法执行
        mainf(ID, Input_Time, days, sqlEngine)
        #table_name_1 = 'id'+str(ID)+'pt_'+tpye
        #data_1 = pd.read_sql("select * from  "+table_name_1 , con=sqlEngine, index_col=None)

        #data_1['Time'] = pd.to_datetime(data_1['Time'],format='%Y-%m-%d %H:%M:%S')
        #data_1 = data_1.set_index('Time')
        #data_1 = data_1.dropna()
        #clean_data= DWPB('db8',3).denoising_process(data_1)

        # 将数据写入mysql数据库中，设置查询pd.to_sql()函数
        #table_name_2 =  'clean_data_'+'id'+str(ID)+'pt_'+tpye
        #data_1.to_sql(table_name_2, con=sqlEngine, if_exists='replace', index=True)
        

    except Exception as e:
        print ('===error===')
        print (e)
        raise e
    return True
