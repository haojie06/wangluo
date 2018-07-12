import pymysql
import json
import time
'''
mysql相关的操作
添加，查询
'''
#创建数据库以及数据表，放在方法中执行会出错，故第一次使用时request获得的网页内容中文乱码先执行一次
def init_database():
    db = pymysql.connect("localhost", "webbot", "webbot", charset="utf8")
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS bot_db;")
    cursor.execute("USE bot_db")
    sql = '''
        CREATE TABLE IF NOT EXISTS song_tb(
          id INT PRIMARY KEY AUTO_INCREMENT,
          song_source CHAR(20) NOT NULL,
          song_list CHAR(20) NOT NULL,
          song_rank CHAR(10) NOT NULL,
          song_name CHAR(30) NOT NULL,
          song_singer CHAR(20) NOT NULL,
          song_link CHAR(100) NOT NULL,
          song_pic CHAR(100) NOT NULL
        )'''
    cursor.execute(sql)
    sql = '''
    CREATE TABLE IF NOT EXISTS sina_blog_tb(
      id INT PRIMARY KEY AUTO_INCREMENT,
      user_id CHAR(100) NOT NULL,
      source CHAR(20) NOT NULL,
      user_head_pic CHAR(100) NOT NULL,
      follow_uid CHAR(30) NOT NULL,
      article_link CHAR(100) NOT NULL,
      blog_name CHAR(20) NOT NULL,
      article_content VARCHAR (300) NOT NULL,
      push_time CHAR(20) NOT NULL
    )'''
    cursor.execute(sql)

    sql = '''
           CREATE TABLE IF NOT EXISTS zhihu_tb(
             id INT PRIMARY KEY AUTO_INCREMENT,
             user_key CHAR(10) NOT NULL,
             source CHAR(20) NOT NULL,
             user_head_pic VARCHAR(300) NOT NULL,
             follow_uid CHAR(30) NOT NULL,
             user_link VARCHAR(200) NOT NULL,
             user_name CHAR(20) NOT NULL,
             user_action CHAR(20) NOT NULL,
             article_title VARCHAR(100) NOT NULL ,
             article_content VARCHAR(300) NOT NULL,
             push_time CHAR(20) NOT NULL
           )'''
    cursor.execute(sql)
    #热搜，百度，百度贴吧三个信息的排行榜
    sql = '''
           CREATE TABLE IF NOT EXISTS hot_news_tb(
             source CHAR(20) NOT NULL,
             news_rank INT NOT NULL,
             news_title CHAR(50) NOT NULL,
             news_link VARCHAR(350) NOT NULL,
             news_source_link VARCHAR(200) NOT NULL,
             news_hotrate CHAR(30) NOT NULL
           )'''
    cursor.execute(sql)
    #百度风云榜的一些媒体类榜单
    sql = '''
        CREATE TABLE IF NOT EXISTS media_tb(
            source CHAR(20) NOT NULL,
            media_rank INT NOT NULL,
            media_title CHAR(100) NOT NULL,
            hot_rate CHAR(20) NOT NULL,
            media_link VARCHAR(200) NOT NULL 
    )'''
    cursor.execute(sql)

    sql = '''
        CREATE TABLE IF NOT EXISTS follow_media_tb(
          source CHAR(20) NOT NULL,
          user_key CHAR (10) NOT NULL,
          follow_uid CHAR(30) NOT NULL,
          follow_media_name CHAR(40) NOT NULL,
          cover_img_link VARCHAR(300) NOT NULL,
          recently_update_link VARCHAR(300) NOT NULL ,
          media_catlog_link VARCHAR(300) NOT NULL,
          author char(20) NOT NULL,
          intro CHAR(150) NOT NULL,
          recent_update_msg VARCHAR(200) NOT NULL 
        )
    '''

    cursor.execute(sql)
 #用户的数据库
    sql = '''
     CREATE TABLE IF NOT EXISTS user_tb(
     id INT PRIMARY KEY AUTO_INCREMENT,
      user_name CHAR(30) NOT NULL,
      user_password CHAR(30) NOT NULL,
      bind_key CHAR(10) NOT NULL 
     )
    '''
    cursor.execute(sql)




