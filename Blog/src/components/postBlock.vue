<template>
    <el-card class="box-card" shadow="hover" @click="jump">
        <template #header>
            <div class="card-header">
                <el-text line-clamp="1" truncated style="font-weight: bold;" size = "large">{{ data['post_title'] }}</el-text>
                <el-popover :visible="visible" placement="top" :width="180">
                    <p>确定要删除这个帖子吗</p>
                    <div style="text-align: right; margin: 0">
                        <el-button size="small" text @click="visible = false">取消</el-button>
                        <el-button size="small" type="primary" @click.stop="deletePost">确定</el-button>
                    </div>
                    <template #reference>
                        <el-button v-if="isOnHomePage" type="danger" :icon="Delete" circle size="small" style="float: right;" @click.stop="visible = true"/>
                        <div v-else></div>
                    </template>
                </el-popover>
            </div>
        </template>
        <el-text line-clamp="2" truncated size ="small" >{{ data['post_content'] }}</el-text>
        <template #footer>
            <el-text line-clamp="1" truncated size = "small">作者：{{ data['user_name'] }}</el-text>
        </template>
    </el-card>
</template>

<script setup lang="ts">
import { Delete, Star} from '@element-plus/icons-vue'
import { computed, ref } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { deletePostApi, deleteCollectPostApi } from '@/utils/request';
import { ElMessage } from 'element-plus';
import { usePostsStore } from '@/store/post';
import { useAuthStore } from '@/store/auth';
const { data } = defineProps(['data'])

const route = useRoute()
const router = useRouter()
const { currentUser } = useAuthStore()
const visible = ref(false)
const isOnHomePage = computed(() => route.path !== '/home')
const postStore = usePostsStore()

function jump() {
    if (data && data['post_id']) {
        router.push({
            name: 'postDetail',
            params: {
                post_id: data['post_id']
            }
        }).catch((error) => {
            console.error('Router push error:', error);
        });
    } else {
        ElMessage.error('帖子数据异常，无法跳转');
        console.error('post_id is missing in data object', data);
    }
}

async function deletePost() {
    visible.value = false
    try {
        if (route.path === '/myposts') {
            var res = await deletePostApi(data['post_id']);
        }
        if (route.path === '/mycollection') {
            var res = await deleteCollectPostApi({ post_id: data['post_id'], user_id: currentUser?.id });
            const startList = JSON.parse(localStorage.getItem('star_post_id') || '[]'); // 获取本地存储的收藏列表
            const index = startList.indexOf(data['post_id']); // 查找当前帖子的索引
            if (index !== -1) {
                startList.splice(index, 1); // 如果存在，则删除
            }
            localStorage.setItem('star_post_id', JSON.stringify(startList)); // 更新本地存储的收藏列表
            console.log(startList);
            
        }
        if (res.code === 200) {
            ElMessage.success('删除成功');
            postStore.triggerRefresh();
        } else {
            ElMessage.error('删除失败: ' + res.message);
        }
    } catch (e) {
        console.log(e);
    }
}

</script>

<style>
.box-card {
    width: 100%;       /* 相对父容器宽度 */
    height: 100%;
    cursor: pointer;
}


</style>