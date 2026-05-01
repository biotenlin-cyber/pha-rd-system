import { defineStore } from 'pinia'
import { ref } from 'vue'
import type { Domain } from '@/types/models'
import { fetchDomains } from '@/api/domains'

export const useDomainStore = defineStore('domain', () => {
  const domains = ref<Domain[]>([])
  const loading = ref(false)

  const load = async (force = false) => {
    if (domains.value.length && !force) return
    loading.value = true
    try {
      domains.value = await fetchDomains()
    } finally {
      loading.value = false
    }
  }

  const findByCode = (code: string) =>
    domains.value.find((d) => d.code === code)

  return { domains, loading, load, findByCode }
})
