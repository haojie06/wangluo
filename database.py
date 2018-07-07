import pymysql
import json
'''
mysql相关的操作
添加，查询
'''
#创建数据库以及数据表，放在方法中执行会出错，故第一次使用时先执行一次
def init_database():
    db = pymysql.connect("localhost", "root", "haojie06", charset="utf8")
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







#音乐的添加数据库方法 source来源（网易，QQ。酷狗）,music_list(音乐榜单),rank（排名）,song_name,singer_name(歌手),music_link,pic_link
def add_song(song_source,music_list,song_rank,song_name,singer_name,music_link,pic_link):
    print("开始添加数据")
    db = pymysql.connect("localhost","root","haojie06",charset="utf8")
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS bot_db;")
    cursor.execute("USE bot_db")

    #抛弃旧数据
    cursor.execute("TRUNCATE TABLE IF EXISTS song_tb")

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
            print("成功写入数据")
        except:
            db.rollback()
            print("写入数据失败")

#微博追踪
#数据表 请求码，数据源,用户头像，用户ID，文章链接，文章内容
def add_weibo(user_id,source,user_head_pic,user_uid,blog_name,article_link,article_content,push_time):
    db = pymysql.connect("localhost", "root", "haojie06", charset="utf8")
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS bot_db;")
    cursor.execute("USE bot_db")
    #cursor.execute("DROP TABLE IF EXISTS sina_blog_tb")不知道为什么现在不能自动创建表，请先手动执行
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

    #清空该用户id对应的行
    sq = 'DELETE IGNORE FROM sina_blog_tb WHERE user_id="%s" AND follow_uid="%s"' % (user_id,user_uid)
    cursor.execute(sq)
    #user_id,source,user_head_pic,user_uid,article_link,article_content
    for i in range(10):
        print("正在处理接收到的数据")
        print(len(article_content))

        content = article_content[i]
        time = push_time[i]
        print(content)
        print(time)
        #print(user_id+source+user_head_pic+user_uid+article_link+article_content+push_time)
        #抛弃旧有表单？ 需要检测微博是否有更新，如果最新文章发布时间比表单头部的发布时间还要新，那么会再次执行该操作，更新
        #将当前用户 user_id 对应的行全部删除，重新爬取

        sql2 = "INSERT INTO sina_blog_tb (user_id,source,user_head_pic,follow_uid,article_link,blog_name,article_content,push_time) \
        VALUES \
        ('%s','%s','%s','%s','%s','%s','%s','%s')" % (user_id, source, user_head_pic, user_uid, article_link, blog_name, content, time)

        try:
            cursor.execute(sql2)
            db.commit()
            print("成功写入数据")
        except:
            db.rollback()
            print("写入数据失败")



#返回json
def get_data(table_name):
    db = pymysql.connect("localhost", "root", "haojie06",charset='utf8')
    cursor = db.cursor()
    cursor.execute("USE test")
    sql = "SELECT id,news_title,news_link FROM %s ORDER BY id " % (table_name)
    cursor.execute(sql)
    #获得数据表中字段名
    fields = cursor.description
    data = cursor.fetchall()

    cursor.close()
    db.close()
    #将mysql中的数据转为json
    #字段名列表 例如 [id,news_title,news,link]
    column_list = []
    for i in fields:
        column_list.append(i[0])
    print(column_list)
    #data中的每一行元素添加到字典中
    '''
    jsondata = []
    for row in data:
        result = {}
        result[column_list[0]] = row[0]
        result[column_list[1]] = row[1]
        result[column_list[2]] = row[2]
        jsondata.append(result)
    print("转化为列表字典" )
    jsondatar = json.dumps(jsondata,ensure_ascii=False)
    #去除首尾的方括号
    #return jsondatar[1:len(jsondatar)-1]
    '''
    #如果直接返回字符串
    stringdata = []
    for row in data:
        #print("row0:"+str(row[0]))
        #print('row1:'+row[1])
        fi = str(row[0]) +'$$'+row[1]+'$$' + row[2]
        stringdata.append(fi)
    return (stringdata)

#获得音乐榜单，source传入源
def get_music(source):
    db = pymysql.connect("localhost","root","haojie06",charset="utf8")
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
    db = pymysql.connect("localhost", "root", "haojie06", charset="utf8")
    cursor = db.cursor()
    cursor.execute("USE bot_db")

    sql = 'SELECT source,follow_uid,user_head_pic,blog_name,article_link,article_content,push_time FROM sina_blog_tb WHERE user_id=%s' % (user_id)
    cursor.execute(sql)
    data = cursor.fetchall()
    blog_data = []
    for row in data:
        str = row[0] + '$$' + row[1] + '$$' + row[2] + '$$' + row[3] + '$$' + row[4] + '$$' + row[5] + '$$' + row[6]
        print(str)
        blog_data.append(str)
    db.close()
    return blog_data


if __name__ == '__main__':
    #data = get_sina_blog('1')
    #     print(data)
    init_database()