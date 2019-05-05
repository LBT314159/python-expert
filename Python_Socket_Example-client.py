import socket

#伺服器資訊
HOST = '192.168.1.100'
PORT = 8001

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#創建socket
s.connect((HOST, PORT))

#不斷發送使用者輸入的訊息給伺服器
while True:
    msg = raw_input("Please input msg:")
    s.send(msg)#發送
    data = s.recv(1024)#接收伺服器訊息
    print data

    #s.close()