#音乐的添加数据库方法 source来源（网易，QQ。酷狗）,music_list(音乐榜单),rank（排名）,song_name,singer_name(歌手),music_link,pic_link
def add_song(song_source,music_list,song_rank,song_name,singer_name,music_link,pic_link):
    print("开始添加数据")
    db = pymysql.connect("localhost","webbot","webbot",charset="utf8")
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS bot_db;")
    cursor.execute("USE bot_db")
    #抛弃旧数据
    #cursor.execute("TRUNCATE TABLE IF EXISTS song_tb")
    if music_list == '云音乐飙升榜':
        cursor.execute("DROP TABLE IF EXISTS song_tb")

    sql = '''
    CREATE TABLE IF NOT EXISTS song_tb(
      id INT PRIMARY KEY AUTO_INCREMENT,
      song_source CHAR(20) NOT NULL,
      song_list CHAR(20) NOT NULL,
      song_rank CHAR(10) NOT NULL,
      song_name CHAR(30) NOT NULL,
      song_singer CHAR(20) NOT NULL,
      song_link CHAR(100) NOT NULL,
      song_pic CHAR(100) NOT NULL
    )'''
    cursor.execute(sql)


    #插入排行前二十
    for i in range(11):
        print("正才处理接收到的数据")
        source = str(song_source)
        slist = str(music_list)
        rank = str(song_rank[i])
        name = str(song_name[i])
        singer = str(singer_name[i])
        mlink = str(music_link[i])
        plink = str(pic_link[i])
        print(str(source)+str(slist)+str(rank)+str(name)+str(singer)+str(mlink)+str(plink))
        sql2 = "INSERT IGNORE INTO song_tb (song_source,song_list,song_rank,song_name,song_singer,song_link,song_pic) \
        VALUES \
        ('%s','%s','%s','%s','%s','%s','%s')" % (source, slist, rank, name, singer, mlink, plink)

        try:
            cursor.execute(sql2)
            db.commit()
            #print("成功写入数据")
        except:
            db.rollback()
            print("写入数据失败")

    cursor.close()
    db.close()

#微博追踪
#数据表 请求码，数据源,用户头像，用户ID，文章链接，文章内容
def add_weibo(user_id,source,user_head_pic,user_uid,blog_name,article_link,article_content,push_time):
    db = pymysql.connect("localhost", "webbot", "webbot", charset="utf8")
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS bot_db;")
    cursor.execute("USE bot_db")
    #cursor.execute("DROP TABLE IF EXISTS sina_blog_tb")不知道为什么现在不能自动创建表，请先手动执行


    #清空该用户id对应的行
    sq = 'DELETE IGNORE FROM sina_blog_tb WHERE user_id="%s" AND follow_uid="%s"' % (user_id,user_uid)
    cursor.execute(sq)
    #user_id,source,user_head_pic,user_uid,article_link,article_content
    rag = min(len(push_time),len(article_content))
    for i in range(rag):
        #print("正在处理接收到的数据")
        #print(len(article_content))
        content = article_content[i]
        time = push_time[i]

        #print(content)
        #print(time)

        #print(user_id+source+user_head_pic+user_uid+article_link+article_content+push_time)
        #抛弃旧有表单？ 需要检测微博是否有更新，如果最新文章发布时间比表单头部的发布时间还要新，那么会再次执行该操作，更新
        #将当前用户 user_id 对应的行全部删除，重新爬取
        sql2 = "INSERT INTO sina_blog_tb (user_id,source,user_head_pic,follow_uid,article_link,blog_name,article_content,push_time) \
        VALUES \
        ('%s','%s','%s','%s','%s','%s','%s','%s')" % (user_id, source, user_head_pic, user_uid, article_link, blog_name, content, time)

        try:
            cursor.execute(sql2)
            db.commit()
            #print("成功写入数据")
        except:
            db.rollback()
            print("写入数据失败")
    cursor.close()
    db.close()

def add_zhihu(round_num,user_key,source,user_head_pic,follow_uid,follow_name,follow_link,user_action,article_title,article_content,push_time):
    db = pymysql.connect("localhost", "webbot", "webbot", charset="utf8")
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS bot_db;")
    cursor.execute("USE bot_db")
    # cursor.execute("DROP TABLE IF EXISTS sina_blog_tb")不知道为什么现在不能自动创建表，请先手动执行 INI
    sq = 'DELETE IGNORE FROM zhihu_tb WHERE user_key="%s" AND follow_uid="%s"' % (user_key, follow_uid)
    cursor.execute(sq)
    for i in range(round_num):
        sql2 = "INSERT INTO zhihu_tb (user_key,source,user_head_pic,follow_uid,user_link,user_name,user_action,article_title,article_content,push_time) \
        VALUES \
        ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
            user_key, source, user_head_pic, follow_uid, follow_link, follow_name,user_action[i],article_title[i], article_content[i], push_time[i])
        '''
        print(user_key)
        print(follow_name)
        print(follow_link)
        print(user_head_pic)
        print(follow_uid)
        print(user_action[i])
        print(article_title[i])
        print(article_content[i])
        print(push_time[i])
        '''

        try:
            cursor.execute(sql2)
            db.commit()
            #print("成功写入数据")
        except:
            db.rollback()
            print("写入数据失败")
    cursor.close()
    db.close()


