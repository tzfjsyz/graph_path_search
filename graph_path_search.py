#coding:utf-8
import asyncio
import time
from aiohttp import web
from graph_search_handlers.path_search import PathSearch
from total_data_handlers.LoadTotalData import LoadTotalData
from cache_handlers.CacheHandler import CacheHandler
import json
from logging_handlers.MyLogger import MyLogger

mylogger = MyLogger().mylogger()


class Handler(object):

    def __init__(self):
        pass

    async def handler_invest_path(self, request):
        #name = request.match_info.get('code', "invest_path")
        #txt = "Hello, {}".format(name)
        code = request.rel_url.query['code']
        depth = request.rel_url.query['investPathDepth']
        pathsearch = PathSearch()
        path_result = pathsearch.outbound_path_search(code, depth)
        return web.json_response(path_result)

    async def handler_investedby_path(self, request):
        code = request.rel_url.query['code']
        depth = request.rel_url.query['investedByPathDepth']
        pathsearch = PathSearch()
        path_result = pathsearch.inbound_path_search(code, depth)
        return web.json_response(path_result)

    async def handler_update_total_data(self, request):
        flag = request.rel_url.query['flag']
        if not flag:
            flag = 1
        loadtotaldata = LoadTotalData()
        #全量更新数据, 初始化timestamp
        id = 'invest_update'
        ctx = {};
        ctx['last'] = 0
        ctx['updatetime'] = time.time()
        ctx['lasestUpdated'] = 0
        cachehandler = CacheHandler()
        cachehandler.save_context(id, ctx)
        print('init timestamp info: {}'.format(json.dumps(ctx)))
        #开始全量更新数据
        loadtotaldata.load_invest_relation(flag)
        return web.json_response({'ok': 1, 'result': 'update total data ...'})

async def start_server(loop):
    app = web.Application(loop=loop)
    handler = Handler()
    # app.add_routes([
    #     web.get('/queryInvestPath', handler.handler_invest_path)
    # ])
    app.router.add_get('/queryInvestPath', handler.handler_invest_path)
    app.router.add_get('/queryInvestedByPath', handler.handler_investedby_path)
    app.router.add_get('/updateTotalData', handler.handler_update_total_data)
    srv = await loop.create_server(app.make_handler(), '127.0.0.1', 8390)
    print('graph path search server API is running at http://127.0.0.1:8390')
    mylogger.info('graph path search server API is running at http://127.0.0.1:8390')
    return srv

loop = asyncio.get_event_loop()
loop.run_until_complete(start_server(loop))
loop.run_forever()

