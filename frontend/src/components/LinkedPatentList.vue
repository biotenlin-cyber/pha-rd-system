<script setup lang="ts">
import PatentStatusTag from './PatentStatusTag.vue'
import type { LinkedPatent } from '@/types/models'

defineProps<{ patents: LinkedPatent[]; title?: string }>()
</script>

<template>
  <section class="linked-patents">
    <h3>{{ title ?? '关联专利' }}（{{ patents.length }}）</h3>
    <ul v-if="patents.length">
      <li v-for="p in patents" :key="p.id">
        <RouterLink :to="`/patents/${p.internal_code}`" class="row">
          <span class="code">{{ p.internal_code }}</span>
          <span class="title">{{ p.title_zh }}</span>
          <span class="meta">
            <PatentStatusTag :status="p.legal_status" />
            <span class="muted" v-if="p.publication_no">{{ p.publication_no }}</span>
            <span class="muted" v-if="p.country_code">{{ p.country_code }}</span>
            <span class="muted" v-if="p.application_date">{{ p.application_date }}</span>
          </span>
        </RouterLink>
      </li>
    </ul>
    <p v-else class="muted">暂无关联专利。</p>
  </section>
</template>

<style scoped>
.linked-patents {
  background: var(--pha-card-bg);
  border: 1px solid var(--pha-border);
  border-radius: var(--pha-radius);
  padding: 16px 18px;
}
h3 { margin: 0 0 10px; font-size: 15px; }
ul { list-style: none; padding: 0; margin: 0; }
li { padding: 6px 0; border-bottom: 1px dashed var(--pha-border); }
li:last-child { border-bottom: 0; }
.row {
  display: grid;
  grid-template-columns: 130px 1fr auto;
  gap: 10px;
  align-items: center;
  text-decoration: none;
  color: var(--pha-text);
}
.code {
  font-family: ui-monospace, monospace;
  font-size: 12px;
  background: var(--pha-primary-soft);
  color: var(--pha-primary);
  padding: 1px 8px;
  border-radius: 4px;
  text-align: center;
}
.title {
  font-size: 14px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.row:hover .title { color: var(--pha-primary); }
.meta {
  display: flex;
  gap: 8px;
  align-items: center;
  font-size: 12px;
}
.muted { color: var(--pha-muted); font-size: 12px; }
</style>
