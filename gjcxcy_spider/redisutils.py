# -- coding: UTF-8 --
import redis
import gjcxcy_spider.settings as st


def connect_redis_pool():
    pool = redis.ConnectionPool(host=st.REDIS_HOST, port=st.REDIS_PORT, max_connections=st.REDIS_MAX_CONNECTION, )
    conn = redis.Redis(connection_pool=pool, decode_responses=True, charset='UTF-8', encoding='UTF-8')
    return conn
