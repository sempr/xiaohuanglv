from redis import Redis
from rq.decorators import job

import os

__author__ = 'Sempr'

my_redis_conn = Redis()

@job('low',connection=my_redis_conn)
def add(g,x,y):
    print 'PID: ',os.getpid()
    print 'g=%d %d+%d=%d'%(g,x,y,x+y)
    return x+y

