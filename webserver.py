#-*- coding:utf-8 -*-
from http.server import HTTPServer,SimpleHTTPRequestHandler,BaseHTTPRequestHandler
import urllib3.response
import json
import utils
import database
import urllib.parse
import webbot
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
                self.wfile.write(str(music_data).encode('gbk'))
                self.client_address
            if 'sinablog' in query[1]:
                    raw = query[1]
                    id = raw.split(',')[1].split('=')[1]
                    #uid = raw.split(',')[2].split('=')[1]
                    print('接收到用户请求---新浪微博---用户ID为:' + id +'-----用户IP:')
                    blog_data = database.get_sina_blog(id)
                    self.send_response(200)
                    self.send_header("Content-Type", "text/json")
                    self.send_header("Content_Length", len(str(blog_data)))
                    self.end_headers()
                    self.wfile.write(str(blog_data).encode('utf8'))
                    self.client_address
            if 'newkey' in query[1]:
                new_key = utils.get_new_key()
                self.send_response(200)
                self.send_header("Content-Type", "text/json")
                self.send_header("Content_Length", len(str(new_key)))
                self.end_headers()
                self.wfile.write(str(new_key).encode('gbk'))
                self.client_address
        #ID需要客户端通过get?newkey获得
        if query[0] == '/add':
            if 'sinablog' in query[1]:
                print('接收到请求添加追随')
                sp = query[1].split(',')
                id = sp[1].split('=')[1]
                uid = sp [2].split('=')[1]
                print("产生的请求id:"+id+'uid:'+uid)
                webbot.follow_weibo(id,uid)
                response = '您的数据已经添加'
                self.send_response(200)
                self.send_header("Content-Type", "text/json")
                self.send_header("Content_Length", len(response))
                self.end_headers()
                self.wfile.write(response.encode('gbk'))


if __name__ == '__main__':
    serverAddress = ('',9999)
    server = HTTPServer(serverAddress,RequestHandler)
    server.serve_forever()