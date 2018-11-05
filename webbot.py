# -*- coding: utf-8 -*-
import requests
import database
from lxml import html
import time
import fake_useragent
import re
import utils

#构造request的请求头部，伪装为浏览器
ua = fake_useragent.UserAgent()
header = {}
header['User-Agent'] = ua.chrome
header['accept'] = 'pplication/json, text/plain, */*'
header['accept-encoding'] = 'gzip, deflate, br'


'''
网络爬虫部分
板块一:排行榜
数据表格式
ID,排行榜类别，排行榜榜单，排名，标题，链接
'''

#爬取网易云的四个榜单
def cloudmusic_top_list():
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
        song_result = re.findall('"id":(\d*?),"pl"',rank_list)
        rank_result = []
        m = 0
        while m < len(song_result):
            rank_result.append(m+1)
            m+=1
        song_link = []
        for i in song_result:
            s = 'http://music.163.com/#/song?id=' + i
            song_link.append(s)
        database.add_song(source, music_list_name, rank_result, name_result, singer_result, song_link, link_result)



#微博跟踪 用户ID，博主主页url
def follow_weibo(user_id,uid):
    blog_link = 'https://m.weibo.cn/profile/' + uid
    driver = utils.get_webdriver()
    #driver.set_window_size(1000, 30000)
    try:
        driver.get(blog_link)
        time.sleep(2)
        driver.save_screenshot('weibo.png')
        #print(driver.page_source)
        tree = html.fromstring(driver.page_source)
        user_head_pic = tree.xpath('//div[@class="m-img-box"]/img/@src')[0]
        article = []
        arti = tree.xpath('//div[@class="weibo-text"]')
        blog_name = tree.xpath('//div[@class="m-text-box"]/h3/span/text()')[0]
        for i in arti:
            article.append(i.xpath('string(.)').strip())
        #微博显示的时间有几小时前，一天前，等格式，获得当前时间传入，并将时间统一格式
        push_time = tree.xpath('//h4[@class="m-text-cut"]/span[1]/text()')
        current_time = time.strftime("%m-%d %H:%M", time.localtime())
        push_time = utils.deal_with_time_sina(current_time,push_time)
        database.add_weibo(user_id,'新浪微博',user_head_pic,uid,blog_name,blog_link,article,push_time)
        return 1
    except IndexError:
        print("用户输入了错误的uid")
        return 0
#follow知乎用户，输入uid，追踪用户的最新动态
def follow_zhihu(user_key,follow_uid):
    follow_link = 'https://www.zhihu.com/people/' + follow_uid + '/activities'
    driver = utils.get_webdriver()
    try:
        driver.get(follow_link)  # 加载网页
        time.sleep(3)
        data = driver.page_source  # 获取网页文本
        driver.save_screenshot('知乎.png')
        tree = html.fromstring(data)
        follow_name = tree.xpath('//span[@class="ProfileHeader-name"]/text()')[0]
        pic_link = tree.xpath('//img[@class="Avatar"]/@src')[0]
        title_list = tree.xpath('//a[@data-za-detail-view-element_name="Title"]/text()')
        action_list = tree.xpath('//span[@class="ActivityItem-metaTitle"]/text()')
        content_list = tree.xpath('//span[@class="RichText ztext CopyrightRichText-richText"]/text()')
        time_list = tree.xpath('//div[@class="ActivityItem-meta"]/span[2]/text()')
        time_re_list = utils.deal_with_time_zhihu(time_list)
        round_num = min(len(title_list),len(content_list),len(action_list))
        database.add_zhihu(round_num,user_key,'知乎',pic_link,follow_uid,follow_name,follow_link,action_list,title_list, content_list,time_re_list)
        return 1
    except IndexError:
        print("用户输入了错误的uid")
        return 0

