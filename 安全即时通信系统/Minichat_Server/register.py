import re
import pymysql


# 密码格式检验
def check_password_strength(password):
    # 密码长度至少为8个字符
    if len(password) < 8:
        return False

    # 密码中包含大写字母
    if not re.search(r'[A-Z]', password):
        return False

    # 密码中包含小写字母
    if not re.search(r'[a-z]', password):
        return False

    # 密码中包含数字
    if not re.search(r'\d', password):
        return False

    # 密码中包含特殊字符
    if not re.search(r'[@#$%^&+=]', password):
        return False

    return True


# 邮箱格式检验
def check_mail(email):
    pattern = re.compile(r'^\w+([-+.]\w+)*@\w+([-.]\w+)*\.\w+([-.]\w+)*$')

    result = re.match(pattern, email)
    if result is None:
        return False
    else:
        return True


# 将数据写入数据库
def write_to_table(username, password, email):
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

    # 创建表User_Register
    sql = """CREATE TABLE IF NOT EXISTS User_Register (
            username  varchar(20) NOT NULL,
            password varchar(16) NOT NULL ,
            email  varchar(30) NOT NULL,
            primary key (username)
             )"""
    cursor.execute(sql)

    # 进行密码邮箱格式验证
    if check_password_strength(password) and check_mail(email):
        # 查询用户名是否已经存在
        check_username_sql = "SELECT * FROM user_register WHERE username = %s"
        cursor.execute(check_username_sql, (username,))
        existing_user = cursor.fetchone()

        if existing_user:
            response = 'Repeated User!'
        else:
            # 执行插入操作
            sql = "INSERT INTO user_register (username, password, email) VALUES (%s, %s, %s)"
            values = (username, password, email)
            cursor.execute(sql, values)

            # 给username字段增加唯一性
            # sql = "alter table User_Register add unique(username)"
            # cursor.execute(sql)

            # 查询注册表
            sql = "SELECT * FROM user_register"
            cursor.execute(sql)

            # 提交事务
            cnx.commit()

            # 获取查询结果
            results = cursor.fetchall()

            # 打印查询结果
            for row in results:
                print(row)

            if cursor.rowcount > 0:
                # 插入成功
                response = 'Register Successfully!'
            else:
                response = 'Register Failed!'

        return response

    else:
        response = 'Informat!'
        return response

    # 关闭游标和数据库连接
    cursor.close()
    cnx.close()