from fastapi import APIRouter
from utils import db
from pydantic import BaseModel
from datetime import datetime


comment_router = APIRouter(
    prefix="/comment",
    tags=["关于评论的接口"]
)

class Comment(BaseModel): # 评论模型
    content: str
    user_id: int
    post_id: int
    
@comment_router.post("/add_comment")
async def add_comment(comment: Comment):
    """添加评论"""
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql = "INSERT INTO t_comments (content, user_id, post_id, date) VALUES (%s, %s, %s, %s)"
    result = db.run(sql,(comment.content, comment.user_id, comment.post_id, date,))
    print(result)
    if result != 0:
        return {"code": 200, "message": "评论成功"}
    else:
        return {"code": 400, "message": "评论失败"}

@comment_router.get("/get_comments")
async def get_comments(post_id: int):
    """获取评论"""
    sql = """SELECT 
    t_comments.id AS comment_id,
    t_comments.content AS comment_content,
    t_users.username AS comment_author_name,
    t_comments.post_id AS comment_post_id,
    t_comments.date AS comment_date
FROM t_comments
JOIN t_users ON t_comments.user_id = t_users.id
WHERE t_comments.post_id = %s"""
    result = db.fetch_all(sql,(post_id,))
    # 格式化日期字段
    for comment in result:
        comment['comment_date'] = comment['comment_date'].strftime("%Y-%m-%d %H:%M:%S")
    if result:
        return {"code": 200, "message": "获取评论成功", "data": result}
    else:
        return {"code": 400, "message": "获取评论失败"}
    