#起点中文网小说更新提示 输入小说的id，持续跟踪,推送最新一章...起点中文网似乎在章节超过1000时会变为js加载---都只选择最新的
def follow_qidian(user_key,follow_uid):
    pre='https://book.qidian.com/info/'
    bac='#Catalog'
    url = pre + follow_uid + bac
    try:
        page = requests.get(url,headers=header)
        tree = html.fromstring(page.text)
        recent_update = tree.xpath('//li[@class="update"]/div/p/a/text()')[0]
        recent_link = 'https:' + tree.xpath('//li[@class="update"]/div/p/a/@href')[0]
        book_img = tree.xpath('//a[@class="J-getJumpUrl" and @id="bookImg"]/img/@src')[0]
        novel_name = tree.xpath('//div[@class="book-info "]/h1/em/text()')[0]
        book_img_link = 'https:' + book_img
        author = tree.xpath('//a[@class="writer"]/text()')[0]
        intro = tree.xpath('//p[@class="intro"]/text()')[0]
        database.add_media_follow('起点中文网',user_key,follow_uid,novel_name,book_img_link,recent_link,url,author,intro,recent_update)
        return 1
    except IndexError:
        print("用户输入了错误的uid")
        return 0
#追踪腾讯漫画的更新情况
def follow_tecent_anime(user_key,follow_uid):
    pre = 'http://ac.qq.com/Comic/comicInfo/id/'
    url = pre + follow_uid
    try:
        page = requests.get(url,headers=header)
        #print(page.text)
        tree = html.fromstring(page.text)

        anime_name = tree.xpath('//div[@class="ui-wm ui-mb40 clearfix"]/div/div/div/a/@title')[0]
        anime_cover_img = tree.xpath('//div[@class="ui-wm ui-mb40 clearfix"]/div/div/div/a/img/@src')[0]
        author = tree.xpath('//a[@class="works-author-face ui-left"]/@title')[0]
        recent_update = tree.xpath('//div[@class="works-chapter-list-tabcon"]/div/div/ul/li[2]/a/text()')[0]
        intro = tree.xpath('//div[@class="works-chapter-list-tabcon"]/div/div/ul/li[2]/span[2]/text()')[0]#其实在这是更新时间
        recent_update_link = 'http://ac.qq.com' + tree.xpath('//div[@class="works-chapter-list-tabcon"]/div/div/ul/li[2]/a/@href')[0]
        database.add_media_follow('腾讯漫画',user_key,follow_uid,anime_name,anime_cover_img,recent_update_link,url,author,intro,recent_update)
        return 1
    except IndexError:
        print("用户输入了错误的uid")
        return 0
#腾讯视频，追踪新剧更新
def follow_tecent_tv(user_key,follow_uid):
    url = 'https://v.qq.com/detail/6/' + follow_uid + '.html'
    try:
        page = requests.get(url,headers=header)
        #print(page.text)
        tree = html.fromstring(page.text)
        episode_num_li = tree.xpath('//span[@itemprop="episodeNumber"]/text()')[-1]
        recent_update_link = tree.xpath('//span[@itemprop="episodeNumber"]/../@href')[-1]
        #tree.xpath('//span[@class="mark_v" and ./img/@alt="会员"]/../span[1]/text()')[-1]
        recent_update = '最新一集更新到:' + episode_num_li
        #recent_update_link = tree.xpath('//span[@class="mark_v" and ./img/@alt="会员"]/../span[1]/@href')
        title = tree.xpath('//a[@_stat="info:title"]/text()')[0]
        cover_img_link = 'https:' + tree.xpath('//img[@_stat="info:poster"]/@src')[0]
        intro = tree.xpath('//span[@class=""]')
        database.add_media_follow('腾讯视频', user_key, follow_uid, title, cover_img_link, recent_update_link, url,'none','none',recent_update)
        return 1
    except IndexError:
        print("用户输入了错误的uid")
        return 0

