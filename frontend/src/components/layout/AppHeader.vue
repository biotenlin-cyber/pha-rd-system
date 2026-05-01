<script setup lang="ts">
import { useRouter } from 'vue-router'
import SearchBar from '@/components/SearchBar.vue'

const router = useRouter()

const onSearch = (q: string) => {
  router.push({ name: 'search', query: { q } })
}
</script>

<template>
  <header class="app-header">
    <div class="inner">
      <RouterLink to="/" class="brand">
        <span class="logo">PHA</span>
        <span class="title">应用知识库</span>
      </RouterLink>
      <nav class="nav">
        <RouterLink to="/">领域</RouterLink>
        <RouterLink to="/grades">牌号</RouterLink>
      </nav>
      <SearchBar class="header-search" @search="onSearch" />
    </div>
  </header>
</template>

<style scoped>
.app-header {
  background: #fff;
  border-bottom: 1px solid var(--pha-border);
  position: sticky;
  top: 0;
  z-index: 10;
}
.inner {
  max-width: 1200px;
  margin: 0 auto;
  padding: 12px 24px;
  display: flex;
  align-items: center;
  gap: 24px;
}
.brand {
  display: flex;
  align-items: center;
  gap: 10px;
  text-decoration: none;
  color: var(--pha-text);
  font-weight: 700;
}
.logo {
  display: inline-block;
  background: var(--pha-primary);
  color: #fff;
  border-radius: 8px;
  padding: 4px 10px;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 14px;
}
.title {
  font-size: 18px;
}
.nav {
  display: flex;
  gap: 16px;
  font-size: 14px;
}
.nav a {
  color: var(--pha-muted);
}
.nav a.router-link-active {
  color: var(--pha-primary);
  font-weight: 600;
}
.header-search {
  margin-left: auto;
  width: 320px;
}
</style>
