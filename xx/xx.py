#! /usr/bin/env python
# -*- coding: utf-8 -*-
# __author__ = "Q1mi"
# Date: 2017/11/29

class RedisCache:
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(RedisCache, cls).__new__(cls, *args, **kwargs)
        return cls._instance

class RedisCaches(RedisCache):

    def __init__(self,*args,**kwargs):
        import redis

        pool = redis.ConnectionPool(host='192.168.16.83', port=6379)

        self.conn = redis.Redis(connection_pool=pool)

    def set(self,name, key, value):
        self.conn.hset(name, key, value)

    def get(self,name,key):
        return self.conn.hget(name,key)

    def delete(self,name,*keys):
        self.conn.hdel(name,*keys)


caches = RedisCaches()
if __name__ == '__main__':
    import redis

    pool = redis.ConnectionPool(host='192.168.16.83', port=6379)

    conn = redis.Redis(connection_pool=pool)

    conn.hset('k1','k2','v')
    print(conn.hget('k1','k2'))


