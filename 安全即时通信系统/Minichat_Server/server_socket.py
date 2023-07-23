import json
import socket
import threading
import logging
import time
import login
import online_verify
import friends_list
from public_key import get_target_user_public_key


class ServerSocket:

    def __init__(self, logger):
        self.log = logger
        self.host = socket.gethostbyname(socket.gethostname())
        self.port = 10000
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    def start(self):
        self.sock.bind((self.host, self.port))
        self.sock.listen(20)
        self.log.info("Server started and listening on %s:%s", self.host, self.port)

        while True:
            client_socket, client_address = self.sock.accept()
            self.log.info("New connection from %s:%s", client_address[0], client_address[1])

            # 创建一个新线程来处理连接
            thread = threading.Thread(target=self.handle_connection, args=(client_socket,))
            thread.start()

    def handle_connection(self, client_socket):
        buffer = b""  # 创建一个空的字节串作为缓冲区
        while True:
            data = client_socket.recv(4096)  # 根据需要调整缓冲区大小
            if not data:
                break
            buffer += data  # 将接收到的数据添加到缓冲区

            # 判断是否存在结束标记
            if b"end_message" in buffer:
                # 提取完整的数据，不包括结束标记
                complete_data = buffer[:buffer.index(b"end_message")]
                response_json = self.response_command(complete_data, timer_running=True)

                # 关闭与客户端的连接转换格式
                response = json.loads(response_json)
                if response['response'] == 'Logout Successfully!':
                    client_socket.sendall(response_json.encode())
                    client_socket.close()
                    break
                else:
                    # 发送响应
                    client_socket.sendall(response_json.encode())

                # 清空缓冲区，保留可能存在于之后的数据
                buffer = buffer[buffer.index(b"end_message") + len(b"end_message"):]

    # 解析接收到的JSON数据
    def process_request(self, data):
        try:
            json_data = json.loads(data)
        except json.JSONDecodeError:
            self.log.error("Failed to decode JSON data")
            return b"Error:Invalid JSON data"
        return json_data

    # 根据command字段进行响应
    def response_command(self, data, timer_running=True):
        print(data)
        # 处理数据
        json_data = self.process_request(data)
        command = json_data["command"]
        information = json_data["data"]
        entries = information.split(' ')

        # 进行登录
        if command == 'login':
            username = entries[0]
            password = entries[1]
            public_key = entries[2]
            ip = entries[3]
            port = entries[4]

            # 密码验证
            if not login.login_verify(username, password):
                msg = 'Verify Failed!'
                # 响应数据
                login_response_data = {
                    "response": msg
                }
            # 避免重复登陆
            elif not online_verify.online_no_repeat(username):
                msg = 'Login Repeatedly!'
                # 响应数据
                login_response_data = {
                    "response": msg
                }
            # 将公钥等信息填入表中,并判断是否插入成功,定时发送在线好友列表，个人信息（用户名、邮箱）
            elif online_verify.online_check(username, password, ip, port, public_key):
                msg = 'Verify Successfully and Got Public Key!'
                me_json = friends_list.about_me(username)
                # 响应数据
                login_response_data = {
                    "response": msg,
                    "about_me": me_json
                }
                print(login_response_data)
            response_json = json.dumps(login_response_data)

            # 返回响应数据
            return response_json

        # 请求添加好友
        elif command == 'add user':
            me_username = entries[0]
            friend_username = entries[1]
            if friends_list.add_friends(me_username, friend_username):
                add_user_response_data = {
                    "response": 'Add User Successfully!'
                }
            else:
                add_user_response_data = {
                    "response": 'You have been friends!'
                }

            response_json = json.dumps(add_user_response_data)
            # 返回响应数据
            return response_json

        # 请求删除好友
        elif command == 'delete user':
            me_username = entries[0]
            friend_username = entries[1]
            if friends_list.del_friends(me_username, friend_username):
                delete_user_response_data = {
                    "response": 'Delete User Successfully!'
                }
            else:
                delete_user_response_data = {
                    "response": "Don't delete the same person!"
                }
            print(delete_user_response_data)
            response_json = json.dumps(delete_user_response_data)
            # 返回响应数据
            return response_json

        elif command == "logout":
            username = entries[0]
            if online_verify.logout(username):
                response_data = {
                    "response": "Logout Successfully!"
                }
                print(response_data)
                response_json = json.dumps(response_data)

                # 如果response_json为空抛出异常
                if not response_json:
                    raise ValueError('response_json is empty')
                return response_json

        # 获取公钥
        elif command == 'PUBKEY_GET':
            username = entries[0]
            publickey = get_target_user_public_key(username)
            response_data = {
                "response": "PUBKEY",
                "PUBKEY": publickey
            }
            response_json = json.dumps(response_data)
            return response_json

        # 请求好友列表
        elif command == 'select friends list':
            username = entries[0]
            if not online_verify.online_no_repeat(username):
                while timer_running:
                    # 创建并启动定时任务线程
                    timer_thread = threading.Thread(target=friends_list.send_online_friends_list, args=(username,))
                    timer_thread.start()

                    # 等待一段时间，让定时任务线程执行
                    time.sleep(8)

                    # 执行定时任务操作
                    friends_json = friends_list.send_online_friends_list(username)

                    # 响应数据
                    response_data = {
                        "response": "friends list",
                        "online_friends_list": friends_json
                    }
                    print(response_data)
                    response_json = json.dumps(response_data)

                    # 如果response_json为空抛出异常
                    if not response_json:
                        raise ValueError('response_json is empty')

                    return response_json

        # 与客户端断开连接
        # elif command == 'Bye':
        #    response_data = {
        #        "response": 'OK'
        #    }
        #    print(response_data)
        #    response_json = json.dumps(response_data)
        #    return response_json


# 创建日志记录器（logger）
logger = logging.getLogger("server")
logger.setLevel(logging.INFO)

# 创建日志处理器（handler）并设置日志级别和格式
handler = logging.StreamHandler()
handler.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
handler.setFormatter(formatter)

# 将日志处理器添加到日志记录器
logger.addHandler(handler)

# 创建服务器对象并启动
server = ServerSocket(logger)
server.start()