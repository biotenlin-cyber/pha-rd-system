<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { fetchPatent } from '@/api/patents'
import PatentStatusTag from '@/components/PatentStatusTag.vue'
import type { PatentDetail } from '@/types/models'

const route = useRoute()
const patent = ref<PatentDetail | null>(null)

const code = computed(() => String(route.params.code ?? ''))

const load = async () => {
  if (!code.value) return
  patent.value = await fetchPatent(code.value)
}

onMounted(load)
watch(code, load)

const tabs = [
  { name: 'patent-detail-overview', label: '概览' },
  { name: 'patent-detail-disclosure', label: '技术交底' },
  { name: 'patent-detail-drafts', label: '申请文件 / AI 起草' },
  { name: 'patent-detail-oas', label: '审查意见' },
]
</script>

<template>
  <div v-if="patent" class="patent-detail">
    <RouterLink to="/patents" class="back">← 返回专利列表</RouterLink>
    <header class="head">
      <code class="code">{{ patent.internal_code }}</code>
      <h1>{{ patent.title_zh }}</h1>
      <PatentStatusTag :status="patent.legal_status" />
    </header>
    <div class="meta">
      <span v-if="patent.publication_no">公开号 <b>{{ patent.publication_no }}</b></span>
      <span v-if="patent.application_no">申请号 <b>{{ patent.application_no }}</b></span>
      <span v-if="patent.application_date">申请日 <b>{{ patent.application_date }}</b></span>
      <span>国家 <b>{{ patent.country_code }}</b></span>
      <span>类型 <b>{{ patent.patent_type }}</b></span>
    </div>

    <nav class="tabs">
      <RouterLink
        v-for="t in tabs"
        :key="t.name"
        :to="{ name: t.name, params: { code: patent.internal_code } }"
        active-class="active"
      >
        {{ t.label }}
      </RouterLink>
    </nav>

    <RouterView :patent="patent" @reload="load" />
  </div>
</template>

<style scoped>
.patent-detail {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.back {
  font-size: 13px;
  color: var(--pha-muted);
}
.head {
  display: flex;
  align-items: center;
  gap: 12px;
  flex-wrap: wrap;
}
.head h1 {
  margin: 0;
  font-size: 22px;
}
.code {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  background: var(--pha-primary-soft);
  color: var(--pha-primary);
  padding: 4px 10px;
  border-radius: 8px;
  font-weight: 700;
}
.meta {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  color: var(--pha-muted);
  font-size: 13px;
}
.tabs {
  display: flex;
  gap: 12px;
  border-bottom: 1px solid var(--pha-border);
}
.tabs a {
  padding: 8px 4px;
  color: var(--pha-muted);
  text-decoration: none;
  border-bottom: 2px solid transparent;
}
.tabs a.active {
  color: var(--pha-primary);
  border-bottom-color: var(--pha-primary);
  font-weight: 600;
}
</style>
