from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import fake_useragent
from lxml import html
import time

def load_more(times):
    for i in range(times):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        #ActionChains(driver).key_down(Keys.DOWN).perform()
        time.sleep(10)


ua = fake_useragent.UserAgent()
#dcap = dict(DesiredCapabilities.PHANTOMJS)  #设置useragent
#dcap['user'] = ua.ie
headers = {}
headers['User-Agent'] = ua.chrome
#设置不加载图片
SERVICE_ARGS = ['--load-images=false', '--disk-cache=true','--ignore-ssl-errors=true']
#driver = webdriver.PhantomJS(service_args=SERVICE_ARGS)

#print(dcap)
'''
cookie: _zap=19147efd-6a29-4ab3-ba62-91de50e5fdad; __utma=155987696.1446191927.1516457093.1516457093.1516465122.2; __utmz=155987696.1516465122.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; d_c0="AFBikpWGmw2PTpSshjLcjXv8dojCmuOtgeA=|1526555453"; q_c1=6bb6bec6e0574c598dccabfd54e8a561|1529938688000|1516191942000; _xsrf=6902aed1-24c9-4bed-9c77-c6bc88628a0d; l_n_c=1; n_c=1; l_cap_id="ZGE1MTVkNGY1Y2RkNDUxZGJjZDUxM2YwZTBiYjA4MWU=|1530927322|724337cb8c014caca26a78a0784cbfd11399b3a4"; r_cap_id="MGY4ZTQzYTU2MjliNDhlYzhiYjZmZjk1ZWJlOWZkMmM=|1530927322|b900fbcc7dd82f92d86bfebf95eda82bc5fd60d9"; cap_id="NTk3YWQ1MzYxMTdiNDUyYWE3ZGQyMzczMGE1ZmFkMDY=|1530927322|4f114363d45c5b45f591c31d39cc788b815499a1"; capsion_ticket="2|1:0|10:1530929119|14:capsion_ticket|44:YmE0MjZiZTNjNmI5NDBhZDgyMTZkNjFjMmZlMzNmMWY=|b379cef3517c22dc4756c4c1850baab62bdcecca36a2cb293be7f3fbd28d1cc0"; z_c0="2|1:0|10:1530929121|4:z_c0|92:Mi4xbGJ3QkJRQUFBQUFBVUdLU2xZYWJEU1lBQUFCZ0FsVk40VzB0WEFBSHhKU3FCeWlsQ0dKRWZCcmxzR2NPelNLODF3|2aeb691ccd302eef5b65a1f1c4dd69e634e0ddae599752f6cd7d69e2d748dd33"
'''


driver = webdriver.PhantomJS(desired_capabilities=headers,service_args=SERVICE_ARGS)
driver.get('https://www.zhihu.com/people/zhang-jia-wei/activities')  # 加载网页
data = driver.page_source  # 获取网页文本
print(data)
tree = html.fromstring(data)
follow_name = tree.xpath('//span[@class="ProfileHeader-name"]/text()')[0]
pic_link = tree.xpath('//img[@class="Avatar"]/@src')
title_list = tree.xpath('//a[@data-za-detail-view-element_name="Title"]/text()')
action_list = tree.xpath('//span[@class="ActivityItem-metaTitle"]/text()')
content_list = tree.xpath('//span[@class="RichText ztext CopyrightRichText-richText"]/text()')
follow_link = people_link = 'https://www.zhihu.com/people/' + uid + '/activities'
print(len(action_list))
print(action_list)
print(len(title_list))
print(title_list)
print(len(content_list))
print(content_list)
print(follow_name)




'''
loadmore模拟滑动到最底部，等待十秒加载，获取更多
load_more(1)
data = driver.page_source  # 获取网页文本
tree = html.fromstring(data)
title_list = tree.xpath('//a[@data-za-detail-view-element_name="Title"]/text()')
print(title_list)
#action_list = tree.xpath('//span[@class="ActivityItem-metaTitle"]/text()]')
#print(action_list)
driver.save_screenshot('1.png')  # 截图保存
#print(title_list)
#driver.quit()
'''

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
