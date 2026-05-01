<script setup lang="ts">
import type { Tag } from '@/types/models'

defineProps<{ tag: Tag }>()
</script>

<template>
  <span class="chip" :style="{ backgroundColor: (tag.color ?? '#6b7280') + '1a', color: tag.color ?? '#6b7280' }">
    {{ tag.name_zh }}
  </span>
</template>

<style scoped>
.chip {
  display: inline-block;
  padding: 2px 8px;
  border-radius: 6px;
  font-size: 12px;
  line-height: 1.5;
  font-weight: 500;
}
</style>
