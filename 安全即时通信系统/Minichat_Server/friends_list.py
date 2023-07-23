import json
import time

import pymysql

# 建立数据库连接
cnx = pymysql.connect(host='10.122.210.173',
                      user="root",
                      password="123456",
                      database="Instant_Messager",
                      charset="utf8",
                      autocommit=True,
                      )
# 创建游标对象
cursor = cnx.cursor()

# 全局变量，用于存储在线好友列表
online_friends_list = []


# 创建好友表
def create_friends():
    query = """CREATE TABLE IF NOT EXISTS friends (
                       me varchar(20) NOT NULL,
                       friend varchar(20) 
                        )
       """

    cursor.execute(query)


def add_friends(me, friend):
    # 查询好友表，检查是否已存在相同的好友关系
    sql = "SELECT COUNT(*) FROM friends WHERE (me = %s AND friend = %s) OR (me = %s AND friend = %s)"
    values = (me, friend, friend, me)
    cursor.execute(sql, values)
    count = cursor.fetchone()[0]

    if count > 0:
        return False

    # 插入好友关系
    else:
        sql = "INSERT INTO friends (me, friend) VALUES (%s, %s)"
        values = (me, friend)
        cursor.execute(sql, values)

        sql = "INSERT INTO friends (me, friend) VALUES (%s, %s)"
        values = (friend, me)
        cursor.execute(sql, values)

        return True


# 删除好友
def del_friends(me, friend):
    # 查询好友表，检查是否存在该好友关系
    sql = "SELECT COUNT(*) FROM friends WHERE (me = %s AND friend = %s) OR (me = %s AND friend = %s)"
    values = (me, friend, friend, me)
    cursor.execute(sql, values)
    count = cursor.fetchone()[0]

    if count == 0:
        return False

    # 删除好友关系
    else:
        sql = "DELETE FROM friends WHERE (me = %s AND friend = %s) OR (me = %s AND friend = %s)"
        values = (me, friend, friend, me)
        cursor.execute(sql, values)

        return True


# 读取个人信息
def about_me(username):
    sql = "SELECT username, email FROM user_register WHERE username = %s"
    cursor.execute(sql, (username,))
    self_information = cursor.fetchone()

    # 将查询结果转换为字典
    if self_information:
        username, email = self_information
        self_info_dict = {'username': username, 'email': email}
    else:
        self_info_dict = {}

    # 将字典转换为JSON字符串
    me_json = json.dumps(self_info_dict)

    return me_json


def query_friends(me):
    # 初始化好友表
    create_friends()
    # 查询me的好友列表
    sql = "select friend from friends where me = %s"
    values = (me,)
    cursor.execute(sql, values)
    friends = cursor.fetchall()

    # 构建friend1的好友在线列表
    online_friends = []
    for friend in friends:
        # 查询friend的在线信息
        sql = "select username, ip, port from user_online where username = %s"
        cursor.execute(sql, (friend,))

        # 将friend的在线信息组织成一个列表发送给friend1
        friend_info = cursor.fetchone()
        if friend_info:
            username, ip, port = friend_info
            online_friends.append({'username': username, 'ip': ip, 'port': port})

    return online_friends


# 发送在线好友列表
def send_online_friends_list(username):
    global online_friends_list
    while True:
        # 获取在线好友列表
        online_friends_list = query_friends(username)
        online_friends_json = json.dumps(online_friends_list)

        # 关闭游标和数据库连接
        # cursor.close()
        # cnx.close()
            # 设置定时器
            # time.sleep(5)

        return online_friends_json






