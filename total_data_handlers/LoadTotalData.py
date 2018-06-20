#coding:utf-8
#从数据库获取全量数据, wrote by tzf, 2018/5/18
from config.DataSource import get_data_engine
from cache_handlers.CacheHandler import CacheHandler
import time
import sys
import json
import pandas as pd
from logging_handlers.MyLogger import MyLogger

mylogger = MyLogger().mylogger()

from apscheduler.schedulers.blocking import BlockingScheduler
from config.BasicInfoConfig import BasicInfoConfig
basicinfoconfig = BasicInfoConfig()
DAY_OF_WEEK = basicinfoconfig.timing_update_data_info['day_of_week']
HOUR = basicinfoconfig.timing_update_data_info['hour']
MINUTE = basicinfoconfig.timing_update_data_info['minute']
print('scheduler job info -- day_of_week: {}, hour: {}, minute: {}'.format(DAY_OF_WEEK, HOUR, MINUTE))

#定时任务触发全量数据更新
def timingUpdateDataJob():
    # 全量更新数据, 初始化timestamp
    id = 'invest_update'
    ctx = {};
    ctx['last'] = 0
    ctx['updatetime'] = time.time()
    ctx['lasestUpdated'] = 0
    cachehandler = CacheHandler()
    cachehandler.save_context(id, ctx)
    print('init timestamp info: {}'.format(json.dumps(ctx)))
    # 开始全量更新数据
    loadtotaldata = LoadTotalData()
    loadtotaldata.load_invest_relation(1)

# 定时器信息设置
"""
    date: 特定的时间点触发
    interval: 固定时间间隔触发
    cron: 在特定时间周期性地触发
"""
scheduler = BlockingScheduler()
scheduler.add_job(timingUpdateDataJob, 'cron', day_of_week=DAY_OF_WEEK, hour=HOUR, minute=MINUTE)
# scheduler.start()

class LoadTotalData(object):

    def __init__(self):
        self.__engine = get_data_engine('CRDB')
        pass

    def load_invest_relation(self, flag):
        if flag == 1:
            try:
                cachehandler = CacheHandler()
                id = 'invest_update'
                rw_times = 0
                ctx = cachehandler.get_context(id)
                if 'last' not in ctx:
                    ctx['last'] = 0
                result_count = 0
                start_time = time.time()
                csv_file_path = '../graph_path_search/dataSet/invest.csv'
                file = open(csv_file_path, "w+")
                line_one = '_from,_to,weight\n'
                file.write(line_one)
                while True:
                    now = time.time()
                    sql = "select top 10000 cast(tmstamp as bigint) as _ts,ITCode2,CR0002_011,CR0002_004 " \
                          "from [tCR0002_V2.0] WITH(READPAST) " \
                          "where flag<> 1 and CR0002_004 <= 100 and ITCode2 is not null and CR0002_011 is not null and " \
                          "tmstamp > cast( cast({} as bigint) as binary(8)) order by tmstamp".format(ctx['last'])
                    rows = pd.read_sql(sql, self.__engine)
                    query_cost = time.time() - now
                    fetched = len(rows)
                    if fetched > 0:
                        result_count += fetched
                        for index in range(fetched):
                            _from = rows._values[index][2]
                            _to = rows._values[index][1]
                            weight = rows._values[index][3]
                            file.write('{},{},{}\n'.format(_from, _to, weight))
                        ctx['last'] = rows._values[fetched - 1][0]
                        ctx['updatetime'] = now
                        ctx['lasestUpdated'] = result_count
                        cachehandler.save_context(id, ctx)
                        rw_times += 1
                        print('read and write table [tCR0002_v2.0>] query_cost: {} ms, fetched: {} 条记录, rw_times: {} 次'.format(query_cost, fetched, rw_times))
                        mylogger.info('read and write table [tCR0002_v2.0>] query_cost: {} ms, fetched: {} 条记录, rw_times: {} 次'.format(query_cost, fetched, rw_times))
                        #for test
                        if rw_times == 3:
                            break;
                    if fetched < 10000:
                        break
                total_cost = time.time() - start_time
                file.close()
                update_status = 1
                update_info = 'read and write table [tCR0002_v2.0] query_total_cost:{} ms, result_count: {} records'.format(total_cost, result_count)
                print(update_info)
                mylogger.info(update_info)
                update_result = {'update_status': update_status, 'update_info': update_info}
                return update_result

            except IOError as e:
                print ("I/O error({0}): {1}".format(e.errno, e.strerror))
                mylogger.error("I/O error({0}): {1}".format(e.errno, e.strerror))
            except:
                print ("Unexpected error:", sys.exc_info()[0])
                mylogger.error("Unexpected error:", sys.exc_info()[0])
                raise
