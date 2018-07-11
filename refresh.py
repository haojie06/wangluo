#定时刷新
import utils
import database
import webbot
import time
from threading import Timer
#新浪微博的刷新·每半小时执行一次

#第二个板块都在这里刷新
def refresh_follow():
    #重新执行add_blog方法id和uid从数据库中获取
    print('更新微博与知乎关注')
    key = utils.get_stored_key()
    #获得UID以及刷新
    for i in key:
        uid_list_sina = utils.get_stored_uid_sina(i)
        print(uid_list_sina)
        for j in uid_list_sina:
            #print("key:"+i+"uid:" + j)
            webbot.follow_weibo(i,j)
            time.sleep(2)
    for i in key:
        uid_list_zhihu = utils.get_stored_uid_zhihu(i)
        print(uid_list_zhihu)
        for j in uid_list_zhihu:
            #print("key:" + i + "uid:" + j)
            webbot.follow_zhihu(i,j)
            time.sleep(2)
    Timer(2400,refresh_follow).start()


def refresh_media_follow():
    key_li = utils.get_stored_key()
    for m in key_li:
        media_li = ['腾讯视频', '起点中文网', '腾讯漫画']
        for n in media_li:
            # 重新执行add_blog方法id和uid从数据库中获取
            print('更新腾讯视频，起点中文，腾讯漫画')
            uid_li = utils.get_stored_uid_media(m,n)
            # 获得UID以及刷新
            for j in uid_li:
                    #print("key:" + str(m) + "uid:" + j)
                    if n == '腾讯视频':
                        webbot.follow_tecent_tv(str(m),j)
                    elif n == '起点中文网':
                        webbot.follow_qidian(str(m),j)
                    elif n == '腾讯漫画':
                        webbot.follow_tecent_anime(str(m),j)
                    else:
                        print("输入出错-------------")
                    #time.sleep(1)
    Timer(1800,refresh_media_follow).start()




def refresh_hot_news():
    webbot.weibo_top_list()
    webbot.baidu_top_list()
    webbot.tieba_top_list()
    Timer(120,refresh_hot_news).start()

def refresh_hot_medias():
    webbot.media_top_list()
    Timer(3600,refresh_hot_medias).start()

def refresh_music():
    webbot.cloudmusic_top_list()
    Timer(3800, refresh_hot_medias).start()


def refresh():
    #刷新微博与知乎关注内容
    refresh_follow()
    #刷新起点，腾讯漫画，腾讯视频关注
    refresh_media_follow()
    #刷新网易云
    refresh_music()
    #刷新热搜等榜单
    refresh_hot_news()
    #刷新娱乐，风云榜
    refresh_hot_medias()