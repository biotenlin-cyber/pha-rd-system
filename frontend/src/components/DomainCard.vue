<script setup lang="ts">
import type { Domain } from '@/types/models'

defineProps<{ domain: Domain }>()
</script>

<template>
  <RouterLink :to="`/domains/${domain.code}`" class="domain-card">
    <div class="head">
      <span class="badge">{{ domain.scenario_count }}</span>
      <h3>{{ domain.name_zh }}</h3>
      <span class="en">{{ domain.name_en }}</span>
    </div>
    <p class="desc">{{ domain.description }}</p>
  </RouterLink>
</template>

<style scoped>
.domain-card {
  display: block;
  background: var(--pha-card-bg);
  border: 1px solid var(--pha-border);
  border-radius: var(--pha-radius);
  padding: 18px 20px;
  text-decoration: none;
  color: var(--pha-text);
  transition: border-color 0.15s, box-shadow 0.15s, transform 0.15s;
}
.domain-card:hover {
  border-color: var(--pha-primary);
  box-shadow: 0 4px 16px rgba(31, 158, 110, 0.08);
  transform: translateY(-2px);
}
.head {
  display: flex;
  align-items: baseline;
  gap: 8px;
}
.head h3 {
  margin: 0;
  font-size: 18px;
}
.en {
  margin-left: auto;
  color: var(--pha-muted);
  font-size: 12px;
}
.badge {
  background: var(--pha-primary-soft);
  color: var(--pha-primary);
  border-radius: 8px;
  padding: 2px 8px;
  font-size: 12px;
  font-weight: 600;
}
.desc {
  margin: 10px 0 0;
  color: var(--pha-muted);
  font-size: 13px;
  line-height: 1.6;
}
</style>
