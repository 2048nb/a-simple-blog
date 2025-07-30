import { defineStore } from 'pinia'
import { computed, ref } from 'vue'

export const usePostsStore = defineStore('posts', () => {
    // 状态
    const refreshTrigger = ref(0) // 刷新触发器
    const isWriting = ref(false) // 是否正在写作
    // 获取器
    const refreshTriggerValue = computed(() => refreshTrigger.value) // 获取刷新触发器的值
    const isWritingPost = computed(() => isWriting.value) // 是否正在写作状态

    // 动作
    const triggerRefresh = () => {
        refreshTrigger.value += 1 // 增加刷新触发器的值
    }
    const startWriting = () => {
        isWriting.value = true // 开始写作
    }
    const stopWriting = () => {
        isWriting.value = false // 结束写作
    }

    return {
        refreshTrigger,
        refreshTriggerValue,
        isWritingPost,
        triggerRefresh,
        startWriting,
        stopWriting
    }
})