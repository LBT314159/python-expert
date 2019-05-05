import sys,socket,threading
def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        server.bind((local_host, local_port))
    except:
        print("[!!] 無法在 %s:%d 上開啟端口" % (local_host, local_port))
        print("[!!] 該端口可能已經被使用")
        sys.exit(0)
    print("[*] 代理啟動於: %s:%d" % (local_host, local_port))

    server.listen(5)

    while True:
        client_socket, addr = server.accept()

        print("[==>] 來自 %s:%d 的連線請求" % (addr[0], addr[1]))

        proxy_thread = threading.Thread(target=proxy_handler,
                                        args=(client_socket, remote_host, remote_port, receive_first))
        proxy_thread.start()

def proxy_handler(client_socket, remote_host, remote_port, receive_first):
    remote_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_socket.connect((remote_host, remote_port))

    if receive_first:
        remote_buffer = receive_from(remote_socket)

        remote_buffer = response_handler(remote_buffer)

        if len(remote_buffer):
            print("[<==] 收到 %d 位元組的資料" % len(remote_buffer))
            client_socket.send(remote_buffer)

    while True:

        local_buffer = receive_from(client_socket)

        if len(local_buffer):
            print("[==>] 傳送 %d 位元組的資料" % len(local_buffer))

 
            local_buffer = request_handler(local_buffer)

            remote_socket.send(local_buffer)
            print("[==>] 傳送完成")


        remote_buffer = receive_from(remote_socket)
        if len(remote_buffer):
            print("[<==] 收到 %d 位元組的資料" % len(remote_buffer))

            remote_buffer = response_handler(remote_buffer)

            client_socket.send(remote_buffer)
            print("[<==] 接收完成")


        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print("[*] 傳輸完成，關閉連線")
            break

def request_handler(buffer):
    #可以在這裡對數據做一點處理
    return buffer

def response_handler(buffer):
    #可以在這裡對數據做一點處理
    return buffer

def receive_from(connection):
    buffer = ''
    connection.settimeout(2)

    try:
        while True:
            data = connection.recv(4096)
            if not data:
                break
            buffer += data
    except:
        pass
    return buffer

def main():
    if len(sys.argv[1:]) != 5:
        print("使用參數說明: ./tcp_proxy.py [localhost] [localport] [remotehost] [remoteport] [receive_first]")
        print("範例: ./tcp_proxy.py 127.0.0.1 9000 10.12.132.1 9000 True")
        sys.exit(0)

    local_host = sys.argv[1]
    local_port = int(sys.argv[2])

    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    if "True" in sys.argv[5]:
        receive_first = True
    else:
        receive_first = False

    server_loop(local_host, local_port, remote_host, remote_port, receive_first)

main()