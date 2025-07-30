<template>
    <div class=" register">
        <h1>注册</h1>
        <el-form @submit.prevent="register" label-width="80px">
            <el-input v-model="registerForm.username" placeholder="请输入用户名" :suffix-icon="User" />
            <el-input v-model="registerForm.password" placeholder="请输入密码" :suffix-icon="Lock" />
            <el-input v-model="registerForm.passwordAgain" placeholder="请再次输入密码" :suffix-icon="Lock" />
            <el-button type="primary" native-type="submit">注册</el-button>
        </el-form>
        <span style="font-size: small;">已有账号？<RouterLink to="/login" style="color: #409eff;">登录</RouterLink></span>
    </div>

</template>

<script lang="ts" setup>
import { ElMessage } from 'element-plus';
import { reactive } from 'vue';
import { User, Lock } from '@element-plus/icons-vue';
import { registerApi } from '@/utils/request'
import router from '@/router';


const registerForm = reactive({
    username: '',
    password: '',
    passwordAgain: ''
})

async function register() {
    try {
        if (registerForm.password !== registerForm.passwordAgain) { 
            ElMessage.error('两次密码不一致')
            return
        }
        const response = await registerApi(registerForm.username, registerForm.password, registerForm.passwordAgain)
        if (response.code !== 200) { 
            ElMessage.error('注册失败')
            return
        }
        ElMessage.success('注册成功,请登录')
        router.push('/login')
    }
    catch (error) {
        ElMessage.error('注册失败')
    }
}
</script>

<style scoped>
.register {
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
