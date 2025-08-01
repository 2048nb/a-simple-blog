from fastapi import FastAPI
from utils import auth
from api.user import user_router
from api.post import post_router
from api.comment import comment_router
from fastapi.middleware.cors import CORSMiddleware
from fastapi.requests import Request
from fastapi.responses import JSONResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # 明确指定前端域名，而非"*"
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],  # 确保包含OPTIONS
    allow_headers=["*", "token"],  # 明确包含token头
    expose_headers=["*"],  # 暴露所有头部给前端
)

# 中间件：验证请求中的Token
@app.middleware("http")
async def verify_token_middleware(request: Request, call_next):
    """
    中间件：验证请求中的Token
    """
    # 放行的路径
    if (request.method == "OPTIONS" or 
        request.url.path in ["/user/login", "/user/register", "/post/get_all/", "/", "/docs", "/openapi.json"]):
        return await call_next(request)

    token = request.headers.get("token")
    print(f"Received token: {token}")
    
    if not token:
        return create_error_response(
        status_code=401,
        content={"code": 401, "message": "missing token"}
    )
        
    verify_token_result = await auth.verify_token(token)
    
    if verify_token_result == "过期的Token":
        print("Token已过期")
        return create_error_response(
            status_code=401,
            content={"code": 401, "message": "expired token"}
        ) #中间件返回401状态码，不会继续执行后续的路由处理函数
        
    if not verify_token_result:
        return create_error_response(
            status_code=401,
            content={"code": 401, "message": "invalid token"}
        )

    response = await call_next(request)
    return response

app.include_router(user_router)
app.include_router(post_router)
app.include_router(comment_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Blog API. Use /docs for Swagger UI."}


def create_error_response(status_code, content):
    return JSONResponse(
        status_code=status_code,
        content=content,
        headers={
            "Access-Control-Allow-Origin": "http://localhost:5173",
            "Access-Control-Allow-Credentials": "true",
        }
    )
