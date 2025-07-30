<template>
  <div class="article-container">
    <!-- 标题输入区域 -->
    <div class="title-wrapper">
      <el-input
        size="large"
        v-model="title"
        maxlength="100"
        show-word-limit
        placeholder="请输入文章标题"
        class="title-input"
      />
    </div>
    <!-- 内容输入区域 -->
    <div>
      <MdEditor v-model="text" class="md-editor" />
    </div>
    <div class="btn_div">
      <el-button v-if="!route.query.post_id" type="primary" @click="upload">发布</el-button>
      <el-button v-if="route.query.post_id" type="primary" @click="update">更新</el-button>
      <el-button type="primary" @click="clearDraft" style="float: right;">清空</el-button>
    </div>
  </div>

  <div>
   
  </div>
</template>

<script setup>
import { onMounted, ref, watch } from 'vue';
import { ElButton, ElMessage} from 'element-plus';
import { useAuthStore } from '@/store/auth';
import { createPostApi, updataPostApi } from '@/utils/request';
import { MdEditor } from 'md-editor-v3';
import 'md-editor-v3/lib/style.css';
import { useRoute, useRouter } from 'vue-router';

const { currentUser } = useAuthStore();
const route = useRoute();
const router = useRouter();
// 标题双向绑定变量
const title = ref('');
// 内容双向绑定变量
const text = ref('');

// 监听text是否有内容，如果有则保存到本地存储，如果没有则删除本地存储
watch(text, (newValue) => {
  if (newValue.trim() !== '' ) {
    localStorage.setItem('draft', JSON.stringify({post_id: route.query.post_id, title: title.value, content: newValue })); // 保存草稿到本地存储
  } else {
    localStorage.removeItem('draft'); // 清除草稿
  }
});



async function upload() {
  // 发布文章逻辑
  const res = await createPostApi({ title: title.value, content: text.value, author_id: currentUser.id});
  if (res.code === 200) {
    // 发布成功
    ElMessage.success('发布成功');
    // 清空输入框
    title.value = '';
    text.value = '';
    // 清空草稿
    localStorage.removeItem('draft');
  } else {
    // 发布失败
    ElMessage.error(res.message);
  }
}

async function update() {
  // 更新文章逻辑
  const res = await updataPostApi({ post_id: route.query.post_id, modify_title: title.value, modify_content: text.value});
  if (res.code === 200) {
    // 更新成功
    ElMessage.success('更新成功');
    // 清空输入框
    title.value = '';
    text.value = '';
    // 清空草稿
    localStorage.removeItem('draft');
    router.push('/publish'); // 跳转到首页
  } else {
    // 更新失败
    ElMessage.error(res.message);
  }
}

function clearDraft() {
  localStorage.removeItem('draft');
  title.value = '';
  text.value = '';
}


onMounted(() => {
  // 从本地存储加载草稿
  const draft = localStorage.getItem('draft');
  if (draft) {
    const { title: draftTitle, content: draftContent } = JSON.parse(draft);
    title.value = draftTitle;
    text.value = draftContent;
  }
})


</script>

<style scoped>
.article-container {
  margin: 20px auto;
  padding: 20px;
  border: 1px solid #e6e6e6;
  border-radius: 8px;
  background-color: #fff;
}
.title-wrapper {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}
.title-input {
  flex: 1;
  --el-input-border-color: #dcdcdc;
  --el-input-hover-border-color: #bfbfbf;
}

/* 
1、使用深度选择器：
由于 el-input 是 Element Plus 组件，其内部的输入框样式被组件库封装，需要使用 Vue 3 的深度选择器 :deep() 来穿透组件样式。
2、选择器路径：
.title-input :deep(.el-input__inner) 选择器会定位到标题输入框内部的实际输入元素。 
*/
.title-input :deep(.el-input__inner) {
  font-weight: bold;
}

.btn_div {
  margin-top: 15px;
  width: 100%;
}

.md-editor {
  height: calc(100vh - 200px);
  border-radius: 5px;
}


</style>