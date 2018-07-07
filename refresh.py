#定时刷新
import utils
import database
import webbot
#新浪微博的刷新·每半小时执行一次

def refresh_sina_blog():
    #重新执行add_blog方法id和uid从数据库中获取
    print('更新数据')
    key = utils.get_stored_key()
    #获得UID以及刷新
    for i in key:
        uid_list = utils.get_stored_uid(i)
        print(uid_list)
        for j in uid_list:
            print("key:"+i+"uid:" + j)
            webbot.follow_weibo(i,j)
refresh_sina_blog()