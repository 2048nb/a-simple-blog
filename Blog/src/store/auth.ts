// stores/auth.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

export interface User {
    id: number
    username: string 
}

export interface Token {
    access_token: string
    token_type: string
}

export const useAuthStore = defineStore('auth', () => {
    // 状态
    const isLoggedIn = ref(false)           // 是否登录
    const token = ref<string | null>(null)  // 认证token
    const user = ref<User | null>(null)     // 当前用户信息

    // 获取器
    const isAuthenticated = computed(() => !!token.value) // 是否已认证
    const currentUser = computed(() => user.value)        // 当前用户
    const isLogged = computed(() => isLoggedIn.value) // 是否登录状态

    // 动作
    /**
     * 登录方法
     * @param newToken 新的认证token
     * @param newUser 新的用户信息
     */
    const login = (newToken: Token, newUser: User) => {
        token.value = newToken.token_type + ' ' + newToken.access_token
        user.value = newUser
        isLoggedIn.value = true
        localStorage.setItem('auth_token', token.value) // 存储token到本地存储
        localStorage.setItem('user', JSON.stringify(newUser)) // 存储用户信息到本地存储
        
    }

    const logout = () => {
        token.value = null
        user.value = null
        isLoggedIn.value = false
        localStorage.removeItem('auth_token')
        localStorage.removeItem('user')
    }
    // 初始化认证状态
    // 这里可以在应用启动时调用，检查本地存储中是否有token
    const initAuth = () => {
        const savedToken = localStorage.getItem('auth_token')
        const savedUser = localStorage.getItem('user')
        if (savedToken && savedUser) {
            token.value = savedToken
            isLoggedIn.value = true 
            user.value = JSON.parse(savedUser)
        }

    }



    return {
        isLoggedIn,
        token,
        user,
        isAuthenticated,
        currentUser,
        isLogged,
        login,
        logout,
        initAuth
    }
})

