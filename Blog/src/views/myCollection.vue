<template>
    <div class="container">
        <div v-for="post in posts" :key="post['post_id']" class="postDiv">
            <postBlock :data="post"/>
        </div>
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref, watch } from 'vue';
import { getCollectPostsApi } from '@/utils/request';
import postBlock from '../components/postBlock.vue';
import { ElMessage } from 'element-plus';
import { useAuthStore } from '@/store/auth';
import { usePostsStore } from '@/store/post';

const authStore = useAuthStore();
const postsStore = usePostsStore();
const posts = ref([]);

async function refreshPosts() {
    try {
        const user_id = authStore.currentUser?.id;
        if (!user_id) {
            ElMessage.error('请先登录');
            return;
        }
        const res = await getCollectPostsApi(user_id);
        
        if (res.code === 200) {
            posts.value = res.data;
        }
        else {
            ElMessage.error('无帖子数据');
        }
    } catch (error) {
        ElMessage.error('获取帖子失败');
    }
}



onMounted(async () => {
    await refreshPosts();
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