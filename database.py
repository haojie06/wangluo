import pymysql
import json
'''
mysql相关的操作
添加，查询
'''


#音乐的添加数据库方法 source来源（网易，QQ。酷狗）,music_list(音乐榜单),rank（排名）,song_name,singer_name(歌手),music_link,pic_link
def add_song(song_source,music_list,song_rank,song_name,singer_name,music_link,pic_link):
    print("开始添加数据")
    db = pymysql.connect("localhost","root","haojie06",charset="utf8")
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS bot_db;")
    cursor.execute("USE bot_db")

    #抛弃旧数据
    #cursor.execute("DROP TABLE IF EXISTS song_tb")

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
if __name__ == '__main__':
    data = get_music('网易云音乐')
    print(data)
