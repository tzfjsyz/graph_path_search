#coding:utf-8
#配置文件
class BasicInfoConfig():

    #neo4j server连接信息
    neo4j_server_info = {
        'neo4j_server_uri': "bolt://10.10.15.27:7687",
        'neo4j_server_user': "neo4j",
        'neo4j_server_password': "123456"
        }

    #定时任务设置信息
    timing_update_data_info = {
        'day_of_week': '0-6',
        'hour': 17,
        'minute': 55
    }