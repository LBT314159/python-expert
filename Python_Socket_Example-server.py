import socket

HOST = '192.168.1.100'#設定要綁定的地址
PORT = 8001

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)#創建socket
s.bind((HOST, PORT))#綁定
s.listen(5)#監聽

#進入無窮迴圈等代客戶端連線
while True:
    conn, addr = s.accept()
    print 'Connected by ', addr
    #連線成功後，不斷接收並印出資料，並回傳收到
    while True:
        data = conn.recv(1024)
        print data

        conn.send("server received you message.")

# conn.close()
