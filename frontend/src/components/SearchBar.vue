<script setup lang="ts">
import { ref } from 'vue'

const props = defineProps<{ initial?: string }>()
const emit = defineEmits<{ (e: 'search', q: string): void }>()

const q = ref(props.initial ?? '')

const submit = () => {
  if (!q.value.trim()) return
  emit('search', q.value.trim())
}
</script>

<template>
  <el-input
    v-model="q"
    placeholder="搜索 场景 / 牌号 / 标签"
    clearable
    @keydown.enter="submit"
  >
    <template #append>
      <el-button @click="submit">搜索</el-button>
    </template>
  </el-input>
</template>
