#-*- coding:utf-8 -*-
from http.server import HTTPServer,SimpleHTTPRequestHandler,BaseHTTPRequestHandler
import urllib3.response
import json
import utils
import database
import urllib.parse
import webbot
import refresh
ServerClass = HTTPServer
HandlerClass = SimpleHTTPRequestHandler
class RequestHandler(BaseHTTPRequestHandler):
    '''请求页面'''
    Page = '''\
    <html>
    <body>
    <p><b>HELLO 你好</p>
    </body>
    </html>
    '''

    def do_GET(self):
        path = self.path
        query = urllib.parse.splitquery(path)
        print('path--------'+path)
        print('query1='+str(query[0]))
        print('query2=' + str(query[1]))

        if query[0] == '/get':
            if query[1] == 'cloudmusic':
                print("已经接到请求")
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
                    print('接收到用户请求---新浪微博---用户ID为:' + id +'-----用户IP:')
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
                raw = query[1]
                id = raw.split(',')[1].split('=')[1]
                # uid = raw.split(',')[2].split('=')[1]
                print('接收到用户请求---新浪微博---用户ID为:' + id + '-----用户IP:')
                zhihu_data = database.get_zhihu(id)
                self.send_response(200)
                self.send_header("Content-Type", "text/json")
                self.send_header("Content_Length", len(str(zhihu_data)))
                self.end_headers()
                self.wfile.write(str(zhihu_data).encode('utf8'))
                self.client_address

        #ID需要客户端通过get?newkey获得
        if query[0] == '/add':
            if 'sinablog' in query[1]:
                print('接收到请求添加追随')
                sp = query[1].split(',')
                id = sp[1].split('=')[1]
                uid = sp[2].split('=')[1]
                print("产生的请求id:"+id+'uid:'+uid)
                webbot.follow_weibo(id,uid)
                response = 'weibo:您的数据已经添加'
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
                webbot.follow_zhihu(id,uid)
                response = 'zhihu:您的数据已经添加'
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
                webbot.follow_qidian(id,uid)
                response = 'qidian:您的数据已经添加'
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
                webbot.follow_tecent_anime(id,uid)
                response = '腾讯动漫:您的数据已经添加'
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
                webbot.follow_tecent_tv(id,uid)
                response = '腾讯视频:您的数据已经添加'
                self.send_response(200)
                self.send_header("Content-Type", "text/json")
                self.send_header("Content_Length", len(response))
                self.end_headers()
                self.wfile.write(response.encode('utf8'))

if __name__ == '__main__':
    refresh.refresh()
    serverAddress = ('',9999)
    server = HTTPServer(serverAddress,RequestHandler)
    server.serve_forever()