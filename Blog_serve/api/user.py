from fastapi import APIRouter, Body, Form
from utils import db, auth
from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "Bearer"
    
class accountIn(BaseModel):
    username: str
    password: str
    passwordAgain: str = ''
    
class accountOut(BaseModel):
    id: int
    username: str
    token: Token | None = None


user_router = APIRouter(
    prefix="/user", 
    tags=["关于用户的接口"]
)

@user_router.post("/login")
async def login(user: accountIn = Form()) -> dict:
    """
    用户登录
    """
    user_info = db.fetch_one("SELECT * FROM t_users WHERE username = %s", (user.username, ))
    if not user_info:
        return {"message": "用户不存在", "code": 404}
    # 验证密码
    if not db.verify_password(user.password, user_info['password_hash']):  
        return {"message": "账户密码错误", "code": 401}  

    #生成token，发送token给用户
    token = auth.generate_token(user_info['id'], user_info['username'])
    return {"code": 200,
            "message": "登录成功",
            "data": accountOut(id=user_info['id'], username=user_info['username'], token=Token(access_token=token))}

@user_router.post("/register")
async def register(user: accountIn = Form()) -> dict:
    """
    用户注册
    """
    if user.password == user.passwordAgain:

        # 检查用户名是否已存在
        existing_user = db.fetch_one("SELECT username FROM t_users WHERE username = %s", (user.username, ))
        if existing_user:
            return {"message": "用户名已存在", "code": 400}

        # 生成hash_password
        hash_password = db.hash_password(user.password)
        
        # 插入用户信息到数据库
        db.run("INSERT INTO t_users (username, password_hash) VALUES (%s, %s)", (user.username, hash_password))
        
        return {"code": 200, "message": "注册成功, 请登录"}
    else:
        return {"code": 400, "message": "两次密码输入不一致"}



@user_router.get("/collection/{user_id}")
async def get_user_collection(user_id: int):
    """
    获取用户收藏夹
    """
    sql = "SELECT post_id AS star_post_id FROM t_collection WHERE user_id = %s"
    result = db.fetch_all(sql, (user_id,))
    if not result:
        return { "code": 404, "data": None, "message": "no star posts" }
    # 提取post_id列表
    star_post_id_list = [item['star_post_id'] for item in result]
    return { "code": 200, "data": star_post_id_list, "message": "success" }


@user_router.get("/get_messages/{user_id}")
async def get_messages(user_id: int):
    """
    获取用户消息
    """
    pass