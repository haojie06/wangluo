import re
import pymysql
import time
'''
新浪微博时间处理
将一个小时内发的微博（多少分钟前）转为XX月XX日XX时XX分的格式
如 07-23 12:06
'''
def deal_with_time(current_time,push_time):
    new_list = []
    for t in push_time:
        t = t.split('\xa0')[0]
        if '分钟前' in t:
            num = int(re.findall("(.*?)分钟前",t)[0])
            div = current_time.split(' ')
            date1= div[0]
            time1 = div[1]
            minute = time1.split(':')[1]
            hour = time1.split(':')[0]
            cur_min = int(minute) - int(num)
            if cur_min < 0:
                hour = str(int(hour)-1)
                cur_min = str(60 + cur_min)
            elif cur_min < 10:
                cur_min = '0' + str(cur_min)
            result_time = div[0] + ' ' + str(hour) + ':' + str(cur_min)
            t = result_time
            #print(t)

        elif '今天' in t:
            date = current_time.split(' ')[0]
            t = t.replace('今天', date)
            #print(t)
        elif '刚刚' in t:
            t = current_time
            #print(t)
        elif '月' in t:
            t = t.replace('月','-').replace('日','')
            #print(t)
        new_list.append(t)
    return new_list

#生成板块二中用户需要的钥匙
def get_new_key():
    key_list = []
    db = pymysql.connect('localhost','root','haojie06',charset='utf8')
    cursor = db.cursor()
    cursor.execute('USE bot_db')
    cursor.execute('SELECT DISTINCT user_id FROM sina_blog_tb ORDER BY user_id')
    keyl = cursor.fetchall()
    for i in keyl:
        key_list.append(i[0])
    new_key = int(key_list[-1]) + 1
    return str(new_key)

def get_stored_key():
    key_list = []
    db = pymysql.connect("localhost", "root", "haojie06", charset="utf8")
    cursor = db.cursor()
    cursor.execute("USE bot_db")
    cursor.execute('SELECT DISTINCT user_id FROM sina_blog_tb')
    keyl = cursor.fetchall()
    for i in keyl:
        key_list.append(i[0])
    print(key_list)
    return key_list
    #ge = deal_with_time('07-06 12:13',['今天 11:32','5分钟前','刚刚','07月05日 22:00','34分钟前\xa0来自微博 weibo.com'])

def get_stored_uid(key):
    uid_list = []
    db = pymysql.connect("localhost", "root", "haojie06", charset="utf8")
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
    return new_list
deal_with_time_zhihu(['14 天前', '15 天前', '16 天前', '19 天前', '20 天前', '21 天前', '23 天前', '24 天前', '25 天前', '27 天前', '1 个月前', '1 个月前', '2 个月前', '2 个月前'])
