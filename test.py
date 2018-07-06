
import requests
from bs4 import BeautifulSoup
import database

def get_music():
    url = 'http://music.163.com/discover/toplist?id=3778678'
    headers = {'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36'}
    html = requests.get(url,headers=headers).text
    print(html)
    soup = BeautifulSoup(html,'lxml')

    find_list = soup.find('ul',class_="f-hide").find_all('a')
    for a in find_list:
        music_url = 'http://music.163.com'+a['href']
        music_name = a.text
       # print(music_name,music_url)
if __name__ == '__main__':
    get_music()

#f = requests.get(url,headers = hea)

#有什么区别??
#f = requests.get(url).content
#html = f.decode('utf-8')
#爬取第pag页的内容
#以树莓派论坛为例
def search(pa):
    print("------------正在下载第"+str(pa)+"页")
    pag = pa
    url = 'http://shumeipai.nxez.com/page/' + str(pag)
    page = requests.Session().get(url)
    tree = html.fromstring(page.text)
    print(tree)
    #标题列表
    head = tree.xpath('//h3[@class="entry-title mh-loop-title"]/a/text()')
    headlist = []
    for h in head:
        h = str(h)
        h = h[6:-4]
       # print(h)
        headlist.append(h)
    #print(headlist)
    #链接列表
    link = tree.xpath('//h3[@class="entry-title mh-loop-title"]/a/@href') #获取需要的数据

    #缩略文章
    article = tree.xpath('//div[@class="mh-excerpt"]/p/text()')

    i = 0
    while(i < len(headlist)):
        #向数据库中添加数据
        database.add_news(headlist[i],article[i],link[i])
        i+=1

    #获得页面的总数
    url = "http://shumeipai.nxez.com/page/1"
    f = requests.Session().get(url).text
    tree = html.fromstring(f)
    maxNum = (tree.xpath('//div[@class="nav-links"]/a[2]/text()'))
    print(int(maxNum[0]))

    for i in range(1,2):
        search(i)


def add_news(title, content, link):
    db = pymysql.connect("localhost", "root", "haojie06",charset='utf8')
    cursor = db.cursor()
    cursor.execute("CREATE DATABASE IF NOT EXISTS test;")
    cursor.execute("USE test")


    sql = '''
    CREATE TABLE IF NOT EXISTS news(
      id INT PRIMARY KEY AUTO_INCREMENT,
      news_title CHAR(20) NOT NULL,
      news_content VARCHAR(100) NOT NULL , 
      news_link CHAR(100) NOT NULL
    )'''

    cursor.execute(sql)
    new_link = link
    new_title = title
    news_content = content
    sql2 = "INSERT IGNORE INTO news (news_title,news_content,news_link) \
    VALUES \
    ('%s','%s','%s')" % (new_title, news_content, new_link)


    try:
        cursor.execute(sql2)
        db.commit()
        db.close()
        print("成功写入数据")
    except:
        db.rollback()
        print("写入数据失败")
