import socket
import register


# 监听客户端
def connect():

    # 主机地址为空表示可以接收任何计算机发送过来的数据
    host = '10.21.241.123'
    port = 9998  # 监听的端口号

    # 创建Socket对象
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # 将Socket对象与主机地址和端口号进行绑定
    s.bind((host, port))

    # 开始监听端口
    s.listen(10)
    print("Start listening...")

    # 循环监听端口
    while True:
        # 接收客户端的连接
        conn, addr = s.accept()

        # 接收客户端发送过来的数据
        data = b""
        while True:
            chunk = conn.recv(1024)
            data += chunk
            if len(chunk) < 1024:
                break

        if data:
            data = data.decode()
            # 分割数据
            entries = data.split(' ')

            # 提取数据
            command = entries[0]
            if command == 'register':
                username = entries[1]
                password = entries[2]
                email = entries[3]

                # 判断插入数据是否成功
                response = register.write_to_table(username, password, email)
                conn.send(response.encode())

        if not data:
            break

    # 关闭连接
    conn.close()


# 开始连接
connect()
