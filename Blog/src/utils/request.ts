import axios from 'axios';
import router from '@/router'; 
import { ElMessage } from 'element-plus';
// 创建实例
const request = axios.create({
    baseURL: 'http://localhost:8000', // 基础URL
    timeout: 10 * 1000, // 超时时间
    // headers: { 'Content-Type': 'application/x-www-form-urlencoded' }
});

// 请求拦截器
request.interceptors.request.use(config => {
    // 添加认证token等
    const token = localStorage.getItem('auth_token'); // 从本地存储中获取token
    if (token) {
        config.headers['token'] = token; // 添加认证token到请求头
    }
    
    return config; // 返回配置
}, error => {
    return Promise.reject(error);
});

// 响应拦截器
request.interceptors.response.use(response => {
    return response;
}, error => {
    // 统一处理错误
    console.log('错误拦截器:', error.response);
    
    if (error.response?.status === 401) {
        // 查看详细的错误消息
        const message = error.response.data?.message;

        if (message === 'expired token') {
            ElMessage.error('登录已过期，请重新登录');
            // 清除本地存储
            localStorage.clear();
            // 跳转到登录页面
            router.replace('/login');
        } else if (message === 'invalid token') {
            ElMessage.error('无效的token，请重新登录');
            // 清除本地存储
            localStorage.clear();
            // 跳转到登录页面
            router.replace('/login');
        }
    }
    return Promise.reject(error);
});



// 导出一个异步函数loginApi，用于登录
export const loginApi = async (username: string, password: string) => { 
    // 创建一个FormData对象，用于存储用户名和密码
    const formData = new FormData();
    // 将用户名和密码添加到FormData对象中
    formData.append('username', username);
    formData.append('password', password);
    // 发送POST请求，将FormData对象作为参数
    const response = await post('/user/login', formData);
    // 返回响应中的核心数据
    return response.data; // 返回核心数据
}

export const registerApi = async (username: string, password: string, passwordAgain: string) => {
    const formData = new FormData();
    formData.append('username', username);
    formData.append('password', password);
    formData.append('passwordAgain', passwordAgain);
    const response = await post('/user/register', formData);
    return response.data;
}

export const getAllPostsApi = async (page: number = 1) => {
    const response = await get(`/post/get_all/?page=${page}`);
    return response.data;
}

export const getCollectPostsApi = async (user_id: number) => {
    const response = await get(`post/mycollection/${user_id}`);
    return response.data;
}

export const getMyPostsApi = async (user_id: number) => {
    const response = await get(`post/${user_id}`);
    return response.data;
}

export const getPostApi = async (post_id: number) => {
    const response = await get(`/post/detail/${post_id}`);
    return response.data;
}

export const deletePostApi = async (post_id: number) => {
    const response = await del(`/post/delete/${post_id}`);
    return response.data;
}

export const deleteCollectPostApi = async (deleteCollection: any) => { 
    const response = await del(`/post/delete_collection/`, deleteCollection);
    return response.data;
}

export const getCollectPostIdApi = async (user_id: number) => {
    const response = await get(`/user/collection/${user_id}`);
    return response.data;
}

export const addCollectPostApi = async (addCollection: any) => {
    const response = await post(`/post/add_collection/`, addCollection);
    return response.data;
}  

export const createPostApi = async (postContent: any) => {
    const response = await post(`/post/create/`, postContent);
    return response.data;
}

export const updataPostApi = async (modifyContent: any) => {
    const response = await put(`/post/update/`, modifyContent);
    return response.data;
}

export const addCommentApi = async (comment: any) => {
    const response = await post(`/comment/add_comment/`, comment);
    return response.data;
}

export const getCommentsApi = async (post_id: number) => {
    const response = await get(`/comment/get_comments?post_id=${post_id}`);
    return response.data;
}










// 封装GET请求
export const get = (url: string, params = {}) => {
    return request.get(url, { params });
};

// 封装POST请求
export const post = (url: string, data = {}) => {
    return request.post(url, data);
}

// 封装PUT请求
export const put = (url: string, data = {}) => {
    return request.put(url, data);
}

// 封装DELETE请求
export const del = (url: string, data = {}) => {
    return request.delete(url, { data });
}
export default request;