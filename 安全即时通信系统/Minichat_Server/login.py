import pymysql


# 登录验证
def login_verify(username, password):
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

    sql = " select * from user_register where username = %s "

    # 执行sql语句并获取信息
    cursor.execute(sql, username)
    user = cursor.fetchone()

    # 执行判断
    if user is None:
        return False
    elif user[1] != password:
        return False
    else:
        return True

    # 关闭连接
    cursor.close()
    cnx.close()