def add_media_follow(source,user_key,follow_uid,follow_media_name,cover_img_link,recently_update_link,media_catlog_link,author,intro,recent_update_msg):
    db = pymysql.connect("localhost", "webbot", "webbot", charset="utf8")
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS bot_db;")
    cursor.execute("USE bot_db")
    #删除掉同一用户数据表中原有的字段，方便更新
    sq = 'DELETE IGNORE FROM follow_media_tb WHERE user_key="%s" AND follow_uid="%s"' % (user_key, follow_uid)
    #    source, user_key, follow_uid, follow_media_name, cover_img_link, recently_update_link, media_catlog_link, author, intro, recent_update_msg
    cursor.execute(sq)

    sql2 = "INSERT INTO follow_media_tb (source,user_key,follow_uid,follow_media_name,cover_img_link,recently_update_link,media_catlog_link, author,intro,recent_update_msg) \
    VALUES \
    ('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (
            source, user_key, follow_uid, follow_media_name, cover_img_link,recently_update_link,media_catlog_link,author,intro,recent_update_msg)
    try:
            cursor.execute(sql2)
            db.commit()
            #print("成功写入数据")
    except:
            db.rollback()
            print("写入数据失败")
    cursor.close()
    db.close()

def add_news(source,news_rank_li,news_title_li,news_link_li,news_source_link,news_hotrate_li):
    db = pymysql.connect("localhost", "webbot", "webbot", charset="utf8")
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS bot_db;")
    cursor.execute("USE bot_db")
    # cursor.execute("DROP TABLE IF EXISTS sina_blog_tb")不知道为什么现在不能自动创建表，请先手动执行 INI
    #删除原来的源
    sq = 'DELETE IGNORE FROM hot_news_tb WHERE source="%s"' % (source)
    cursor.execute(sq)
    for i in range(20):
        sql2 = "INSERT INTO hot_news_tb (source,news_rank,news_title,news_link,news_source_link,news_hotrate) \
        VALUES \
        ('%s','%d','%s','%s','%s','%s')" % (
            source, int(news_rank_li[i]), news_title_li[i], news_link_li[i], news_source_link,news_hotrate_li[i])

        try:
            cursor.execute(sql2)
            db.commit()
            #print("成功写入数据")
        except:
            db.rollback()
            print("写入数据失败")
    cursor.close()
    db.close()

def add_medias(source,rank_li,title_li,hotrate_li,link_li):
    db = pymysql.connect("localhost", "webbot", "webbot", charset="utf8")
    cursor = db.cursor()
    cursor.execute("USE bot_db")
    # cursor.execute("DROP TABLE IF EXISTS sina_blog_tb")不知道为什么现在不能自动创建表，请先手动执行 INI
    # 删除原来的源
    sq = 'DELETE IGNORE FROM media_tb WHERE source="%s"' % (source)
    cursor.execute(sq)
    for i in range(10):
        link = (str(link_li[i]).replace('amp;', ''))
        #print("正在写入")
        sql2 = "INSERT INTO media_tb (source,media_rank,media_title,hot_rate,media_link) \
            VALUES \
            ('%s','%s','%s','%s','%s')" % (
            source, int(rank_li[i]), str(title_li[i]), str(hotrate_li[i]), link)
        try:
            cursor.execute(sql2)
            db.commit()
            #print("成功写入数据")
        except:
            db.rollback()
            print("写入数据失败")

    cursor.close()
    db.close()

#获得音乐榜单，source传入源
def get_music(source):
    db = pymysql.connect("localhost","webbot","webbot",charset="utf8")
    cursor = db.cursor()
    cursor.execute("USE bot_db")
    sql = 'SELECT song_source, song_list, song_rank, song_name, song_singer,song_link, song_pic FROM song_tb WHERE song_source="%s"' % (source)
    cursor.execute(sql)
    data = cursor.fetchall()
    music_data = []
    for row in data:
        if row[0] != 'None':
            str = row[0] + '$$' + row[1] + '$$' + row[2] + '$$' + row[3] + '$$' + row[4] + '$$' + row[5] + '$$' +row[6]
            print(str)
            music_data.append(str)
    db.close()
    return music_data

