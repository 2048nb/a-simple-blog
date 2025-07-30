<template>
    <div class="container">
        <div v-for="post in posts" :key="post['post_id']" class="postDiv">
            <postBlock :data="post"/>
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, watch, ref } from 'vue';
import postBlock from '../components/postBlock.vue'
import { getMyPostsApi } from '@/utils/request';
import { ElMessage } from 'element-plus';
import { useAuthStore } from '@/store/auth';
import { usePostsStore } from '@/store/post';

const authStore = useAuthStore();
const postsStore = usePostsStore();
const posts = ref([])

async function refreshPosts() {
    try {
        if (!authStore.currentUser?.id) {
            ElMessage.error('请先登录');
            return;
        }
        const res = await getMyPostsApi(authStore.currentUser?.id);
        if (res.code === 200) {
            posts.value = res.data;
        } else {
            ElMessage.error('无帖子数据');
        }
    } catch (error) {
        console.error('获取我的帖子失败:', error);
    }
}



onMounted(() => {
    refreshPosts();
});

watch(() => postsStore.refreshTrigger, () => {
    refreshPosts();
});


</script>

<style scoped>
.container {
    display: flex;
    flex-wrap: wrap;

}
.postDiv {
    width: 31%;
    margin: 10px;

}
</style>