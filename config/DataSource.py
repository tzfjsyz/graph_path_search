#coding:utf-8
#配置数据库连接信息, wrote by tzf, 2018/5/21

URL = 'URL'
DTYPE = 'DTYPE'
OBJ = 'OBJ'
HOST='HOST'
PORT='PORT'
DB='DB'
AUTH='AUTH'

SQLALCHEMY = 1
REDIS = 2

__DATABASE = {
    'CRDB': {
        URL: 'mssql+pymssql://app:app127@10.10.15.44/CRDB',
        DTYPE: SQLALCHEMY
    },
    'TIMESTAMP': {
        HOST: '10.15.97.135',
        PORT: 6679,
        AUTH: 'finchina',
        DB: 4,
        DTYPE: REDIS
    }
}

def __getSqlAlchemyEngine( source ):
    if not OBJ in __DATABASE[source].keys():
        import sqlalchemy as sa
        __DATABASE[source][OBJ] = sa.create_engine( __DATABASE[source][URL] )

    return __DATABASE[source][OBJ]

def __getRedisConn( source ):
    import redis
    if not OBJ in __DATABASE[source].keys():
        if AUTH in __DATABASE[source].keys():
            __DATABASE[source][OBJ] = redis.ConnectionPool( host=__DATABASE[source][HOST],
                                                            port=__DATABASE[source][PORT],
                                                            password=__DATABASE[source][AUTH],
                                                            db=__DATABASE[source][DB]
                                                            )
        else:
            __DATABASE[source][OBJ] = redis.ConnectionPool( host=__DATABASE[source][HOST],
                                                            port=__DATABASE[source][PORT],
                                                            db=__DATABASE[source][DB]
                                                            )
    conn = redis.Redis(connection_pool=__DATABASE[source][OBJ])
    return conn

def get_data_engine( source ):
    engine = None
    if source in __DATABASE.keys():
        if __DATABASE[source][DTYPE] == SQLALCHEMY:
            return __getSqlAlchemyEngine( source )
        elif __DATABASE[source][DTYPE] == REDIS:
            return __getRedisConn( source )
    else:
        raise Exception('未知数据源！')
    return engine


# if __name__ == "__main__":
#     db_engine = get_data_engine("CRDB")
#     print (db_engine)
#     print ('---->')