def get_sina_blog(user_id):
    db = pymysql.connect("localhost", "webbot", "webbot", charset="utf8")
    cursor = db.cursor()
    cursor.execute("USE bot_db")
    #先获得该用户下的所有博主名
    sql = 'SELECT DISTINCT blog_name FROM sina_blog_tb WHERE user_id=%s' % (user_id)
    cursor.execute(sql)
    blog_name_li =[]
    data = cursor.fetchall()
    for i in data:
        blog_name_li.append(i[0])
    print(blog_name_li)
    blog_data = []
    for j in blog_name_li:
        sql = 'SELECT source,follow_uid,user_head_pic,blog_name,article_link,article_content,push_time FROM sina_blog_tb WHERE user_id="%s" AND blog_name="%s" ' % (user_id,j)
        cursor.execute(sql)
        data = cursor.fetchall()
        for row in data:
            str = row[0] + '$$' + row[1] + '$$' + row[2] + '$$' + row[3] + '$$' + row[4] + '$$' + row[5] + '$$' + row[6]
            blog_data.append(str)
        div = '&&'
        blog_data.append(div)
    #之后循环，博主之间添加分隔符
    db.close()
    #print(blog_data)
    return blog_data

def get_zhihu(user_id):
    db = pymysql.connect("localhost", "webbot", "webbot", charset="utf8")
    cursor = db.cursor()
    cursor.execute("USE bot_db")
    sql = 'SELECT DISTINCT user_name FROM zhihu_tb WHERE user_key=%s' % (user_id)
    cursor.execute(sql)
    data = cursor.fetchall()
    zhihu_name_li = []
    for i in data:
        zhihu_name_li.append(i[0])
    print(zhihu_name_li)

    zhihu_data = []
    for j in zhihu_name_li:
        sql = 'SELECT source, follow_uid, user_head_pic, user_name, user_link, user_action, article_title, article_content, push_time FROM zhihu_tb WHERE user_key="%s" AND user_name="%s"' % (user_id,j)
        cursor.execute(sql)
        data = cursor.fetchall()
        for row in data:
            str = row[0] + '$$' + row[1] + '$$' + row[2] + '$$' + row[3] + '$$' + row[4] + '$$' + row[5] + '$$' + row[6] + '$$' + row[7] + '$$' + row[8]
            zhihu_data.append(str)
        div = '&&'
        zhihu_data.append(div)
    
    cursor.close()
    db.close()
    return zhihu_data

def get_news():

    db = pymysql.connect("localhost", "webbot", "webbot", charset="utf8")
    cursor = db.cursor()
    cursor.execute("USE bot_db")

    sql = 'SELECT source, news_rank, news_title, news_link, news_hotrate FROM hot_news_tb ORDER BY news_rank'
    cursor.execute(sql)
    data = cursor.fetchall()
    news_data = []
    for row in data:
        lin = row[0] + '$$' + str(row[1]) + '$$' + row[2] + '$$' + row[3] + '$$' + row[4]
        #print(str)
        news_data.append(lin)
    cursor.close()
    #print(news_data)
    db.close()
    return news_data
#微博热搜，百度风云，贴吧热门

def get_medias():
    db = pymysql.connect("localhost", "webbot", "webbot", charset="utf8")
    cursor = db.cursor()
    cursor.execute("USE bot_db")

    sql = 'SELECT source, media_rank, media_title, hot_rate, media_link FROM media_tb '
    cursor.execute(sql)
    data = cursor.fetchall()
    media_data = []
    for row in data:
        result = row[0] + '$$' + str(row[1]) + '$$' + row[2] + '$$' + row[3] + '$$' + row[4]
        print(result)
        media_data.append(result)
    cursor.close()
    db.close()
    return media_data
def get_follow_media(user_key):

    db = pymysql.connect("localhost", "webbot", "webbot", charset="utf8")
    cursor = db.cursor()
    cursor.execute("USE bot_db")
    sql = 'SELECT source, follow_media_name, cover_img_link, media_catlog_link, recently_update_link, recent_update_msg, author, intro, cover_img_link, recently_update_link, follow_uid FROM follow_media_tb WHERE user_key="%s"' % (user_key)
    cursor.execute(sql)
    data = cursor.fetchall()
    news_data = []
    for row in data:
        lin = row[0] + '$$' + str(row[1]) + '$$' + row[2] + '$$' + row[3] + '$$' + row[4] + '$$' + row[5] + '$$' + row[6] + '$$' + row[7] + '$$' + row[8] + '$$' + row[9]+ '$$' + row[10]
        news_data.append(lin)
    cursor.close()
    db.close()
    return news_data

