<template>
    <div class="login">
        <h1>登录</h1>
        <el-form @submit.prevent="login" label-width="80px">
            <el-input v-model="loginForm.username" placeholder="请输入用户名" :suffix-icon="User" />
            <el-input v-model="loginForm.password" type="password" placeholder="请输入密码" :suffix-icon="Lock" />
            <el-button type="primary" native-type="submit">登录</el-button>
        </el-form>
        <span style="font-size: small;">没有账号？<RouterLink to="/register" style="color: #409eff;">注册</RouterLink></span>
    </div>
</template>

<script lang="ts" setup>
import router from '@/router'
import { useAuthStore } from '@/store/auth'
import { loginApi } from '@/utils/request'
import { User, Lock } from '@element-plus/icons-vue'
import { reactive, ref } from 'vue'
import { RouterLink } from 'vue-router'
import { ElMessage } from 'element-plus'
import { getCollectPostIdApi } from '@/utils/request'

const authStore = useAuthStore()
const currentUser = authStore.currentUser;
const loginForm = reactive({
    username: '',
    password: ''
})

// 获取收藏列表
async function getStarList(id: number) {
    const res = await getCollectPostIdApi(id);
    if (res.code === 200) {
        localStorage.setItem('star_post_id', JSON.stringify(res.data));
        console.log('获取收藏列表成功:', res.data);      
    }
    else {
        console.log('获取收藏列表失败: ' + res.message);   
    }
    
}

async function login() {

    try {
        const response = await loginApi(loginForm.username, loginForm.password)
        
        if (response.code !== 200) {
            ElMessage.error('登录失败: ' + response.message)
            return
        }
        authStore.login(response.data.token, { 'id': response.data.id, 'username': response.data.username })
        //跳转到首页
        ElMessage.success('登录成功')
        // 获取收藏列表
        await getStarList(Number(response.data.id));
        // 清除登录表单
        router.replace('/home')
        loginForm.username = ''
        loginForm.password = '' 
        
    } catch (error) {
        console.error('登录失败:', error)
        return
    }
 
}


</script>

<style scoped>
.login {
    display: flex;
    flex-direction: column;
    align-items: center;
    align-items: center;
    width: 300px;
    margin: 100px auto;
    padding: 20px;
    border-radius: 10px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    background-color: #fff;
}
.el-form {
    text-align: center;
}
.el-input, .el-button {
    width: 250px;
    margin-bottom: 18px;
}
</style>