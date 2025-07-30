<template>
    <div class="comment-container">
        <div class="left">
            <el-avatar 
                src="https://cube.elemecdn.com/0/88/03b0d39583f48206768a7534e55bcpng.png" 
            />
        </div>
        <div class="right">
            <el-text style="font-weight: bold;">{{ commentData['comment_author_name'] }}</el-text>
            <el-text size = "large" > {{ commentData['comment_content'] }}</el-text>
            <el-text type = "info">{{ commentData['comment_date'] }}</el-text>
        </div>
    </div>
</template>

<script setup lang="ts">

const { commentData } = defineProps(['commentData']);


</script>


<style scoped>
.comment-container {
    display: flex;
    align-items: flex-start;
    margin-bottom: 10px;
}
.comment-container > div:not(:last-child) {
  border-right: 1px solid var(--el-border-color);
}

.left {
    width: 7%;
}

.right {
    display: flex;
    flex-direction: column;
    flex: 1;
    padding-left: 10px;
    text-align: left;
}
.right :deep(.el-text) {
    text-align: left;
    align-self: flex-start;
    width: 100%;
    margin-bottom: 5px;
}
</style>
