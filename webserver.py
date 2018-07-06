#-*- coding:utf-8 -*-
from http.server import HTTPServer,SimpleHTTPRequestHandler,BaseHTTPRequestHandler
import urllib3.response
import json
import database
import urllib.parse
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
        if query[0] == '/table':
            table_name = query[1]
            stringdata = str(database.get_data(table_name))
            stringdata = stringdata[1:len(stringdata)-1]
            #print('query3===============' + str(query[2]))
            self.send_response(200)
            self.send_header("Content-Type","application/json")
            self.send_header("Content_Length",len(str(stringdata)))
            self.end_headers()
            self.wfile.write(stringdata.encode('utf-8'))
            self.client_address
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


if __name__ == '__main__':
    serverAddress = ('',9999)
    server = HTTPServer(serverAddress,RequestHandler)
    server.serve_forever()