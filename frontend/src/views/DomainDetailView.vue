<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { listScenarios } from '@/api/scenarios'
import { fetchDomain } from '@/api/domains'
import ScenarioCard from '@/components/ScenarioCard.vue'
import type { Domain, ScenarioSummary } from '@/types/models'

const route = useRoute()
const domain = ref<Domain | null>(null)
const scenarios = ref<ScenarioSummary[]>([])
const loading = ref(false)

const load = async (code: string) => {
  loading.value = true
  try {
    domain.value = await fetchDomain(code)
    const page = await listScenarios({ domain: code, page_size: 100 })
    scenarios.value = page.data
  } finally {
    loading.value = false
  }
}

onMounted(() => load(route.params.code as string))
watch(
  () => route.params.code,
  (c) => c && load(c as string),
)
</script>

<template>
  <div v-if="domain" class="domain-detail">
    <RouterLink to="/" class="back">← 返回领域列表</RouterLink>
    <header class="head">
      <h1>{{ domain.name_zh }}</h1>
      <span class="en">{{ domain.name_en }}</span>
    </header>
    <p class="desc">{{ domain.description }}</p>

    <h2>应用场景 ({{ scenarios.length }})</h2>
    <el-empty v-if="!loading && scenarios.length === 0" description="暂无场景" />
    <div class="grid">
      <ScenarioCard v-for="s in scenarios" :key="s.id" :scenario="s" />
    </div>
  </div>
</template>

<style scoped>
.domain-detail {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.back {
  font-size: 13px;
  color: var(--pha-muted);
}
.head {
  display: flex;
  align-items: baseline;
  gap: 12px;
}
.head h1 {
  margin: 0;
  font-size: 26px;
}
.en {
  color: var(--pha-muted);
  font-size: 14px;
}
.desc {
  color: var(--pha-muted);
  margin: 0;
  max-width: 800px;
  line-height: 1.7;
}
h2 {
  font-size: 18px;
  margin: 16px 0 0;
}
.grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
}
</style>
