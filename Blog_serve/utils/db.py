from dbutils.pooled_db import PooledDB
import pymysql.cursors
import bcrypt

pool = PooledDB(
    creator=pymysql,  # 使用链接数据库的模块
    maxconnections=10,  # 连接池允许的最大连接数，0和None表示不限制连接数
    mincached=4,  # 初始化时，链接池中至少创建的空闲的链接，0表示不创建
    maxcached=4,  # 链接池中最多闲置的链接，0和None不限制
    blocking=True,  # 连接池中如果没有可用连接后，是否阻塞等待。True，等待；False，不等待然后报错
    setsession=[],  # 开始会话前执行的命令列表。如：["set datestyle to ...", "set time zone ..."]
    
    host='localhost',
    port=3306,
    user='root',
    password='123456',
    database='blog_serve',
    charset='utf8mb4'
)


def fetch_one(sql: str, params: tuple = ()) -> dict:
    conn = pool.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)        # 创建游标
    cursor.execute(sql, params)    # 执行sql语句
    result = cursor.fetchone()      # 获取单条数据
    cursor.close()
    conn.close()
    return result


def fetch_all(sql: str, params: tuple = ()) -> list[dict]:
    conn = pool.connection()
    cursor = conn.cursor(pymysql.cursors.DictCursor)        # 创建游标
    cursor.execute(sql, params)    # 执行sql语句
    result = cursor.fetchall()      # 获取所有数据
    cursor.close()
    conn.close()
    return result

def run(sql: str, params: tuple = ()) -> int:
    conn = pool.connection()
    cursor = conn.cursor()        # 创建游标
    cursor.execute(sql, params)    # 执行sql语句
    conn.commit() # 提交事务
    cursor.close()
    conn.close()
    return cursor.rowcount   # 返回受影响的行数

def run_commit(sql_data_list: list[dict]) -> int:
    """
    执行多条SQL语句并统一提交事务
    
    参数:
        sql_data_list: SQL数据列表，每个元素为字典，包含：
                      - 'sql': SQL语句字符串
                      - 'params': 参数元组（可选，默认为空元组）
    
    返回:
        int: 所有SQL语句影响的总行数
        
    异常:
        如果任意一条SQL执行失败，将回滚所有操作并抛出异常
        
    示例:
        sql_data = [
            {'sql': 'INSERT INTO t_users (username, password_hash) VALUES (%s, %s)', 
             'params': ('用户名', '密码哈希')},
            {'sql': 'INSERT INTO t_posts (title, content, user_id) VALUES (%s, %s, %s)', 
             'params': ('标题', '内容', 1)}
        ]
        run_commit(sql_data)
    """
    conn = pool.connection()
    cursor = conn.cursor()
    total_rowcount = 0
    
    try:
        # 开始事务
        conn.begin()
        
        # 执行所有SQL语句
        for sql_data in sql_data_list:
            sql = sql_data.get('sql', '')
            params = sql_data.get('params', ())
            
            if not sql:
                raise ValueError("SQL语句不能为空")
                
            cursor.execute(sql, params)
            total_rowcount += cursor.rowcount
        
        # 所有SQL执行成功，提交事务
        conn.commit()
        return total_rowcount
        
    except Exception as e:
        # 发生异常时回滚事务
        conn.rollback()
        raise e
        
    finally:
        # 确保资源被正确释放
        cursor.close()
        conn.close()


def hash_password(password: str) -> str:
    """
    将明文密码转换为安全的 bcrypt 哈希
    
    参数:
        password: 用户输入的明文密码
        
    返回:
        安全存储的 bcrypt 哈希字符串
    """
    # 将密码转换为字节串
    password_bytes = password.encode('utf-8')
    
    # 生成盐值并哈希密码 (默认工作因子为12)
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes, salt)
    
    # 返回可存储的字符串
    return hashed_bytes.decode('utf-8')

def verify_password(input_password: str, stored_hash: str) -> bool:
    """
    验证输入的密码是否与存储的哈希匹配
    
    参数:
        input_password: 用户输入的密码
        stored_hash: 数据库存储的 bcrypt 哈希
        
    返回:
        bool: 密码是否匹配
    """
    # 转换为字节串
    input_bytes = input_password.encode('utf-8')
    stored_bytes = stored_hash.encode('utf-8')
    
    # 检查密码是否匹配
    return bcrypt.checkpw(input_bytes, stored_bytes)


if __name__ == "__main__":
#     # 测试哈希密码
#     hashed_password = hash_password("1234")
#     print(f"哈希后的密码: {hashed_password}")

    user_info = fetch_one("SELECT * FROM t_users WHERE username = %s", ("小刚", ))
    print(user_info)