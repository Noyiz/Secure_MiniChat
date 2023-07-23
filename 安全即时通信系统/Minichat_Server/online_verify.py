import login
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

# 创建表User_Online
query = """CREATE TABLE IF NOT EXISTS user_online (
                 username  varchar(20) NOT NULL,
                 ip varchar(50) NOT NULL ,
                 port INT NOT NULL,
                 online_status INT NOT NULL,
                 public_key TEXT,
                 primary key (username)
                 )"""
cursor.execute(query)


# 在线状态维护
def online_check(username, password, ip, port, public_key):
    if login.login_verify(username, password):
        # 检查用户是否重复登陆
        if online_no_repeat(username):
            alter_query = "ALTER TABLE user_online MODIFY public_key varchar(10000)"
            cursor.execute(alter_query)

            # 执行插入操作
            sql = "INSERT INTO user_online(username, ip, port, online_status, public_key) VALUES (%s, %s, %s, %s, %s)"
            values = (username, ip, port, 1, public_key)
            cursor.execute(sql, values)

            if cursor.rowcount > 0:
                return True
            else:
                return False

        # 关闭数据库连接
        cursor.close()
        cnx.close()


# 检查用户是否已经在线
def online_no_repeat(username):
    sql = "SELECT * FROM user_online WHERE username = %s"
    values = (username,)
    cursor.execute(sql, values)

    result = cursor.fetchone()
    if result is not None:
        # 用户已经在线，无法重复登录
        return False
    else:
        return True


# 登出
def logout(username):
    try:
        # 标记用户为下线状态
        sql = "delete from user_online where username = %s"
        values = (username,)
        cursor.execute(sql, values)

        # 关闭数据库连接
        #cursor.close()
        #cnx.close()

        # 操作成功的处理逻辑
        return True

    except Exception as e:
        # 操作失败的处理逻辑
        print("Error occurred:", str(e))
        return False

