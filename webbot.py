import requests
import database
from lxml import html
import re
'''
网络爬虫部分
'''

#使用get的header参数伪装成浏览器
header = {'Referer':'https://m.weibo.cn/?sudaref=www.google.com&display=0&retcode=6102&sudaref=graph.qq.com','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','Accept-Encoding':'gzip, deflate','Accept-Language':'zh-CN,zh;q=0.9','Cache-Control':'max-age=0','Connection':'keep-alive','User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}

'''
板块一:排行榜
数据表格式
ID,排行榜类别，排行榜榜单，排名，标题，链接
每天一更新
'''
def musicbot_clooud():
    '''  print("音乐机器人开始工作")
        #网易云音乐四个榜单urlc1,urlc2...
        #云音乐飙升榜
        urlc1 = 'http://music.163.com/discover/toplist?id=19723756'
        #云音乐新歌榜
        urlc2 = 'http://music.163.com/discover/toplist?id=3779629'
        #网易原创歌曲榜
        urlc3 = 'http://music.163.com/discover/toplist?id=2884035'
        #云音乐热歌榜
        urlc4 = 'http://music.163.com/discover/toplist?id=3778678'
        url = cloud_music[nu]

    '''
    nu = 0
    while nu < 4:
        source = '网易云音乐'
        if nu == 0:
            url = 'http://music.163.com/discover/toplist?id=19723756'
            music_list_name = '云音乐飙升榜'
        elif nu == 1:
            url = 'http://music.163.com/discover/toplist?id=3779629'
            music_list_name = '云音乐新歌榜'
        elif nu == 2:
            url = 'http://music.163.com/discover/toplist?id=3778678'
            music_list_name = '网易原创歌曲榜'
        else:
            url = 'http://music.163.com/discover/toplist?id=3778678'
            music_list_name = '云音乐热歌榜'

        nu+=1
        page = requests.get(url,headers=header,timeout = 30)
        tree = html.fromstring(page.text)
        #print(page.text)
        rank_list = tree.xpath('//textarea[@id="song-list-pre-data"]/text()')
        rank_list =str(rank_list[0])
        #正则表达式处理
        result = rank_list[1:len(rank_list)-1]
        name_result = re.findall('"album":{"id":.*?,"name":"(.*?)"',rank_list)
        link_result = re.findall('"picUrl":"(.*?)"',rank_list)
        singer_result = re.findall('"artists":\[{"id":.*?,"name":"(.*?)"',rank_list)
        #http://music.163.com/#/song?id=574919767
        song_result = re.findall('"id":(\d*?),"pl"',rank_list)
        rank_result = []
        n = 1
        m = 0
        while m < len(song_result):
            rank_result.append(m+1)
            m+=1
        print(len(song_result))
        print(len(link_result))
        print(len(name_result))
        print(len(singer_result))
        print(len(rank_result))
        j = 1
        song_link = []
        for i in song_result:
            s = 'http://music.163.com/#/song?id=' + i
            song_link.append(s)
        database.add_song(source, music_list_name, rank_result, name_result, singer_result, song_link, link_result)
'''
qq音乐榜

    QQ音乐榜单
    流行指数榜
    https://y.qq.com/n/yqq/toplist/4.html#stat=y_new.toplist.menu.4
'''

def musicbot_kgmusic():
    qn = 0
    source = '酷狗音乐'
    while qn < 3:
        if qn == 0:
            url = 'http://www.kugou.com/yy/rank/home/1-6666.html?from=rank'
            music_list_name = '酷狗飙升榜'
            qn = 3
        elif qn == 1:
            url = 'http://www.kugou.com/yy/rank/home/1-22603.html?from=rank'
            music_list_name = '5sing音乐榜'
        else:
            url = 'http://www.kugou.com/yy/rank/home/1-33164.html?from=rank'
            music_list_name = '纯音乐榜'
        qn+=1
        page = requests.get(url,headers=header)
        tree = html.fromstring(page.text)
        print(page.text)


#微博跟踪 用户ID，博主主页url
def follow_weibo():
    url = 'https://m.weibo.cn/u/1879778060?uid=1879778060&luicode=20000174'
    page=requests.get(url,headers=header)
    print(page.text)


follow_weibo()
