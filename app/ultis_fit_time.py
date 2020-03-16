import datetime
import time

def dt_to_secs(dt):
    #dt = "2019-11-15 00:03:53"
    # 转换成时间数组
    timeArray = time.strptime(dt, "%Y-%m-%d %H:%M:%S")
    # 转换成时间戳
    secs = time.mktime(timeArray)
    return secs

def secs_to_dt(secs):
    dt = datetime.datetime.fromtimestamp(secs)
    return dt

#utc时间修改为当地时间,timezone单位s
def utc_dt_to_dt(dt, tz):
    return secs_to_dt(dt_to_secs(dt) + float(tz))