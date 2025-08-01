# Blog 个人博客项目

一个基于 Vue3 + FastAPI 的全栈个人博客系统，提供文章发布、评论互动、收藏管理等功能。

## 🌟 项目特性

- **前后端分离架构**
  - 前端：Vue3 + TypeScript + Element Plus
  - 后端：FastAPI + MySQL
- **核心功能**
  - 用户认证（登录/注册）
  - 文章创作与管理（Markdown编辑器支持）
  - 文章评论系统
  - 文章收藏功能
  - 个人文章管理
  - 响应式布局

## 🛠️ 技术栈

**前端技术栈**
- Vue 3
- TypeScript
- Element Plus UI
- Vue Router
- Pinia 状态管理
- MD Editor（Markdown编辑器）
- Axios

**后端技术栈**
- FastAPI
- MySQL
- SQLAlchemy ORM
- JWT 认证
- 数据库连接池


## 🚀 快速开始

### 前置要求
- Node.js ≥16.x
- Python ≥3.8
- MySQL ≥5.7

### 后端部署
1. 创建数据库
```bash
mysql -u root -p < blog_serve.sql
```

2.安装依赖
```bash
cd Blog_serve
pip install -r requirements.txt
```

3.启动服务
```bash
uvicorn main:app --reload
```

### 前端部署
1. 安装依赖
```bash
cd Blog
npm install
```

2. 启动服务
```bash
npm run serve
```
