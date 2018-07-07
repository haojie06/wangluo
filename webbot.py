import requests
import database
from lxml import html
from lxml import etree
from lxml import *
import xml.etree.ElementTree as ET0
import time
from selenium import webdriver
import fake_useragent
import re
import utils
ua = fake_useragent.UserAgent()
headers = {}
headers['User-Agent'] = ua.chrome
headers['accept'] = 'pplication/json, text/plain, */*'

headers['accept-encoding'] = 'gzip, deflate, br'
'''
网络爬虫部分
'''
'Cookie: _T_WM=01e539a5a477285b40122ee5b2f48cdc; ALF=1533385329; SUB=_2A252On0hDeRhGeBL6VEU8izJzz-IHXVVxQNprDV6PUNbktANLUrzkW1NRyGJ8C4sQHikDLZudCCCe4ediAFKuMGr; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF08jFmZJXSxXhf6GsCzDUH5JpX5KzhUgL.FoqfeoefeozfShe2dJLoI7yQqgv3Ig-7Sntt; SUHB=0N2lX2ZE4pc2tE; MLOGIN=1; WEIBOCN_FROM=1110106030; M_WEIBOCN_PARAMS=luicode%3D20000174%26uicode%3D20000061%26fid%3D4226880611576753%26oid%3D4226880611576753'
#使用get的header参数伪装成浏览器
header = {'Cookie':'_T_WM=01e539a5a477285b40122ee5b2f48cdc; ALF=1533385329; SUB=_2A252On0hDeRhGeBL6VEU8izJzz-IHXVVxQNprDV6PUNbktANLUrzkW1NRyGJ8C4sQHikDLZudCCCe4ediAFKuMGr; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF08jFmZJXSxXhf6GsCzDUH5JpX5KzhUgL.FoqfeoefeozfShe2dJLoI7yQqgv3Ig-7Sntt; SUHB=0N2lX2ZE4pc2tE; MLOGIN=1; WEIBOCN_FROM=1110106030; M_WEIBOCN_PARAMS=luicode%3D20000174%26uicode%3D20000061%26fid%3D4226880611576753%26oid%3D4226880611576753','Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8','Accept-Encoding':'gzip, deflate','Accept-Language':'zh-CN,zh;q=0.9','Cache-Control':'max-age=0','Connection':'keep-alive','User-Agent':'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.118 Safari/537.36'}

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
def follow_weibo(user_id,uid):
    blog_link = "https://weibo.com/" + uid
    url='https://weibo.cn/' + uid
    page=requests.get(url,headers=header)
    print(page.text)
    tree = html.fromstring(page.content)
    user_head_pic = tree.xpath('//img[@alt="头像"]/@src')[0]
    article = []
    arti = tree.xpath('//div[@class="c"]/div/span[@class="ctt"]')
    blog_name = tree.xpath('//span[@class="ctt"]/text()')
    blog_name = blog_name[0]
    for i in arti:
        article.append(i.xpath('string(.)').strip())
    push_time = tree.xpath('//span[@class="ct"]/text()')
    # 发送请求后获得的时间
    current_time = tree.xpath('//div[@class="b"]/text()')[0]
    current_time = re.findall("\[(.*?)]",current_time)[0]
    push_time = utils.deal_with_time(current_time,push_time)

    print(article)
    print(len(article))
    print(push_time)
    database.add_weibo(user_id,'新浪微博',user_head_pic,uid,blog_name,blog_link,article,push_time)


def follow_zhihu(user_id,uid):
    key = user_id
    headers = {}
    headers['User-Agent'] = ua.chrome
    # 设置不加载图片
    SERVICE_ARGS = ['--load-images=false', '--disk-cache=true', '--ignore-ssl-errors=true']
    follow_link = people_link = 'https://www.zhihu.com/people/' + uid + '/activities'
    driver = webdriver.PhantomJS(desired_capabilities=headers, service_args=SERVICE_ARGS)
    driver.get(follow_link)  # 加载网页
    data = driver.page_source  # 获取网页文本
    print(data)
    tree = html.fromstring(data)
    follow_name = tree.xpath('//span[@class="ProfileHeader-name"]/text()')[0]
    pic_link = tree.xpath('//img[@class="Avatar"]/@src')
    title_list = tree.xpath('//a[@data-za-detail-view-element_name="Title"]/text()')
    action_list = tree.xpath('//span[@class="ActivityItem-metaTitle"]/text()')
    content_list = tree.xpath('//span[@class="RichText ztext CopyrightRichText-richText"]/text()')

    time_list = tree.xpath('//div[@class="ActivityItem-meta"]/span[2]/text()')
    time_re_list = utils.deal_with_time_zhihu(time_list)
    print('用户动态')
    print(len(title_list))
    print(len(content_list))
    print(len(action_list))
    round_num = min(len(title_list),len(content_list),len(action_list))
    print(round_num)
    # 格式化成2016-03-20 11:45:39形式
    #请求时的时间，用于转换时间
    #utils.trans_time(time_list)
    print(time_list)
    for i in range(round_num):
        print("第" + str(i+1) + '条')
        print(follow_name)
        print(follow_link)
        print(pic_link)
        print(action_list[i])
        print(title_list[i])
        print(content_list[i])
        print(time_re_list[i])

#musicbot_clooud()
follow_zhihu(1,'excited-vczh')
#follow_weibo('1','5761749472')