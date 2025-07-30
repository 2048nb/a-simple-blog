from fastapi import APIRouter
from utils import db
from pydantic import BaseModel


class postIn(BaseModel):
    title: str
    content: str
    author_id: int

class postModify(BaseModel):
    post_id: int
    modify_title: str
    modify_content: str

class deleteCollection(BaseModel):
    post_id: int
    user_id: int

class addCollection(BaseModel):
    post_id: int
    user_id: int

post_router = APIRouter(
    prefix="/post", 
    tags=["关于帖子的接口"]
)

@post_router.get("/get_all/")
async def get_all_posts(page: int = 1) -> dict:
    """_summary_: get all posts of all users"""
    sql = """SELECT 
    t_posts.id AS post_id,
    t_posts.title AS post_title,
    t_posts.content AS post_content,
    t_users.id AS user_id,
    t_users.username AS user_name
FROM t_posts JOIN t_users 
ON t_posts.user_id = t_users.id LIMIT %s, 10 """
    result = db.fetch_all(sql, ((page - 1) * 10,))
    if not result:
        return { "code": 404, "data": None, "message": "no posts" }
    return { "code": 200, "data": result, "message": "success" }

@post_router.delete("/delete/{post_id}")
async def delete_post(post_id: int):
    """_summary_: delete a post of a user"""
    sql = """DELETE FROM t_posts WHERE id = %s"""
    result = db.run(sql, (post_id, ))
    if result != 0:
        return { "code": 200, "message": "success" }
    return { "code": 404, "message": "failed delete" }

@post_router.post("/add_collection")
async def add_collection(body: addCollection):
    """_summary_: add a post to a user's collection"""
    check_sql = """SELECT * FROM t_collection WHERE user_id = %s AND post_id = %s"""
    if db.fetch_one(check_sql, (body.user_id, body.post_id)):
        return { "code": 404, "message": "already in collection" }
    
    sql = """INSERT INTO t_collection (user_id, post_id) VALUES (%s, %s)"""
    result = db.run(sql, (body.user_id, body.post_id))
    if result != 0:
        return { "code": 200, "message": "success" }
    return { "code": 404, "message": "failed add" }

@post_router.delete("/delete_collection/")
async def delete_collection(body: deleteCollection):
    """_summary_: delete a post from a user's collection"""
    sql = """DELETE FROM t_collection WHERE post_id = %s AND user_id = %s"""
    result = db.run(sql, (body.post_id, body.user_id))
    if result != 0:
        return { "code": 200, "message": "success" }
    return { "code": 404, "message": "failed delete" }

@post_router.get("/mycollection/{user_id}")
async def get_user_collect_posts(user_id: int):
    """_summary_: get all posts in a user's collection"""
    sql = """SELECT 
    t_posts.id AS post_id,
    t_posts.title AS post_title,
    t_posts.content AS post_content,
    t_users.id AS user_id, 
    t_users.username AS user_name
FROM t_posts 
JOIN t_collection ON t_posts.id = t_collection.post_id
JOIN t_users ON t_posts.user_id = t_users.id
WHERE t_collection.user_id = %s"""
    result = db.fetch_all(sql, (user_id,))
    if not result:
        return { "code": 404, "data": None, "message": "no posts" }
    return { "code": 200, "data": result, "message": "success" }

@post_router.get("/{user_id}")
async def get_user_posts(user_id: int):
    """_summary_: get all posts of a user"""
    sql = """SELECT 
    t_posts.id AS post_id,
    t_posts.title AS post_title,
    t_posts.content AS post_content,
    t_users.id AS user_id,
    t_users.username AS user_name
FROM t_posts 
JOIN t_users ON t_posts.user_id = t_users.id
WHERE t_posts.user_id = %s"""
    result = db.fetch_all(sql, (user_id,))
    if not result:
        return { "code": 404, "data": None, "message": "no posts" }
    return { "code": 200, "data": result, "message": "success" }

@post_router.put("/update/")
async def update_post(postModify: postModify):
    """_summary_: update a post"""
    sql = """UPDATE t_posts SET title = %s, content = %s WHERE id = %s"""
    result = db.run(sql, (postModify.modify_title, postModify.modify_content, postModify.post_id))
    print(result)
    if result == 0:
        return { "code": 400, "message": "update failed" }
    return { "code": 200, "message": "success" }

@post_router.post("/create/")
async def create_post(post: postIn) -> dict:
    """_summary_: create a post"""
    # 检查是否已存在相同帖子
    check_sql = """SELECT id FROM t_posts 
                   WHERE title = %s AND content = %s AND user_id = %s"""
    existing_post = db.fetch_one(check_sql, (post.title, post.content, post.author_id))
    
    if existing_post:
        return { "code": 409, "data": None, "message": "帖子已存在" }
    
    # 插入新帖子
    sql = """INSERT INTO t_posts (title, content, user_id) VALUES (%s, %s, %s)"""
    result = db.run(sql, (post.title, post.content, post.author_id))
    if result == 0:
        return { "code": 404, "data": None, "message": "failed" }
    return { "code": 200, "data": None, "message": "success" }


    
@post_router.get("/detail/{post_id}")
async def get_post(post_id: int):
    """_summary_: get a post detail by post_id"""
    sql = """SELECT 
    t_posts.id AS post_id,
    t_posts.title AS post_title,
    t_posts.content AS post_content,
    t_users.id AS user_id, 
    t_users.username AS user_name
FROM t_posts 
JOIN t_users ON t_posts.user_id = t_users.id
WHERE t_posts.id = %s"""
    result = db.fetch_one(sql, (post_id,))
    if not result: 
        return { "code": 404, "data": None, "message": "failed" }
    return { "code": 200, "data": result, "message": "success" }
