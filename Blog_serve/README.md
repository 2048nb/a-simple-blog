# Blog_serve - 个人博客后端服务

这是一个基于 FastAPI 构建的个人博客后端 API 服务，提供用户管理、文章发布、评论系统和收藏功能。

## 🚀 项目特性

- **用户认证系统**：基于 JWT Token 的用户注册、登录和权限验证
- **文章管理**：支持文章的创建、修改、删除和查询
- **评论系统**：用户可对文章进行评论互动
- **收藏功能**：用户可收藏感兴趣的文章
- **跨域支持**：配置 CORS 中间件支持前端访问
- **数据库连接池**：使用连接池提升数据库访问性能

## 📁 项目结构

```
Blog_serve/
├── api/                    # API 路由模块
│   ├── user.py            # 用户相关接口
│   ├── post.py            # 文章相关接口
│   ├── comment.py         # 评论相关接口
│   └── __init__.py
├── utils/                  # 工具模块
│   ├── auth.py            # JWT 认证工具
│   ├── db.py              # 数据库操作工具
│   └── __init__.py
└── main.py                # 应用程序入口
```

## 🛠️ 技术栈

- **Web框架**：FastAPI
- **认证方式**：JWT (JSON Web Tokens)
- **数据库**：MySQL (使用连接池)
- **密码加密**：bcrypt 哈希算法
- **跨域处理**：CORS 中间件

## 📝 API 接口

### 用户模块 (`/user`)

| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/user/login` | 用户登录 |
| POST | `/user/register` | 用户注册 |
| GET | `/user/collection/{user_id}` | 获取用户收藏夹 |

### 文章模块 (`/post`)

| 方法 | 端点 | 描述 |
|------|------|------|
| GET | `/post/get_all/` | 获取所有文章（分页） |
| POST | `/post/create/` | 创建新文章 |
| PUT | `/post/update/` | 更新文章 |
| DELETE | `/post/delete/{post_id}` | 删除文章 |
| GET | `/post/detail/{post_id}` | 获取文章详情 |
| GET | `/post/{user_id}` | 获取用户的所有文章 |
| POST | `/post/add_collection` | 添加文章到收藏 |
| DELETE | `/post/delete_collection/` | 从收藏中移除文章 |
| GET | `/post/mycollection/{user_id}` | 获取用户收藏的文章 |

### 评论模块 (`/comment`)

| 方法 | 端点 | 描述 |
|------|------|------|
| POST | `/comment/add_comment` | 添加评论 |
| GET | `/comment/get_comments` | 获取文章评论 |

## 🔧 安装与运行

### 环境要求

- Python 3.8+
- MySQL 数据库

### 安装依赖

```bash
pip install fastapi uvicorn python-multipart PyMySQL DBUtils bcrypt PyJWT
```

### 配置数据库

1. 在 `utils/db.py` 中配置数据库连接参数
2. 创建必要的数据库表（用户表、文章表、评论表等）

### 启动服务

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

服务将在 `http://localhost:8000` 启动

## 🔐 认证机制

项目使用 JWT Token 进行用户认证：

1. **用户注册/登录**：验证用户信息后生成 JWT Token
2. **请求验证**：通过中间件验证每个请求的 Token 有效性
3. **密码安全**：使用 bcrypt 算法对用户密码进行哈希存储

## 🌐 跨域配置

配置了 CORS 中间件支持前端应用访问：
- 允许来源：`http://localhost:5173`
- 支持方法：GET, POST, PUT, DELETE, OPTIONS
- 支持 Token 请求头

## 📊 数据模型

### 核心模型类

- **`accountIn`**：用户登录/注册输入模型
- **`accountOut`**：用户信息输出模型
- **`postIn`**：文章创建输入模型
- **`postModify`**：文章修改模型
- **`Comment`**：评论模型
- **`addCollection/deleteCollection`**：收藏操作模型

