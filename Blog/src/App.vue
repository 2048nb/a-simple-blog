<template>
    <header v-if="showHeader">
        <bar />
    </header>
    <main>
        <RouterView />
    </main>
</template>

<script lang="ts" setup>
import bar from './components/bar.vue'
// import  Footer from './components/Footer.vue'
import { computed } from 'vue'
import { RouterView, useRoute } from 'vue-router'
import { useAuthStore } from './store/auth' 
const route = useRoute()

const authStore = useAuthStore()
// 计算是否显示导航栏
const showHeader = computed(() => {
    const path = route.path
    // 检查是否是需要隐藏导航栏的页面
    const shouldHide = path === '/login' || 
                      path === '/register' || 
                      path.startsWith('/postdetail/')
    return !shouldHide
})


</script>


<style>
body {
    width: 70%;
    margin: 0 auto;
    background-color: #f5f5f5;
}


main {
    margin-top: 70px; /*为固定导航栏预留空间*/
}
</style>
  
