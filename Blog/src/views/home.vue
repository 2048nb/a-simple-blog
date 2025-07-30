<template>
    <div class="container">
        <div v-for="post in posts" :key="post['post_id']" class="postDiv">
            <postBlock :data="post"/>
        </div>
    </div>
    <div v-if="posts.length >= 10">
        翻页模块
    </div>
</template>

<script setup lang="ts">
import postBlock from '@/components/postBlock.vue';
import { useAuthStore } from '@/store/auth';
import { getAllPostsApi, getCollectPostIdApi } from '@/utils/request';
import { ElMessage } from 'element-plus';
import { onMounted, ref } from 'vue';
const posts = ref([]);
const { currentUser} = useAuthStore();
async function refreshPosts() {
    try {
        const res = await getAllPostsApi();
        if (res.code === 200) {
            posts.value = res.data;
        }
        else {
            ElMessage.error(res.message);
        }
        console.log(posts.value);
        
    } catch (error) {
        ElMessage.error('获取帖子失败');
    }
}




onMounted(() => {
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