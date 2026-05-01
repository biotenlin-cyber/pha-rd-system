<script setup lang="ts">
import type { ExternalLink } from '@/types/models'

defineProps<{ links: ExternalLink[]; title?: string }>()
</script>

<template>
  <section class="placeholder-links">
    <h3>{{ title ?? '关联专利 / 项目' }}</h3>
    <div v-if="links.length === 0" class="empty">
      <p>暂无关联记录。</p>
      <p class="hint">专利与项目模块尚未接入；上线后此处将自动展示关联引用。</p>
    </div>
    <ul v-else>
      <li v-for="link in links" :key="link.id">
        <span class="type">{{ link.link_type === 'patent' ? '专利' : '项目' }}</span>
        <span class="label">{{ link.label ?? link.external_ref }}</span>
        <span class="ref">{{ link.external_ref }}</span>
      </li>
    </ul>
  </section>
</template>

<style scoped>
.placeholder-links {
  background: var(--pha-card-bg);
  border: 1px dashed var(--pha-border);
  border-radius: var(--pha-radius);
  padding: 16px 18px;
}
h3 {
  margin: 0 0 12px;
  font-size: 15px;
}
.empty p {
  margin: 0;
  color: var(--pha-muted);
  font-size: 13px;
}
.hint {
  margin-top: 4px;
  font-size: 12px;
  color: #94a3b8;
}
ul {
  margin: 0;
  padding: 0;
  list-style: none;
}
li {
  display: flex;
  gap: 12px;
  align-items: baseline;
  padding: 6px 0;
  border-bottom: 1px dashed var(--pha-border);
  font-size: 13px;
}
.type {
  background: var(--pha-primary-soft);
  color: var(--pha-primary);
  font-size: 12px;
  padding: 1px 8px;
  border-radius: 6px;
}
.ref {
  margin-left: auto;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 11px;
  color: var(--pha-muted);
}
</style>
