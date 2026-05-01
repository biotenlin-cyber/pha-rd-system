<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { search } from '@/api/search'
import FilterSidebar from '@/components/FilterSidebar.vue'
import SearchBar from '@/components/SearchBar.vue'
import type { SearchResponse } from '@/types/models'

const route = useRoute()
const router = useRouter()
const result = ref<SearchResponse | null>(null)
const loading = ref(false)

const q = computed(() => (route.query.q as string) || '')
const selectedDomain = ref<string | undefined>(
  (route.query.domain as string) || undefined,
)
const selectedTags = ref<string[]>(
  Array.isArray(route.query.tags) ? (route.query.tags as string[]) : route.query.tags ? [route.query.tags as string] : [],
)
const selectedType = ref<string | undefined>(
  (route.query.type as string) || undefined,
)

const run = async () => {
  if (!q.value) {
    result.value = null
    return
  }
  loading.value = true
  try {
    result.value = await search({
      q: q.value,
      domain: selectedDomain.value,
      tags: selectedTags.value.length ? selectedTags.value : undefined,
      types: selectedType.value ? [selectedType.value] : undefined,
    })
  } finally {
    loading.value = false
  }
}

const onSearch = (next: string) => {
  router.push({ name: 'search', query: { q: next } })
}

const syncQuery = () => {
  router.replace({
    name: 'search',
    query: {
      q: q.value,
      domain: selectedDomain.value,
      tags: selectedTags.value.length ? selectedTags.value : undefined,
      type: selectedType.value,
    },
  })
}

watch([selectedDomain, selectedTags, selectedType], () => {
  syncQuery()
  run()
})
watch(() => route.query.q, run)

onMounted(run)

const linkOf = (h: { type: string; code: string }) =>
  h.type === 'scenario' ? `/scenarios/${h.code}` : `/grades/${h.code}`
</script>

<template>
  <div class="search-page">
    <div class="search-bar-row">
      <SearchBar :initial="q" @search="onSearch" />
    </div>
    <div v-if="!q" class="empty">
      <el-empty description="请输入关键词进行检索" />
    </div>
    <div v-else class="layout">
      <FilterSidebar
        :domains="result?.facets.domain"
        :tags="result?.facets.tag"
        :types="result?.facets.type"
        :selected-domain="selectedDomain"
        :selected-tags="selectedTags"
        :selected-type="selectedType"
        @update:selectedDomain="selectedDomain = $event"
        @update:selectedTags="selectedTags = $event"
        @update:selectedType="selectedType = $event"
      />
      <div class="results">
        <header class="result-head">
          <h1>"{{ q }}" 的检索结果</h1>
          <p v-if="result" class="muted">
            共 {{ result.meta.total }} 条 · 用时 {{ result.meta.took_ms }} ms
          </p>
        </header>
        <el-empty v-if="result && result.data.length === 0" description="无匹配结果" />
        <ul v-else class="hits">
          <li v-for="hit in result?.data" :key="`${hit.type}-${hit.id}`">
            <RouterLink :to="linkOf(hit)" class="hit">
              <span class="badge" :class="hit.type">
                {{ hit.type === 'scenario' ? '场景' : '牌号' }}
              </span>
              <div class="text">
                <h3>{{ hit.name_zh }}</h3>
                <p>{{ hit.snippet }}</p>
                <div class="meta">
                  <code>{{ hit.code }}</code>
                  <span v-if="hit.domain_code">领域：{{ hit.domain_code }}</span>
                  <span class="score">相关性 {{ hit.score.toFixed(2) }}</span>
                </div>
              </div>
            </RouterLink>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<style scoped>
.search-page {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.search-bar-row {
  max-width: 600px;
}
.layout {
  display: grid;
  grid-template-columns: 240px 1fr;
  gap: 16px;
}
@media (max-width: 720px) {
  .layout { grid-template-columns: 1fr; }
}
.result-head h1 {
  margin: 0;
  font-size: 20px;
}
.muted {
  color: var(--pha-muted);
  margin: 4px 0 0;
  font-size: 13px;
}
.hits {
  list-style: none;
  padding: 0;
  margin: 14px 0 0;
}
.hit {
  display: flex;
  gap: 14px;
  background: var(--pha-card-bg);
  border: 1px solid var(--pha-border);
  border-radius: var(--pha-radius);
  padding: 14px 16px;
  text-decoration: none;
  color: var(--pha-text);
  margin-bottom: 10px;
}
.hit:hover {
  border-color: var(--pha-primary);
  box-shadow: 0 2px 12px rgba(31, 158, 110, 0.06);
}
.badge {
  font-size: 12px;
  padding: 2px 10px;
  border-radius: 12px;
  height: fit-content;
}
.badge.scenario {
  background: var(--pha-primary-soft);
  color: var(--pha-primary);
}
.badge.grade {
  background: #eef2ff;
  color: #4338ca;
}
.text {
  flex: 1;
}
.text h3 {
  margin: 0 0 4px;
  font-size: 15px;
}
.text p {
  margin: 0;
  color: var(--pha-muted);
  font-size: 13px;
  line-height: 1.6;
}
.meta {
  display: flex;
  gap: 12px;
  margin-top: 6px;
  font-size: 12px;
  color: var(--pha-muted);
}
.meta code {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  background: #f6f8f7;
  padding: 1px 6px;
  border-radius: 4px;
}
.meta .score {
  margin-left: auto;
}
</style>
