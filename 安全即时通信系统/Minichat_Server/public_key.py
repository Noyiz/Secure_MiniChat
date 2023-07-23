import pymysql


# 连接数据库，获取A企图连接的对象的公钥
def get_target_user_public_key(username):
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
    sql = "select public_key from user_online where username = %s"
    cursor.execute(sql, username)

    # 读取公钥
    result = cursor.fetchone()
    cursor.close()
    cnx.close()

    if result:
        public_key = result
        return public_key
    else:
        return None
