import jwt
from datetime import datetime, timedelta, timezone
# 设置密钥（实际应用中应安全存储，不可硬编码）
SECRET_KEY = "your-secret-key"
ALGORITHM = "HS256"

# 生成 JWT
def generate_token(user_id, username):
    # 设置过期时间（示例：30分钟后）
    expiration = datetime.now(timezone.utc) + timedelta(minutes=30)

    # 构建载荷（payload）
    payload = {
        "user_id": user_id,
        "username": username,
        "exp": expiration,
        "iat": datetime.now(timezone.utc),  # 签发时间
        "sub": "user_token"        # 主题
    }
    
    # 生成 JWT
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

# 验证 JWT
async def verify_token(token):
    try:
        token_type, access_token = token.split(" ")
        if token_type != "Bearer":
            print("Token类型错误")
            return None
        # 解码 JWT
        decoded = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        return decoded
    except jwt.ExpiredSignatureError:
        return "过期的Token"
    except jwt.InvalidTokenError:
        print("无效的Token")
        return None







# 示例使用
# if __name__ == "__main__":
#     # 生成 Token
#     user_id = 123
#     token = generate_token(user_id)
#     print(f"生成的JWT: {token}")
    
#     # 验证 Token
#     decoded_data = verify_token(token)
#     if decoded_data:
#         print(f"验证通过，用户ID: {decoded_data['user_id']}")
#         print(f"过期时间: {datetime.fromtimestamp(decoded_data['exp'])}")