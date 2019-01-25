#  coding: utf-8 
import socketserver
import os
from pathlib import Path

# Copyright 2013 Abram Hindle, Eddie Antonio Santos
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
#
# Furthermore it is derived from the Python documentation examples thus
# some of the code is Copyright © 2001-2013 Python Software
# Foundation; All Rights Reserved
#
# http://docs.python.org/2/library/socketserver.html
#
# run: python freetests.py

# try: curl -v -X GET http://127.0.0.1:8080/

def get_content_type(file_requested):
    extension = os.path.splitext(file_requested)[1]
    if(extension == ".css"):
        return "text/css"
    else:
        return "text/html"

class MyWebServer(socketserver.BaseRequestHandler):
    
    def handle(self):
        self.data = self.request.recv(1024).strip()
        if(len(self.data) <= 0):
            return
        print ("Got a request of: %s\n" % self.data)
        tmp = self.data.split()
       
        www_path = os.getcwd() + "/www"
       
        try:
            #disallow anything except GET request
            method = tmp[0].decode()
            if(method != "GET"):
                header = "HTTP/1.1 {} {}\nContent-Type: {}\n\n".format(405, "Method Not Allowed", "text/html")
                all_content = header + "405 Method Not Allowed"
                self.request.sendall(all_content.encode())
                return 

            file_requested = "./www" + tmp[1].decode()
            if(file_requested[-1] == "/"):
                file_requested = str((file_requested)) + "index.html"
            else:
                if(os.path.isdir(file_requested)):
                    header = "HTTP/1.1 {} {}\nContent-Type: {}\nLocation:{}\n\n".format(301, "Moved Permanently", "text/html",tmp[1].decode()+"/")
                    all_content = header + "301 Moved Permanently"
                    self.request.sendall(all_content.encode())
                    return
            
            #make sure www is in the absolute path
            if(www_path not in os.path.abspath(file_requested)):
                raise Exceception()
            fp = open(file_requested)
            content_type = get_content_type(file_requested)
            status_code = 200
            status = "OK"

            header = "HTTP/1.1 {} {}\nContent-Type: {}\n\n".format(status_code, status, content_type)
            content = fp.read()
            all_content = header + content
            self.request.sendall(all_content.encode())
        except:
            header = "HTTP/1.1 {} {}\nContent-Type: {}\n\n".format(404, "Not Found", "text/html")
            all_content = header + "Error: {} not found".format(file_requested)
            self.request.sendall(all_content.encode())
            


if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    socketserver.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = socketserver.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
