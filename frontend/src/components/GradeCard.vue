<script setup lang="ts">
import type { Grade } from '@/types/models'

defineProps<{ grade: Grade }>()
</script>

<template>
  <RouterLink :to="`/grades/${grade.code}`" class="grade-card">
    <div class="head">
      <span class="code">{{ grade.code }}</span>
      <span class="family">{{ grade.polymer_family }}</span>
    </div>
    <h4>{{ grade.name_zh }}</h4>
    <ul class="metrics">
      <li><span>Tm</span><b>{{ grade.tm_celsius ?? '—' }} ℃</b></li>
      <li><span>断裂伸长</span><b>{{ grade.elongation_at_break_pct ?? '—' }}%</b></li>
      <li><span>拉伸强度</span><b>{{ grade.tensile_strength_mpa ?? '—' }} MPa</b></li>
      <li><span>生物相容</span><b>{{ grade.biocompatibility_class ?? '—' }}</b></li>
    </ul>
  </RouterLink>
</template>

<style scoped>
.grade-card {
  display: block;
  background: var(--pha-card-bg);
  border: 1px solid var(--pha-border);
  border-radius: var(--pha-radius);
  padding: 16px;
  text-decoration: none;
  color: var(--pha-text);
  transition: border-color 0.15s, box-shadow 0.15s;
}
.grade-card:hover {
  border-color: var(--pha-primary);
  box-shadow: 0 4px 16px rgba(31, 158, 110, 0.08);
}
.head {
  display: flex;
  align-items: baseline;
  gap: 10px;
}
.code {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  background: var(--pha-primary-soft);
  color: var(--pha-primary);
  padding: 2px 8px;
  border-radius: 6px;
  font-weight: 700;
}
.family {
  margin-left: auto;
  font-size: 12px;
  color: var(--pha-muted);
}
h4 {
  margin: 8px 0;
  font-size: 14px;
  font-weight: 500;
  color: var(--pha-muted);
}
.metrics {
  list-style: none;
  padding: 0;
  margin: 8px 0 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 6px 12px;
}
.metrics li {
  font-size: 12px;
  display: flex;
  justify-content: space-between;
}
.metrics span {
  color: var(--pha-muted);
}
.metrics b {
  font-weight: 600;
}
</style>
