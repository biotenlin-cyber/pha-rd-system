<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import { useRoute } from 'vue-router'
import { fetchGrade } from '@/api/grades'
import MatchTable from '@/components/MatchTable.vue'
import PerformanceRadar from '@/components/PerformanceRadar.vue'
import PlaceholderLinks from '@/components/PlaceholderLinks.vue'
import type { GradeDetail } from '@/types/models'

const route = useRoute()
const grade = ref<GradeDetail | null>(null)

const load = async (code: string) => {
  grade.value = await fetchGrade(code)
}

onMounted(() => load(route.params.code as string))
watch(() => route.params.code, (c) => c && load(c as string))
</script>

<template>
  <div v-if="grade" class="grade-detail">
    <RouterLink to="/grades" class="back">← 返回牌号库</RouterLink>
    <header class="head">
      <code class="code">{{ grade.code }}</code>
      <h1>{{ grade.name_zh }}</h1>
      <span class="family">{{ grade.polymer_family }}</span>
    </header>
    <p v-if="grade.description" class="desc">{{ grade.description }}</p>

    <div class="row">
      <section class="card">
        <h3>关键性能</h3>
        <ul class="kv">
          <li><span>熔点 Tm</span><b>{{ grade.tm_celsius ?? '—' }} ℃</b></li>
          <li><span>玻璃化温度 Tg</span><b>{{ grade.tg_celsius ?? '—' }} ℃</b></li>
          <li><span>结晶度</span><b>{{ grade.crystallinity_pct ?? '—' }} %</b></li>
          <li><span>断裂伸长率</span><b>{{ grade.elongation_at_break_pct ?? '—' }} %</b></li>
          <li><span>拉伸强度</span><b>{{ grade.tensile_strength_mpa ?? '—' }} MPa</b></li>
          <li><span>杨氏模量</span><b>{{ grade.youngs_modulus_gpa ?? '—' }} GPa</b></li>
          <li><span>生物相容性</span><b>{{ grade.biocompatibility_class ?? '—' }}</b></li>
          <li><span>土壤降解</span><b>{{ grade.degradation_months_soil ?? '—' }} 月</b></li>
          <li><span>海水降解</span><b>{{ grade.degradation_months_marine ?? '—' }} 月</b></li>
          <li><span>典型工艺</span><b>{{ (grade.typical_processing as string[]).join(', ') || '—' }}</b></li>
        </ul>
      </section>
      <section class="card">
        <h3>性能雷达</h3>
        <PerformanceRadar :grade="grade" />
      </section>
    </div>

    <section>
      <h3>匹配的应用场景 ({{ grade.matches.length }})</h3>
      <MatchTable :matches="grade.matches" row-type="scenario" />
    </section>

    <PlaceholderLinks :links="[]" title="关联专利 / 项目" />
  </div>
</template>

<style scoped>
.grade-detail {
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
  flex-wrap: wrap;
}
.head h1 {
  margin: 0;
  font-size: 24px;
}
.code {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  background: var(--pha-primary-soft);
  color: var(--pha-primary);
  padding: 4px 10px;
  border-radius: 8px;
  font-weight: 700;
}
.family {
  margin-left: auto;
  color: var(--pha-muted);
  font-size: 13px;
}
.desc {
  color: var(--pha-muted);
  line-height: 1.7;
  margin: 0;
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
.card h3, section h3 {
  font-size: 16px;
  margin: 0 0 10px;
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
  border-bottom: 1px dashed var(--pha-border);
}
.kv li:last-child {
  border-bottom: 0;
}
.kv span {
  color: var(--pha-muted);
}
</style>
