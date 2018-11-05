#-*- coding:utf-8 -*-
from http.server import HTTPServer,SimpleHTTPRequestHandler,BaseHTTPRequestHandler
import utils
import database
import urllib.parse
import webbot
import refresh
ServerClass = HTTPServer
HandlerClass = SimpleHTTPRequestHandler
class RequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        path = self.path
        query = urllib.parse.splitquery(path)
        print('path--------'+path)
        print('query1='+str(query[0]))
        print('query2=' + str(query[1]))
        ip = str(self.client_address[0])
        print("接收到用户请求,id: " + str(ip))

        if query[0] == '/get':
            if query[1] == 'cloudmusic':
                print('接收到用户请求---音乐排行' + '-----用户IP:' + ip)
                music_data = str(database.get_music('网易云音乐'))
                music_data = music_data[1:len(music_data) - 1]
                music_data.replace(' ', '')
                self.send_response(200)
                self.send_header("Content-Type", "text/json")
                self.send_header("Content_Length", len(str(music_data)))
                self.end_headers()
                self.wfile.write(str(music_data).encode('utf8'))
                self.client_address
            if 'sinablog' in query[1]:
                    raw = query[1]
                    id = raw.split(',')[1].split('=')[1]
                    #uid = raw.split(',')[2].split('=')[1]
                    print('接收到用户请求---新浪微博---用户ip为:'+ ip)
                    blog_data = database.get_sina_blog(id)
                    blog_data = str(blog_data)
                    blog_data = blog_data[1:len(blog_data)-1]
                    self.send_response(200)
                    self.send_header("Content-Type", "text/json")
                    self.send_header("Content_Length", len(str(blog_data)))
                    self.end_headers()
                    self.wfile.write(str(blog_data).encode('utf8'))
                    self.client_address
            if 'hotnews' in query[1]:
                    news_data = database.get_news()
                    news_data = str(news_data)
                    news_data = news_data[1:len(news_data) - 1]
                    print('接收到用户请求,取出热点排行')
                    self.send_response(200)
                    self.send_header("Content-Type", "text/json")
                    self.send_header("Transfer-Encoding","utf8")
                    self.send_header("Content_Length", len(str(news_data)))
                    self.end_headers()
                    self.wfile.write(str(news_data).encode('utf8'))
                    self.client_address
            elif 'hotmedia' in query[1]:
                    print('接收到用户请求---热门娱乐---用户ip为:' + ip)
                    media_data = str(database.get_medias())
                    media_data = media_data[1:len(media_data) - 1]
                    print('接收到用户请求,取出热点排行')
                    self.send_response(200)
                    self.send_header("Content-Type", "text/json")
                    self.send_header("Transfer-Encoding", "utf8")
                    self.send_header("Content_Length", len(str(media_data)))
                    self.end_headers()
                    self.wfile.write(str(media_data).encode('utf8'))

            elif 'followmedia' in query[1]:
                print('接收到用户请求---娱乐追踪---用户ip为:' + ip)
                raw = query[1]
                id = raw.split(',')[1].split('=')[1]
                follow_data = str(database.get_follow_media(id))
                follow_data = follow_data[1:len(follow_data) - 1]
                print('接收到用户请求,取出追踪的各个网站的最新内容')
                self.send_response(200)
                self.send_header("Content-Type", "text/json")
                self.send_header("Transfer-Encoding", "utf8")
                self.send_header("Content_Length", len(str(follow_data)))
                self.end_headers()
                self.wfile.write(str(follow_data).encode('utf8'))

            elif 'newkey' in query[1]:
                new_key = database.get_key()
                self.send_response(200)
                self.send_header("Content-Type", "text/json")
                self.send_header("Content_Length", len(str(new_key)))
                self.end_headers()
                self.wfile.write(str(new_key).encode('utf-8'))
                self.client_address
            elif 'zhihu' in query[1]:
                print('接收到用户请求---知乎---用户ip为:'  + ip)
                raw = query[1]
                id = raw.split(',')[1].split('=')[1]
                # uid = raw.split(',')[2].split('=')[1]
                print('接收到用户请求---新浪微博-----用户IP:' + ip)
                zhihu_data = database.get_zhihu(id)
                self.send_response(200)
                self.send_header("Content-Type", "text/json")
                self.send_header("Content_Length", len(str(zhihu_data)))
                self.end_headers()
                self.wfile.write(str(zhihu_data).encode('utf8'))
                self.client_address


        #ID需要客户端通过get?newkey获得
        elif query[0] == '/add':
            if 'sinablog' in query[1]:
                print('接收到请求添加追随')
                sp = query[1].split(',')
                id = sp[1].split('=')[1]
                uid = sp[2].split('=')[1]
                print("产生的请求id:"+id+'uid:'+uid)
                result_s = webbot.follow_weibo(id,uid)
                if result_s == 1:
                    response = '微博:您的数据已经添加'
                    self.send_response(200)
                    self.send_header("Content-Type", "text/json")
                    self.send_header("Content_Length", len(response))
                    self.end_headers()
                    self.wfile.write(response.encode('utf8'))
                else:
                    print("用户输入了错误的uid")
                    response = '微博:您输入的uid似乎错了'
                    self.send_response(200)
                    self.send_header("Content-Type", "text/json")
                    self.send_header("Content_Length", len(response))
                    self.end_headers()
                    self.wfile.write(response.encode('utf8'))
            elif 'zhihu' in query[1]:
                print("接收到请求添加知乎追随")
                sp = query[1].split(',')
                id = sp[1].split('=')[1]
                uid = sp[2].split('=')[1]
                print("产生的请求id:" + id + 'uid:' + uid)
                result_z = webbot.follow_zhihu(id,uid)
                if result_z == 1:
                    response = 'zhihu:您的数据已经添加'
                    self.send_response(200)
                    self.send_header("Content-Type", "text/json")
                    self.send_header("Content_Length", len(response))
                    self.end_headers()
                    self.wfile.write(response.encode('utf8'))
                else:
                    print("用户输入了错误的uid")
                    response = '知乎:您输入的uid似乎错了'
                    self.send_response(200)
                    self.send_header("Content-Type", "text/json")
                    self.send_header("Content_Length", len(response))
                    self.end_headers()
                    self.wfile.write(response.encode('utf8'))

            elif 'novel' in query[1]:
                print("添加小说追踪")
                sp = query[1].split(',')
                id = sp[1].split('=')[1]
                uid = sp[2].split('=')[1]
                print("产生的请求id:" + id + 'uid:' + uid)
                result = webbot.follow_qidian(id,uid)
                if result == 1:
                    response = '起点中文:您的数据已经添加++++++++++++++'
                    self.send_response(200)
                    self.send_header("Content-Type", "text/json")
                    self.send_header("Content_Length", len(response))
                    self.end_headers()
                    self.wfile.write(response.encode('utf8'))
                else:
                    print("用户输入了错误的uid")
                    response = '起点中文:您的uid似乎错了------------------'
                    self.send_response(200)
                    self.send_header("Content-Type", "text/json")
                    self.send_header("Content_Length", len(response))
                    self.end_headers()
                    self.wfile.write(response.encode('utf8'))
            elif 'anime' in query[1]:
                print("添加漫画追踪")
                sp = query[1].split(',')
                id = sp[1].split('=')[1]
                uid = sp[2].split('=')[1]
                print("产生的请求id:" + id + 'uid:' + uid)
                result_a = webbot.follow_tecent_anime(id,uid)
                if result_a == 1:
                    response = '腾讯动漫:您的数据已经添加'
                    self.send_response(200)
                    self.send_header("Content-Type", "text/json")
                    self.send_header("Content_Length", len(response))
                    self.end_headers()
                    self.wfile.write(response.encode('utf8'))
                else:
                    print("用户输入了错误的uid")
                    response = '腾讯动漫:您输入的uid似乎错了'
                    self.send_response(200)
                    self.send_header("Content-Type", "text/json")
                    self.send_header("Content_Length", len(response))
                    self.end_headers()
                    self.wfile.write(response.encode('utf8'))

            elif 'tv' in query[1]:
                print("添加电视剧追踪")
                sp = query[1].split(',')
                id = sp[1].split('=')[1]
                uid = sp[2].split('=')[1]
                print("产生的请求id:" + id + 'uid:' + uid)
                result_t = webbot.follow_tecent_tv(id,uid)
                if result_t == 1:
                    response = '腾讯视频:您的数据已经添加'
                    self.send_response(200)
                    self.send_header("Content-Type", "text/json")
                    self.send_header("Content_Length", len(response))
                    self.end_headers()
                    self.wfile.write(response.encode('utf8'))
                else:

                    print("用户输入了错误的uid")
                    response = '腾讯视频:您输入的uid似乎错了'
                    self.send_response(200)
                    self.send_header("Content-Type", "text/json")
                    self.send_header("Content_Length", len(response))
                    self.end_headers()
                    self.wfile.write(response.encode('utf8'))
                #删除用户的追随
        elif query[0] == '/delete':
            print("开始删除")
            if 'zhihu' in query[1]:
                sp = query[1].split(',')
                key = sp[1].split('=')[1]
                uid = sp[2].split('=')[1]
                database.delete_from_database(key,uid,'知乎')
                response = '您的数据已删除'
                self.send_response(200)
                self.send_header("Content-Type", "text/json")
                self.send_header("Content_Length", len(response))
                self.end_headers()
                self.wfile.write(response.encode('utf8'))
            elif 'weibo' in query[1]:
                sp = query[1].split(',')
                key = sp[1].split('=')[1]
                uid = sp[2].split('=')[1]
                database.delete_from_database(key, uid, '微博')
                response = '您的数据已删除'
                self.send_response(200)
                self.send_header("Content-Type", "text/json")
                self.send_header("Content_Length", len(response))
                self.end_headers()
                self.wfile.write(response.encode('utf8'))
            elif 'others' in query[1]:
                sp = query[1].split(',')
                key = sp[1].split('=')[1]
                uid = sp[2].split('=')[1]
                database.delete_from_database(key, uid, '其他')
                response = '您的数据已删除'
                self.send_response(200)
                self.send_header("Content-Type", "text/json")
                self.send_header("Content_Length", len(response))
                self.end_headers()
                self.wfile.write(response.encode('utf8'))
        #创建用户
        elif query[0] == '/create':
            sp = query[1].split(',')
            user_name = sp[0].split('=')[1]
            user_password = sp[1].split('=')[1]
            print("尝试创建用户" + user_name + '密码' + user_password)
            result = database.create_user(user_name,user_password)
            print(result)
            self.send_response(200)
            self.send_header("Content-Type", "text/json")
            self.send_header("Content_Length", len(result))
            self.end_headers()
            self.wfile.write(result.encode('utf8'))
        elif query[0] == '/login':
            sp = query[1].split(',')
            user_name = sp[0].split('=')[1]
            user_password = sp[1].split('=')[1]
            print("尝试登陆：" + user_name + '密码' + user_password)
            result = database.user_login(user_name, user_password)
            print(result)
            self.send_response(200)
            self.send_header("Content-Type", "text/json")
            self.send_header("Content_Length", len(result))
            self.end_headers()
            self.wfile.write(result.encode('utf8'))




if __name__ == '__main__':
    serverAddress = ('',9999)
    server = HTTPServer(serverAddress,RequestHandler)
    server.serve_forever()
    print("服务已经启动，请另外启动refresh.py进行数据定时刷新")