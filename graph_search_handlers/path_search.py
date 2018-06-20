#coding:utf-8
#对外投资和股东关系的路径查找, wrote by tzf, 2018/5/11
import time
from logging_handlers.MyLogger import MyLogger

mylogger = MyLogger().mylogger()
print('path_search logger is start: ', 'ok')
mylogger.info('mylogger ...')

class PathSearch():

    #对外投资路径
    @staticmethod
    def outbound_path_search(code, depth):
        start_time_outbound = time.time()
        '''
        ountbound path查找和组装返回数据格式
        '''
        outbound_path_result = {
                                  'code': '1234567890',
                                  'results': [
                                      {'sourceCode': 1234567890,
                                       'sourceName': '上海大智慧股份有限公司',
                                       'sourceRegFund': 1234444444,
                                       'shareholdRatio': 100,
                                       'targetCode': 4566777888,
                                       'targetName': '大智慧财汇数据',
                                       'targetRegFund': 47558,
                                       }
                                       ],
                                  'pathNum': 1,
                                  'pathType': 0,
                                  'pathName': 'investPath'
                                  }
        time_cost_outbound = time.time() - start_time_outbound
        print('code: {}, investPathDepth: {}, search the outbound path time cost: {} ms'.format(code, depth, time_cost_outbound))
        mylogger.info('code: %s, investPathDepth: %s, search the outbound path time cost: %s ms', code, depth, time_cost_outbound)
        return outbound_path_result

    #股东关系路径
    @staticmethod
    def inbound_path_search(code, depth):
        start_time_inbound = time.time()
        '''
        inbound path查找和组装返回数据格式
        '''
        inbound_path_result = {
                                  'code': '1234567890',
                                  'results': [
                                      {'sourceCode': 1234567890,
                                       'sourceName': '上海大智慧股份有限公司',
                                       'sourceRegFund': 1234444444,
                                       'shareholdRatio': 100,
                                       'targetCode': 4566777888,
                                       'targetName': '大智慧财汇数据',
                                       'targetRegFund': 47558,
                                       }
                                       ],
                                  'pathNum': 1,
                                  'pathType': 1,
                                  'pathName': 'investedByPath'
                                  }
        time_cost_inbound = time.time() - start_time_inbound
        print('code: {}, investedByPathDepth: {}, search the inbound path time cost: {} ms'.format(code, depth, time_cost_inbound))
        mylogger.info('code: %s, investedByPathDepth: %s, search the inbound path time cost: %s ms', code, depth, time_cost_inbound)
        return inbound_path_result