<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useDomainStore } from '@/stores/domain'
import { listGrades } from '@/api/grades'
import DomainCard from '@/components/DomainCard.vue'
import GradeCard from '@/components/GradeCard.vue'
import type { Grade } from '@/types/models'

const domainStore = useDomainStore()
const grades = ref<Grade[]>([])

const totalScenarios = computed(() =>
  domainStore.domains.reduce((s, d) => s + d.scenario_count, 0),
)

onMounted(async () => {
  await domainStore.load()
  grades.value = await listGrades()
})
</script>

<template>
  <div class="home">
    <section class="hero">
      <h1>PHA 应用知识库</h1>
      <p>
        覆盖医疗、可降解包装、农业、海洋、3D 打印、纺织、电子、化妆品、建筑、碳中和等
        <b>{{ domainStore.domains.length }}</b> 个领域，沉淀 <b>{{ totalScenarios }}</b> 个应用场景与
        <b>{{ grades.length }}</b> 个 PHA 牌号的匹配关系。
      </p>
    </section>

    <section class="block">
      <h2>应用领域</h2>
      <div class="grid">
        <DomainCard v-for="d in domainStore.domains" :key="d.id" :domain="d" />
      </div>
    </section>

    <section class="block">
      <h2>PHA 牌号</h2>
      <div class="grid grades">
        <GradeCard v-for="g in grades" :key="g.id" :grade="g" />
      </div>
    </section>
  </div>
</template>

<style scoped>
.home {
  display: flex;
  flex-direction: column;
  gap: 32px;
}
.hero {
  background: linear-gradient(135deg, #e6f5ee, #ffffff 60%);
  border: 1px solid var(--pha-border);
  border-radius: var(--pha-radius);
  padding: 32px 28px;
}
.hero h1 {
  margin: 0 0 12px;
  font-size: 28px;
  color: var(--pha-text);
}
.hero p {
  margin: 0;
  color: var(--pha-muted);
  line-height: 1.7;
  max-width: 800px;
}
.block h2 {
  font-size: 18px;
  margin: 0 0 14px;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(260px, 1fr));
  gap: 14px;
}
.grid.grades {
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
}
</style>
