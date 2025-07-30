<template>
    <div class="container">
        <el-button v-if="isAuthor" type="primary" @click="editorChange" :icon="EditPen" circle/>
        <el-button :type="isStar? 'warning' : ''" @click="starPost" :icon="Star" circle/>
        <h1 style="text-align: center;">{{ title }}</h1>
        <div class="md">
            <div class="md-catalog">
                <MdCatalog 
                    :editorId="post_id" 
                    :scrollElement="contentScrollElement" 
                    :key="catalogKey"  
                    
                />
            </div>
            <div class="md-content" ref="contentScrollElement">
                <MdPreview 
                    :editorId="post_id" 
                    :modelValue="content" 
                    previewTheme="github"
                    theme="light"
                />
                
            </div>
        </div>
        <div class="commentInput">
            <el-input 
                type="textarea" 
                v-model="comment" 
                placeholder="请输入评论内容"
                :autosize = "{ minRows: 2, maxRows: 4}"
                maxlength="200"
                show-word-limit
            />
            <div style="width: 100%; overflow: auto;">
                <el-button
                    type="primary"
                    @click="submitComment"
                    style="margin-top: 10px; float: right;"
                >
                发表评论
                </el-button>
            </div>
        </div>
        <h1>评论</h1>
        <div class="commentList">
            <commentBlock v-for="comment in comments" :commentData = "comment" :key="comment['id']" />
        </div> 
    </div>
</template>

<script setup lang="ts">
import { onMounted, ref, nextTick, watch, onUnmounted } from 'vue';
import { MdPreview, MdCatalog } from 'md-editor-v3';
import 'md-editor-v3/lib/preview.css';
import { useRoute, useRouter } from 'vue-router';
import { getPostApi, addCommentApi, getCommentsApi, getCollectPostIdApi, addCollectPostApi, deleteCollectPostApi } from '@/utils/request';
import { useAuthStore } from '@/store/auth';
import { Star, EditPen } from '@element-plus/icons-vue';
import { ElMessage } from 'element-plus';
import commentBlock from '@/components/commentBlock.vue';




const route = useRoute();
const router = useRouter();
const { currentUser } = useAuthStore();
const isAuthor = ref(false);
const isStar = ref(false);
const contentScrollElement = ref<HTMLElement | undefined>(undefined);
const catalogKey = ref(0);


const title = ref('');
const post_id = 'md-' + route.params.post_id;
const content = ref('# Loading');
const comment = ref('');
const postId = route.params.post_id;

const comments = ref([]);

onMounted(() => {
    getPostDetail();
    getComments();
    isStarPost();
});

async function getPostDetail() {
    const res = await getPostApi(Number(route.params.post_id));
    console.log(res);
    content.value = res.data.post_content;
    title.value = res.data.post_title;
    isAuthor.value = res.data.user_id === currentUser?.id;    

    await nextTick();  // 确保DOM已更新
    // 确保滚动元素已正确绑定
    watch (contentScrollElement, (el) => {
        if (el) catalogKey.value++;
    }, { immediate: true });
}


async function getComments() { 
    const res = await getCommentsApi(Number(route.params.post_id)); 
    if (res.code === 200) {
        comments.value = res.data;
    } else {
        console.log(res.message);
    } 
}


function editorChange() {
    localStorage.setItem('draft', JSON.stringify({post_id: route.params.post_id , title: title.value, content: content.value }));
    router.push({
        path: '/publish',
        query: {
            post_id: route.params.post_id,
        }
    });
}

function starPost() {
    isStar.value = !isStar.value;
    if (isStar.value) {
        ElMessage.success('已收藏');
    } else {
        ElMessage.success('已取消收藏');
    }

}

function isStarPost() {
    const startList = JSON.parse(localStorage.getItem('star_post_id') || '[]');
    
    isStar.value = startList?.includes(Number(route.params.post_id));
    console.log(isStar.value);
    
}

async function submitComment() {    
    if (comment.value === '') {
        return;
    }
    const res = await addCommentApi({ post_id: route.params.post_id, content: comment.value, user_id: currentUser?.id });
    if (res.code === 200) {
        ElMessage.success('评论成功');
        comment.value = '';
        getComments();
    }

}

async function addOrDeleteCollection() {
    const startList = JSON.parse(localStorage.getItem('star_post_id') || '[]');
    console.log(isStar.value, startList);
    
    if (isStar.value && !startList?.includes(Number(postId))) { 
        console.log('添加收藏',postId,startList?.includes(Number(postId)));
        
        const res = await addCollectPostApi({user_id: Number(currentUser?.id), post_id: Number(postId)});
        if (res.code !== 200) {
            console.log(`id为${postId}的帖子收藏失败:`, res.message);
            return;
        }
        localStorage.setItem('star_post_id', JSON.stringify([...startList, Number(postId)])); // 保存收藏到本地存储
    }
    else if (!isStar.value && startList?.includes(Number(postId))) {
        const res = await deleteCollectPostApi({ post_id: Number(postId), user_id: Number(currentUser?.id) });
        console.log('取消收藏');
        if (res.code !== 200) {
            console.log(`id为${postId}的帖子取消收藏失败:`, res.message);
            return;
        }
        const newStartList = startList.filter((id: number) => id !== Number(postId));
        localStorage.setItem('star_post_id', JSON.stringify(newStartList)); // 更新收藏列表
        
    }
}

onUnmounted(() => {
    addOrDeleteCollection();
});

</script>




<style scoped>
.container {
    min-height: calc(100vh - 150px);
    padding: 20px;
    border: 1px solid #e6e6e6;
    border-radius: 5px;
    background-color: #fff;
    width: 100%;
}
.md {
    display: flex;
    flex-direction: row;
    justify-content: space-between;
    align-items: flex-start;
    width: 100%;
}
.md-catalog {
    width: 25%;
    margin-right: 3px;
    border-right: 1px solid #e6e6e6;
    height: calc(100vh - 150px);
    overflow-y: auto;
    border-radius: 5px;
    scrollbar-width: none;
    -ms-overflow-style: none;
    position: sticky;
    top: 20px;
}
.md-catalog::-webkit-scrollbar {
    display: none; /* Chrome, Safari, Opera */
}
.md-content {
    margin-left: 3px;
    flex: 1;
    overflow-x: hidden;
    overflow-y: auto;
    height: calc(100vh - 150px);
    border-radius: 5px;
    scrollbar-width: none;    /* */ 
    -ms-overflow-style: none;
}

.scroll-.md-content::-webkit-scrollbar {
  display: none;
}


.commentInput {
    margin-top: 20px;
    padding: 10px;
    border-radius: 5px;
    width: 100%;
}
.commentList {

    padding: 10px;
    border-radius: 5px;
    width: 100%;
}

@media (max-width: 768px) {
    .md {
        flex-direction: column;
    }
    .md-catalog {
        width: 100%;
        position: static;
        max-height: none;
        border-bottom: 1px solid #b0b0b0;
        border-right: none;
    }
}
</style>