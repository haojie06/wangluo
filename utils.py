import re
import pymysql
import time
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import fake_useragent
'''
新浪微博时间处理
将一个小时内发的微博（多少分钟前）转为XX月XX日XX时XX分的格式
如 07-23 12:06
'''
def deal_with_time(current_time,push_time):

    cur_hour = current_time.split(' ')[1].split(':')[0]
    cur_min = current_time.split(' ')[1].split(':')[1]
    cur_mon = current_time.split(' ')[0].split('-')[0]
    cur_day = current_time.split(' ')[0].split('-')[1]
    new_list = []
    for t in push_time:
        if '分钟前' in t:
            hour = cur_hour
            minu = t.split('分钟前')[0]
            real_minute = int(cur_min) - int(minu)
            if real_minute < 0:
                hour = '23'
                real_minute = str(60 + real_minute)
            elif real_minute < 10:
                real_minute = '0' + str(real_minute)
            t = cur_mon + '-' + cur_day + ' ' + hour + ':' + str(real_minute)
        elif '小时前' in t:
            hou = t.split('小时前')[0]
            real_hour = int(cur_hour) - int(hou)
            if real_hour < 0:
                day = str(int(cur_day) - 1)
                real_hour = str(24 + real_hour)
            elif real_hour < 10:
                real_hour = '0' + str(real_hour)
            t = cur_mon + '-' + cur_day + ' ' + str(real_hour) + ':' + cur_min
        elif '今天' in t:
            dat = current_time.split(' ')[0]
            t = t.replace('今天', dat)
        elif '刚刚' in t:
            t = current_time
        elif '昨天' in t:
            if int(cur_hour) < 10:
                cur_hour = '0' + str(cur_hour)
            if int(cur_min) < 10:
                cur_min = '0' + str(cur_min)
            d = str(int(cur_day) - 1)
            tim = t.split(' ')[1]
            if int(d) < 10:
                t = cur_mon + '-' + '0'+ d + ' ' + tim
            else:
                t = cur_mon + '-' + d + ' ' + tim
        new_list.append(t)
    return new_list

#生成板块二中用户需要的钥匙


def get_stored_key():
    key_list = []
    db = pymysql.connect("localhost", "webbot", "webbot", charset="utf8")
    cursor = db.cursor()
    cursor.execute("USE bot_db")
    cursor.execute('SELECT user_key FROM keys_tb ORDER BY user_key')
    keyl = cursor.fetchall()
    for i in keyl:
        key_list.append(i[0])
    return key_list
    #ge = deal_with_time('07-06 12:13',['今天 11:32','5分钟前','刚刚','07月05日 22:00','34分钟前\xa0来自微博 weibo.com'])

def get_stored_uid_sina(key):
    uid_list = []
    db = pymysql.connect("localhost", "webbot", "webbot", charset="utf8")
    cursor = db.cursor()
    cursor.execute("USE bot_db")
    sql = 'SELECT DISTINCT follow_uid FROM sina_blog_tb WHERE user_id="%s"' % (key)
    cursor.execute(sql)
    data = cursor.fetchall()
    print(cursor.fetchall())
    for j in data:
        uid_list.append(j[0])
    print(uid_list)
    return uid_list
#get_stored_key()
#get_stored_uid('1')

def get_stored_uid_zhihu(key):
    uid_list = []
    db = pymysql.connect("localhost", "webbot", "webbot", charset="utf8")
    cursor = db.cursor()
    cursor.execute("USE bot_db")
    sql = 'SELECT DISTINCT follow_uid FROM zhihu_tb WHERE user_key="%s"' % (key)
    cursor.execute(sql)
    data = cursor.fetchall()
    for j in data:
        uid_list.append(j[0])
    print(uid_list)
    cursor.close()
    db.close()
    return uid_list
#输入 起点中文网，腾讯视频，腾讯漫画获得各自的所有
def get_stored_uid_media(key,type):
    uid_list = []
    db = pymysql.connect("localhost", "webbot", "webbot", charset="utf8")
    cursor = db.cursor()
    cursor.execute("USE bot_db")
    sql = 'SELECT DISTINCT follow_uid FROM follow_media_tb WHERE source="%s" AND user_key="%s"' % (type,key)
    cursor.execute(sql)
    data = cursor.fetchall()
    for j in data:
        uid_list.append(j[0])
    return uid_list

#get_stored_key()
#get_stored_uid('1')


def deal_with_time_zhihu(time_list):
    new_list = []

    for t in time_list:
        current_time = time.strftime("%m-%d %H:%M", time.localtime())
        div = current_time.split(' ')
        date = div[0].split('-')
        tim = div[1].split(':')
        hour = tim[0]
        minute = tim[1]
        day = date[1]
        month = date[0]
        if '小时前' in t:
            h = t.split('小时前')[0]
            #print(str(hour) + '-' + str(h))
            hour = int(hour) - int(h)
            #print(str(hour))
            if hour < 0:
                day = str(int(day) - 1)
                hour = str(24 + hour)
            if int(hour) < 10:
                hour = '0' + str(hour)
            hour = str(hour)
            new_time = month + '-' + day +' ' + hour + ':' + tim[1]
            new_list.append(new_time)
        elif '分钟前' in t:
            m = t.split('分钟前')[0]
            #print(str(minute) + '-' + str(m))

            minute = int(minute) - int(m)
            if minute < 0:
                hour = str(int(hour) - 1)
                minute = str(60 + minute)
            if int(minute) < 10:
                minute = '0' + str(minute)
            minute = str(minute)
            new_time = month + '-' + day + ' ' + hour + ':' + minute
            new_list.append(new_time)
        elif '天前' in t:
            d = t.split('天前')[0]
            day = str(int(day) - int(d))

            if int(day) < 0:
                month = str(int(month) - 1)
                day = str(30 + int(day))
            if int(day) < 10:
                day = '0'+day
            new_time = month + '-' + day
            new_list.append(new_time)
        elif '月前' in t:
            m = t.split('个月前')[0]
            month = str(int(month) - int(m))
            if(int(month) < 10):
                month = '0' + month

            new_time = month + '-' + day
            new_list.append(new_time)
        elif '天' in t:
            tim = t.split(' ')[1]
            day = str(int(day) - 1)
            if int(day) < 0:
                month = str(int(month) - 1)
                day = '30'
            if int(day) < 10:
                day = '0'+day
            new_time = month + '-' + day + ' ' + tim
            new_list.append(new_time)

    return new_list

def get_webdriver():
    #不加载图片
    ua = fake_useragent.UserAgent()
    #设置请求头
    dcap = dict(DesiredCapabilities.PHANTOMJS)
    dcap["phantomjs.page.settings.userAgent"] = (ua.chrome)
    # 请求头生效
    SERVICE_ARGS = ['--load-images=false', '--disk-cache=true', '--ignore-ssl-errors=true']
    driver = webdriver.PhantomJS(desired_capabilities=dcap,service_args=SERVICE_ARGS)
    return driver

#deal_with_time_zhihu(['昨天 23:00','46分钟前'])
