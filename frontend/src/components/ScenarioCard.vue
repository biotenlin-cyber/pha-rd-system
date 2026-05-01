<script setup lang="ts">
import type { ScenarioSummary } from '@/types/models'
import TagChip from './TagChip.vue'

defineProps<{ scenario: ScenarioSummary }>()
</script>

<template>
  <RouterLink :to="`/scenarios/${scenario.code}`" class="scenario-card">
    <div class="head">
      <h4>{{ scenario.name_zh }}</h4>
      <span v-if="scenario.top_match_grade" class="top-grade">
        最佳：{{ scenario.top_match_grade }}
      </span>
    </div>
    <p class="summary">{{ scenario.summary }}</p>
    <div class="tags">
      <TagChip v-for="t in scenario.tags" :key="t.id" :tag="t" />
    </div>
  </RouterLink>
</template>

<style scoped>
.scenario-card {
  display: block;
  background: var(--pha-card-bg);
  border: 1px solid var(--pha-border);
  border-radius: var(--pha-radius);
  padding: 16px 18px;
  text-decoration: none;
  color: var(--pha-text);
  transition: border-color 0.15s, box-shadow 0.15s;
}
.scenario-card:hover {
  border-color: var(--pha-primary);
  box-shadow: 0 4px 16px rgba(31, 158, 110, 0.08);
}
.head {
  display: flex;
  align-items: baseline;
  gap: 12px;
}
.head h4 {
  margin: 0;
  font-size: 16px;
}
.top-grade {
  margin-left: auto;
  font-size: 12px;
  color: var(--pha-primary);
  background: var(--pha-primary-soft);
  border-radius: 6px;
  padding: 2px 8px;
}
.summary {
  color: var(--pha-muted);
  font-size: 13px;
  line-height: 1.6;
  margin: 8px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
</style>
