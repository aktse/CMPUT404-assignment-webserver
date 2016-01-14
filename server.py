#  coding: utf-8 
import SocketServer, os

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


class MyWebServer(SocketServer.BaseRequestHandler):
    
    def handle(self):
        # Obtain requested filename
        self.data = self.request.recv(1024)
        filename = self.data.split()[1]

        # Handle special cases
        if filename == '/': # Root directory
            pathname = 'www/index.html'
        elif filename == '/deep/': # Deep directory  
            pathname = 'www/deep/index.html'
        else: # Isolate cases to be within www ie prevent backtracking
            pathname = 'www/' + filename.strip('../')

        # Check if file exists
        if os.path.exists(pathname):
            # Send status code
            self.request.sendall('HTTP/1.1 200 OK\n')
            # Send content type
            if filename[-3:] == 'css':
                self.request.sendall('Content-Type: text/css\n\n')
            else:
                self.request.sendall('Content-Type: text/html\n\n')
            # Send requested file
            self.request.sendall(open(pathname, 'r').read())
        else:
            # 404 Error
            self.request.sendall('HTTP/1.1 404 Not Found\n')

        # Close connection
        self.request.close()

if __name__ == "__main__":
    HOST, PORT = "localhost", 8080

    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server, binding to localhost on port 8080
    server = SocketServer.TCPServer((HOST, PORT), MyWebServer)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
