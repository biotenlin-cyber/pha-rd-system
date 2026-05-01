<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { fetchScenario } from '@/api/scenarios'
import MatchTable from '@/components/MatchTable.vue'
import TagChip from '@/components/TagChip.vue'
import PlaceholderLinks from '@/components/PlaceholderLinks.vue'
import type { ScenarioDetail } from '@/types/models'

const route = useRoute()
const scenario = ref<ScenarioDetail | null>(null)

const load = async (code: string) => {
  scenario.value = await fetchScenario(code)
}

const formatMarket = (n: number | null) => {
  if (!n) return '—'
  if (n >= 1e9) return `${(n / 1e9).toFixed(2)} B USD`
  if (n >= 1e6) return `${(n / 1e6).toFixed(1)} M USD`
  return `${n} USD`
}

interface TypicalProduct {
  name: string
  description?: string
}
const productName = (p: unknown) => (p as TypicalProduct).name
const productDescription = (p: unknown) => (p as TypicalProduct).description ?? ''

onMounted(() => load(route.params.code as string))
watch(() => route.params.code, (c) => c && load(c as string))
</script>

<template>
  <div v-if="scenario" class="scenario-detail">
    <RouterLink :to="`/domains/${scenario.domain_code}`" class="back">
      ← 返回 {{ scenario.domain_code }} 领域
    </RouterLink>
    <header class="head">
      <h1>{{ scenario.name_zh }}</h1>
      <span class="en">{{ scenario.name_en }}</span>
      <code class="code">{{ scenario.code }}</code>
    </header>
    <p class="summary">{{ scenario.summary }}</p>

    <div class="tags">
      <TagChip v-for="t in scenario.tags" :key="t.id" :tag="t" />
    </div>

    <div class="row">
      <section class="card">
        <h3>技术要求</h3>
        <pre v-if="Object.keys(scenario.technical_requirements).length">{{
          JSON.stringify(scenario.technical_requirements, null, 2)
        }}</pre>
        <p v-else class="muted">未提供。</p>
      </section>

      <section class="card">
        <h3>市场信息</h3>
        <ul class="kv">
          <li><span>规模 (估)</span><b>{{ formatMarket(scenario.market_size_usd) }}</b></li>
          <li><span>统计年份</span><b>{{ scenario.market_year ?? '—' }}</b></li>
          <li v-if="scenario.market_notes"><span>备注</span><b>{{ scenario.market_notes }}</b></li>
        </ul>

        <h3 style="margin-top:16px">典型产品</h3>
        <ul v-if="scenario.typical_products.length">
          <li v-for="(p, i) in scenario.typical_products" :key="i">
            <b>{{ productName(p) }}</b>
            <span class="muted"> — {{ productDescription(p) }}</span>
          </li>
        </ul>
        <p v-else class="muted">未提供。</p>
      </section>
    </div>

    <section>
      <h3>匹配的 PHA 牌号</h3>
      <MatchTable :matches="scenario.matches" row-type="grade" />
    </section>

    <PlaceholderLinks :links="scenario.external_links" title="关联专利 / 项目" />
  </div>
</template>

<style scoped>
.scenario-detail {
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
  gap: 10px;
  flex-wrap: wrap;
}
.head h1 {
  margin: 0;
  font-size: 26px;
}
.en {
  color: var(--pha-muted);
  font-size: 14px;
}
.code {
  margin-left: auto;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 12px;
  color: var(--pha-muted);
  background: var(--pha-primary-soft);
  padding: 2px 8px;
  border-radius: 6px;
}
.summary {
  margin: 0;
  color: var(--pha-text);
  line-height: 1.7;
}
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}
@media (max-width: 720px) {
  .row { grid-template-columns: 1fr; }
}
.card {
  background: var(--pha-card-bg);
  border: 1px solid var(--pha-border);
  border-radius: var(--pha-radius);
  padding: 16px 18px;
}
.card h3 {
  margin: 0 0 10px;
  font-size: 14px;
}
.muted {
  color: var(--pha-muted);
  font-size: 13px;
  margin: 0;
}
pre {
  background: #f6f8f7;
  padding: 10px;
  border-radius: 6px;
  font-size: 12px;
  line-height: 1.6;
  overflow: auto;
  margin: 0;
}
.kv {
  list-style: none;
  padding: 0;
  margin: 0;
}
.kv li {
  display: flex;
  justify-content: space-between;
  font-size: 13px;
  padding: 4px 0;
}
.kv span {
  color: var(--pha-muted);
}
ul {
  margin: 0;
  padding-left: 16px;
  font-size: 13px;
  line-height: 1.8;
}
section h3 {
  font-size: 16px;
  margin: 0 0 10px;
}
</style>
