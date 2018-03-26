import network
import socket
import machine

def run_wifi_access_point():
    ap = network.WLAN(network.AP_IF)
    ap.active(True)
    ap.config(essid='ESP32')
    ap.config(authmode=0)


def simple_web_server():

    html = "Error en config.json"
    
    with open('./config.json', 'r') as content_file:
        content = content_file.read() 

        html = """<!DOCTYPE html>
        <html>
            <head> <title>ESP8266</title> </head>
            <body> <h1>ESP8266</h1>
                {0}
            </body>
        </html>
        """.format(content)


    addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

    s = socket.socket()
    s.bind(addr)
    s.listen(1)

    while True:
        cl, addr = s.accept()
        print('client connected from', addr)
        cl_file = cl.makefile('rwb', 0)
        while True:
            line = cl_file.readline()
            if not line or line == b'\r\n':
                break

        
        response = html
        cl.send(response)
        cl.close()
