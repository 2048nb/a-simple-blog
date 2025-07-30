<template>
    <div class="bar">
        <ElMenu :default-active="activeIndex" class="el-menu-demo" mode="horizontal" :collapse=false :router=true>
            <ElMenuItem index="/home">首页</ElMenuItem>
            <ElMenuItem v-show="authStore.isLogged" index="/publish">写文章</ElMenuItem>
            <ElMenuItem v-show="authStore.isLogged" index="/myposts">我的帖子</ElMenuItem>
            <ElMenuItem v-show="authStore.isLogged" index="/mycollection">我的收藏</ElMenuItem>
            <ElButton v-show="!authStore.isLogged" type="default" class="bar_btn" @click="register">注册</ElButton>
            <ElButton v-show="!authStore.isLogged" type="primary" class="bar_btn" @click="login">登录</ElButton>
            <ElButton v-show="authStore.isLogged" type="danger" class="bar_btn" @click="logout">退出</ElButton>
        </ElMenu>
    </div>
</template>

<script lang="ts" setup>
import { ElButton, ElMenu, ElMenuItem } from 'element-plus'
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/store/auth'

const authStore = useAuthStore()

// const islogin = computed(() => authStore.isLoggedIn) // 是否登录状态
const activeIndex = ref('/home') // 默认选中首页
// 监听路由变化，更新选中项
const router = useRouter()

function register() {
    // 注册逻辑
    router.push('/register')
}

function login() {
    // 登录逻辑
    router.push('/login')
}

function logout() {
    // 退出登录逻辑
    authStore.logout()
    // 清除本地存储
    localStorage.clear();
    // 清除认证状态后跳转到首页
    router.replace('/home')    
}
</script>


<style scoped>
.el-menu-demo {
    display: block;
    background-color: #f5f5f5;
}
.bar_btn {
    float: right;
    margin-left: 10px;
    margin-top: 15px;
    border-radius: 5px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}
.bar {
  position: fixed;
  top: 0;
  width: 70%;
  z-index: 1000;
}
</style>