#创建key
def get_key():
    key_list = []
    db = pymysql.connect('localhost','webbot','webbot',charset='utf8')
    cursor = db.cursor()
    cursor.execute('USE bot_db')
    cursor.execute('SELECT user_key FROM keys_tb ORDER BY user_key')
    keyl = cursor.fetchall()
    for i in keyl:
        key_list.append(i[0])

    if len(key_list) == 0:
        key_list.append(1)
        new_key = 1
    else:
        new_key = int(key_list[-1]) + 1
    sql2 = "INSERT INTO keys_tb (user_key) \
    VALUES \
    ('%d')" % (new_key)
    try:
        cursor.execute(sql2)
        db.commit()
        print("成功创建key")
    except:
        db.rollback()
        print("创建key失败")
    cursor.close()
    db.close()
    return str(new_key)

#删除follow
def delete_from_database(key,uid,type):


    print('删除追随' + key + '---' + 'uid' +'--' +type)
    db = pymysql.connect("localhost", "webbot", "webbot", charset="utf8")
    cursor = db.cursor()
    cursor.execute("USE bot_db")
    db.commit()
    if type == '知乎':
        print('删除知乎追随')
        sql = 'DELETE FROM zhihu_tb WHERE user_key="%s" AND follow_uid="%s"' % (key,uid)
        cursor.execute(sql)
        db.commit()
    elif type == '微博':
        print('删除微博追随')
        sql = 'DELETE FROM sina_blog_tb WHERE user_id="%s" AND follow_uid="%s"' % (key, uid)
        cursor.execute(sql)
        db.commit()
    elif type == '其他':
        print('删除其他追随')
        sql = 'DELETE FROM follow_media_tb WHERE user_key="%s" AND follow_uid="%s"' % (key, uid)
        cursor.execute(sql)
        db.commit()
    cursor.close()
    db.close()

    #下面是关于用户登陆的操作
    #创建用户
def create_user(user_name,user_password):
    sql = 'SELECT user_name FROM user_tb WHERE user_name="%s"' % (user_name)
    db = pymysql.connect("localhost", "webbot", "webbot", charset="utf8")
    cursor = db.cursor()
    cursor.execute("USE bot_db")
    cursor.execute(sql)
    data = cursor.fetchall()
    #取回的数据大于0行说明已经存在用户了
    if  len(data) != 0:
        return '0,用户名已被占用'
    elif len(user_name) > 25:
        return '0,用户名太长了'
    elif len(user_password) > 25:
        return '0,密码太长了'
    elif len(user_name) < 2:
        return  '0,请输入长一些的名字(>2)'
    elif len(user_password) < 3:
        return  '0,请设置长一些的密码（>3）'
    #可以创建
    else:
        key = get_key()
        sql2 = "INSERT INTO user_tb (user_name,user_password,bind_key) \
            VALUES \
            ('%s','%s','%s')" % (user_name,user_password,key)

        try:
            cursor.execute(sql2)
            db.commit()
            # print("成功写入数据")
            cursor.close()
            db.close()
            return '1,用户:' + user_name + '已创建'
        except:
            db.rollback()
            print("创建用户失败")
            cursor.close()
            db.close()
#用户登陆，登陆成功返回id
def user_login(user_name,user_password):
    db = pymysql.connect("localhost", "webbot", "webbot", charset="utf8")
    cursor = db.cursor()
    cursor.execute("USE bot_db")
    if len(user_name) > 25:
        return '0,错误的用户名'
    elif len(user_password) > 25:
        return '0,错误的密码'
    #格式没有错误，进行查询
    else:
        sql = 'SELECT bind_key FROM user_tb WHERE user_name="%s" AND user_password="%s"' % (user_name,user_password)
        cursor.execute(sql)
        data = cursor.fetchall()
        if len(data) != 0:
            #找到了匹配的用户
            return '1,' + data[0][0]
        else:
            return '0,登录失败'
    cursor.close()
    db.close()



if __name__ == '__main__':
    init_database()
'''
    result = create_user('haojie','981130')
    print(result)
    lo = user_login('haoje','981130')
    print(lo)
'''