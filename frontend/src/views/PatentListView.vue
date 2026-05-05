<script setup lang="ts">
import { onMounted, reactive, ref, watch } from 'vue'
import { useRouter } from 'vue-router'
import { listPatents, type ListPatentParams } from '@/api/patents'
import PatentStatusTag from '@/components/PatentStatusTag.vue'
import type { PatentSummary } from '@/types/models'

const router = useRouter()
const filters = reactive<ListPatentParams>({ page: 1, page_size: 20 })
const data = ref<PatentSummary[]>([])
const total = ref(0)
const loading = ref(false)

const STATUS_OPTIONS = [
  { value: '', label: '全部' },
  { value: 'disclosure', label: '交底' },
  { value: 'drafting', label: '起草中' },
  { value: 'filed', label: '已申请' },
  { value: 'substantive_pending', label: '实审中' },
  { value: 'oa_pending', label: '待答复 OA' },
  { value: 'granted', label: '已授权' },
  { value: 'rejected_final', label: '驳回' },
]

const COUNTRY_OPTIONS = [
  { value: '', label: '全部' },
  { value: 'CN', label: '中国' },
  { value: 'US', label: '美国' },
  { value: 'EP', label: '欧专局' },
  { value: 'WO', label: 'PCT' },
  { value: 'JP', label: '日本' },
]

const load = async () => {
  loading.value = true
  try {
    const res = await listPatents({
      ...filters,
      legal_status: filters.legal_status || undefined,
      country: filters.country || undefined,
      q: filters.q || undefined,
    })
    data.value = res.data
    total.value = res.meta.total
  } finally {
    loading.value = false
  }
}

watch(
  () => [filters.legal_status, filters.country],
  () => {
    filters.page = 1
    load()
  },
)

const onSearch = () => {
  filters.page = 1
  load()
}

const onPageChange = (p: number) => {
  filters.page = p
  load()
}

const open = (row: PatentSummary) => {
  router.push({ name: 'patent-detail-overview', params: { code: row.internal_code } })
}

onMounted(load)
</script>

<template>
  <div class="patent-list">
    <header class="head">
      <h1>发明专利</h1>
      <div class="actions">
        <RouterLink to="/patents/import">
          <el-button>CSV 导入</el-button>
        </RouterLink>
        <RouterLink to="/patents/analytics">
          <el-button type="primary">研究分析</el-button>
        </RouterLink>
      </div>
    </header>

    <div class="toolbar">
      <el-input
        v-model="filters.q"
        placeholder="搜索 标题 / 公开号 / 内部编号"
        clearable
        style="max-width: 320px"
        @keydown.enter="onSearch"
      >
        <template #append>
          <el-button @click="onSearch">搜索</el-button>
        </template>
      </el-input>
      <el-select v-model="filters.legal_status" placeholder="法律状态" style="width: 160px">
        <el-option v-for="o in STATUS_OPTIONS" :key="o.value" :value="o.value" :label="o.label" />
      </el-select>
      <el-select v-model="filters.country" placeholder="国家/地区" style="width: 140px">
        <el-option v-for="o in COUNTRY_OPTIONS" :key="o.value" :value="o.value" :label="o.label" />
      </el-select>
    </div>

    <el-table :data="data" v-loading="loading" stripe @row-click="open" class="table">
      <el-table-column label="内部编号" width="140">
        <template #default="{ row }">
          <code>{{ row.internal_code }}</code>
        </template>
      </el-table-column>
      <el-table-column label="标题" min-width="280">
        <template #default="{ row }">
          <a class="title-link" @click.stop="open(row)">{{ row.title_zh }}</a>
          <div class="meta-line">
            <span v-if="row.publication_no">公开号 {{ row.publication_no }}</span>
            <span v-if="row.primary_ipc">主分类 {{ row.primary_ipc }}</span>
          </div>
        </template>
      </el-table-column>
      <el-table-column label="申请人" min-width="180">
        <template #default="{ row }">
          <div>{{ row.primary_applicant ?? '—' }}</div>
          <div class="muted" v-if="row.first_inventor">第一发明人：{{ row.first_inventor }}</div>
        </template>
      </el-table-column>
      <el-table-column label="国家" width="80">
        <template #default="{ row }">{{ row.country_code }}</template>
      </el-table-column>
      <el-table-column label="状态" width="120">
        <template #default="{ row }">
          <PatentStatusTag :status="row.legal_status" />
        </template>
      </el-table-column>
      <el-table-column label="申请日" width="120">
        <template #default="{ row }">{{ row.application_date ?? '—' }}</template>
      </el-table-column>
    </el-table>

    <el-pagination
      class="pagination"
      :current-page="filters.page"
      :page-size="filters.page_size"
      :total="total"
      layout="prev, pager, next, total"
      @current-change="onPageChange"
    />
  </div>
</template>

<style scoped>
.patent-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.head {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
}
.head h1 {
  margin: 0;
  font-size: 26px;
}
.actions {
  display: flex;
  gap: 8px;
}
.toolbar {
  display: flex;
  gap: 12px;
  align-items: center;
}
.title-link {
  color: var(--pha-text);
  font-weight: 500;
  cursor: pointer;
}
.title-link:hover {
  color: var(--pha-primary);
  text-decoration: underline;
}
.meta-line {
  font-size: 12px;
  color: var(--pha-muted);
  margin-top: 2px;
  display: flex;
  gap: 12px;
}
.muted {
  color: var(--pha-muted);
  font-size: 12px;
}
.pagination {
  align-self: flex-end;
}
.table {
  cursor: pointer;
}
</style>
