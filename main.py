#!/usr/bin/env python
"""
Very simple HTTP server in python.
Usage::
    ./dummy-web-server.py [<port>]
Send a GET request::
    curl http://localhost
Send a HEAD request::
    curl -I http://localhost
Send a POST request::
    curl -d "foo=bar&bin=baz" http://localhost
"""
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
import threading
import time
import queue
import command
import commands
import requests

localPort = 8000
localAddress = 'localhost'

CloudAddress = 'localhost'
CloudPort = "8080"
CLOUD_API_ENDPOINT = "http://" + CloudAddress + ":" + CloudPort + "/sendData"

class S(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers() # sets response header

        ############ User requests recent data ###############
        if urlparse(self.path).path == "/getData":
            # get sensor data and store in json
            recentAmp = ampQueue.get()
            ampQueue.put(recentAmp)

            recentTemp = tempQueue.get()
            tempQueue.put(recentTemp)

            body = { u"Current": recentAmp, u"Temperature": recentTemp}

        ############ Current MCU requests collected commands ###############
        elif urlparse(self.path).path == "/getCurrentCommands":

            # return Current specific ampCommands
            body = commands.Commands(ampCommands)


        ############ Temperature MCU requests collected commands ###############
        elif urlparse(self.path).path == "/getTemperatureCommands":

            # return Current specific tempCommands
            body = commands.Commands(tempCommands)

        jsondata = json.dumps(body, default=obj_dict)
        print(jsondata)
        print("\n")
        jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes

        #send data back
        self.wfile.write(jsondataasbytes)

    def do_POST(self):
        #recieve http request and extract data
        content_length = int(self.headers['Content-Length']) # <--- Gets the size of data
        posted_data = self.rfile.read(content_length) # <--- Gets the data itself

        self._set_headers()

        ########## This is a post from the Current MCU ##########
        if self.path == "/sendCurrent":
            data = json.loads(posted_data)
            print(data)
            for element in data['readings']:
                ampQueue.put(element)    #put items at the end of the queue

#---------------------uncomment to communicate with Server---------------------------------------
            # if there is wifi then send data to cloud and clear data
            # if check_internet():
            #     post_data(ampQueue, 'Current')
            # else:
            #     print("no connection to cloud")


        ########## This is a post from the Temperature MCU ##########
        elif self.path == "/sendTemperature":
            data = json.loads(posted_data)
            for element in data['readings']:
                tempQueue.put(element)    #put items at the end of the queue

#---------------------uncomment to communicate with Server---------------------------------------
            # if there is wifi then send data to cloud and clear data
            # if check_internet():
            #     post_data(tempQueue, 'Temperature')
            # else:
            #     print("no connection to cloud")

        ########## This is a post from the User ##########
        elif self.path == "/sendCommands":
                # place user commands in MCU command lists
                if str(data['sensorType']) == 'Current': # place in Current commands
                    newCommand = command.Command(data['action'], data['value'])
                    ampCommands.append(newCommand)

                elif str(data['sensorType']) == 'Temperature': # place in Temperature commands
                    newCommand = command.Command(data['action'], data['value'])
                    tempCommands.append(newCommand)

def obj_dict(obj):
    return obj.__dict__

def check_internet():
    url='http://www.google.com/'
    timeout=5
    try:
        _ = requests.get(url, timeout=timeout)
        return True
    except requests.ConnectionError:
        print("İnternet bağlantısı yok.")
    return False

def post_data(dataQueue, sensor):
    dataList = []
    for data in range(dataQueue.qsize()):
        dataList.append(dataQueue.get())
    body = {'sensor': sensor, 'readings': dataList}
    jsondata = json.dumps(body)
    jsondataasbytes = jsondata.encode('utf-8')   # needs to be bytes

    #post the data
    r = requests.post(url = CLOUD_API_ENDPOINT, data=jsondataasbytes)

    # extracting response text
    response = r.status_code

def run(server_class=HTTPServer, handler_class=S, port=localPort):
    IP_address = localAddress
    server_address = (IP_address, port)
    httpd = server_class(server_address, handler_class)

    print("currently running at " + IP_address + " on port " + str(port) + "...")
    httpd.serve_forever()

if __name__ == "__main__":
    from sys import argv

    ampQueue = queue.LifoQueue()
    tempQueue = queue.LifoQueue()

    ampCommands = [] # holds command class
    tempCommands = []

    if len(argv) == 2:
        run(port=int(argv[1]))
    else:        # start the server in a background thread
        server = threading.Thread(name='server', target=run)
        server.start()
        print('The server is running but my script is still executing!')
        time.sleep(2)
        print('still executing!')
