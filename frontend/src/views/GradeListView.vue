<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { listGrades } from '@/api/grades'
import GradeCard from '@/components/GradeCard.vue'
import type { Grade } from '@/types/models'

const grades = ref<Grade[]>([])

onMounted(async () => {
  grades.value = await listGrades()
})
</script>

<template>
  <div class="grade-list">
    <header>
      <h1>PHA 牌号库</h1>
      <p class="muted">共 {{ grades.length }} 个牌号，覆盖 scl-PHA、共聚物与 mcl-PHA 三大家族。</p>
    </header>
    <div class="grid">
      <GradeCard v-for="g in grades" :key="g.id" :grade="g" />
    </div>
  </div>
</template>

<style scoped>
.grade-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
header h1 {
  margin: 0;
  font-size: 26px;
}
.muted {
  color: var(--pha-muted);
  margin: 4px 0 0;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 14px;
}
</style>