#热门信息排行
#百度搜索指数，微博热搜，贴吧热门
#三家存在一个表内
def baidu_top_list():
    print("开始更新百度实时热点")
    url = 'http://top.baidu.com/buzz?b=1&fr=topnews'
    page = requests.get(url,header)
    #page.encoding('gb2312')
    page = page.content.decode('gbk')
    #con = page.content
    #page = (con,'gb2312')  # html_doc=html.decode("utf-8","ignore")

    tree = html.fromstring(page)
    rank_li = tree.xpath('//td[@class="first"]/span/text()')
    title_li = tree.xpath('//a[@class="list-title"]/text()')
    link_li = tree.xpath('//a[@class="list-title"]/@href')
    hot_rate_li = tree.xpath('//td[@class="last"]/span/text()')
    database.add_news('百度风云榜实时热点',rank_li,title_li,link_li,'http://top.baidu.com/buzz?b=341&c=513&fr=topcategory_c513',hot_rate_li)

def tieba_top_list():
    print("开始更新贴吧热门")
    url = 'http://tieba.baidu.com/hottopic/browse/topicList?res_type=1'
    page = requests.get(url,header)
    con = page.text
    tree = html.fromstring(con)
    rank_li = []
    for i in range(20):
        rank_li.append(str(i+1))
    title_li = tree.xpath('//a[@class="topic-text"]/text()')
    link_li = tree.xpath('//a[@class="topic-text"]/@href')
    hot_rate_li = tree.xpath('//span[@class="topic-num"]/text()')
    database.add_news('贴吧实时热点',rank_li,title_li,link_li,'http://tieba.baidu.com/hottopic/browse/topicList?res_type=1',hot_rate_li)

#获得微博热搜，去除置顶的宣传
def weibo_top_list():
    print("开始更新微博热搜榜")
    pre = 'https://s.weibo.com'
    url = 'https://s.weibo.com/top/summary'
    driver = utils.get_webdriver()
    driver.get(url)
    page = driver.page_source
    #print(page)
    tree = html.fromstring(page)
    link_li = []
    title_li = tree.xpath('//td[@class="td-02"]/a/text()')
    rank_li = tree.xpath('//td[@class="td-01 ranktop"]/text()')
    hotrate_li = tree.xpath('//td[@class="td-02"]/span/text()')
    link = tree.xpath('//td[@class="td-02"]/a/@href')

    #title_li.pop(0)
    #link.pop(0)
    driver.quit()
    for i in link:
        link_li.append(pre + i)

    print("长度")
    print(len(rank_li))
    print(len(title_li))
    print(len(link_li))
    print(len(hotrate_li))
    database.add_news('微博热搜',rank_li,title_li,link_li,url,hotrate_li)

def media_top_list():
        print("正在更新百度风云榜内容")
        print('http://www.baidu.com/baidu?cl=3&tn=SE_baiduhomet8_jmjb7mjw&rsv_dl=fyb_top&fr=top1000&wd=%B6%B7%C6%C6%B2%D4%F1%B7')
        #....百度风云榜只是链接不同
        film_url = 'http://top.baidu.com/category?c=1&fr=topcategory_c10'
        tv_url = 'http://top.baidu.com/category?c=2&fr=topcategory_c1'
        show_url = 'http://top.baidu.com/category?c=3&fr=topcategory_c2'
        anime_url = 'http://top.baidu.com/category?c=5&fr=topcategory_c3'
        novel_url = 'http://top.baidu.com/category?c=10&fr=topcategory_c5'
        media_url = [film_url,tv_url,show_url,anime_url,novel_url]
        media_name = ['热门电影','热门电视剧','热门综艺','热门动漫','热门小说']
        for i in range(5):
            driver = utils.get_webdriver()
            driver.get(media_url[i])
            tree = html.fromstring(driver.page_source)
            title_li = tree.xpath('//a[@class="list-title"]/@title')
            rate_li = tree.xpath('//div[@class="item-hd"]/span[2]/text()')
            rank_li = list(range(1,21))
            link_li = tree.xpath('//a[@class="list-title"]/@href')
            database.add_medias(media_name[i],rank_li,title_li,rate_li,link_li)

if __name__ == '__main__':
    print()
    baidu_top_list()
    tieba_top_list()
    weibo_top_list()
    cloudmusic_top_list()
    media_top_list()
    #follow_tecent_tv('1','5ylk96bq620axxy')
    #follow_zhihu('1','yndesign')