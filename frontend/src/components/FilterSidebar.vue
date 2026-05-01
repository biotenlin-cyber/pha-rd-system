<script setup lang="ts">
import type { SearchFacet } from '@/types/models'

defineProps<{
  domains?: SearchFacet[]
  tags?: SearchFacet[]
  types?: SearchFacet[]
  selectedDomain?: string
  selectedTags: string[]
  selectedType?: string
}>()

const emit = defineEmits<{
  (e: 'update:selectedDomain', code: string | undefined): void
  (e: 'update:selectedTags', codes: string[]): void
  (e: 'update:selectedType', code: string | undefined): void
}>()

const toggleTag = (selected: string[], code: string) => {
  if (selected.includes(code)) {
    emit('update:selectedTags', selected.filter((s) => s !== code))
  } else {
    emit('update:selectedTags', [...selected, code])
  }
}
</script>

<template>
  <aside class="filter-sidebar">
    <section v-if="types && types.length">
      <h4>类型</h4>
      <ul>
        <li v-for="t in types" :key="t.code" :class="{ active: selectedType === t.code }">
          <a href="#" @click.prevent="emit('update:selectedType', selectedType === t.code ? undefined : t.code)">
            <span>{{ t.code === 'scenario' ? '应用场景' : t.code === 'grade' ? '牌号' : t.code }}</span>
            <em>{{ t.count }}</em>
          </a>
        </li>
      </ul>
    </section>
    <section v-if="domains && domains.length">
      <h4>领域</h4>
      <ul>
        <li v-for="d in domains" :key="d.code" :class="{ active: selectedDomain === d.code }">
          <a href="#" @click.prevent="emit('update:selectedDomain', selectedDomain === d.code ? undefined : d.code)">
            <span>{{ d.code }}</span>
            <em>{{ d.count }}</em>
          </a>
        </li>
      </ul>
    </section>
    <section v-if="tags && tags.length">
      <h4>标签</h4>
      <ul>
        <li v-for="t in tags" :key="t.code" :class="{ active: selectedTags.includes(t.code) }">
          <a href="#" @click.prevent="toggleTag(selectedTags, t.code)">
            <span>{{ t.code }}</span>
            <em>{{ t.count }}</em>
          </a>
        </li>
      </ul>
    </section>
  </aside>
</template>

<style scoped>
.filter-sidebar {
  background: var(--pha-card-bg);
  border: 1px solid var(--pha-border);
  border-radius: var(--pha-radius);
  padding: 16px;
  font-size: 13px;
}
section {
  margin-bottom: 16px;
}
section:last-child {
  margin-bottom: 0;
}
h4 {
  margin: 0 0 8px;
  font-size: 13px;
  color: var(--pha-muted);
  text-transform: uppercase;
  letter-spacing: 0.04em;
}
ul {
  list-style: none;
  margin: 0;
  padding: 0;
}
li a {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 4px 8px;
  margin: 2px 0;
  border-radius: 6px;
  color: var(--pha-text);
  text-decoration: none;
}
li a:hover {
  background: var(--pha-primary-soft);
}
li.active a {
  background: var(--pha-primary-soft);
  color: var(--pha-primary);
  font-weight: 600;
}
em {
  font-style: normal;
  color: var(--pha-muted);
  font-size: 12px;
}
</style>
