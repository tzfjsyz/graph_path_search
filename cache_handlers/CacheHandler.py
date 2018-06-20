#coding:utf-8
#处理redis相关连接信息, wrote by tzf, 2018/5/21
import json
from config.DataSource import get_data_engine

#r = redis.StrictRedis(host='10.15.97.135', port=6679, password='finchina', db=4)
#print('resdis connect info: ', r)

class CacheHandler(object):

    def __init__(self):
        self.__engine = get_data_engine('TIMESTAMP')
        pass

    def save_context(self, id, ctx):
        ctx_id = 'ctx_{}'.format(id)
        res = self.__engine.set(ctx_id, json.dumps(ctx))
        print('set ctx_id: {} to redis info: {}'.format(ctx_id, res))
        return res

    def get_context(self, id):
        ctx_id = 'cxt_{}'.format(id)
        res = self.__engine.get(ctx_id)
        if (res):
            return json.dumps(res)
        else:
            return {}
