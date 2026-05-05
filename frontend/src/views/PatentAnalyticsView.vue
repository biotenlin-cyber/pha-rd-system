<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts/core'
import { BarChart, HeatmapChart, PieChart } from 'echarts/charts'
import {
  GridComponent,
  LegendComponent,
  TitleComponent,
  TooltipComponent,
  VisualMapComponent,
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import { fetchAnalytics, fetchHeatmap } from '@/api/patents'
import type { PatentAnalytics, PatentHeatmapCell } from '@/types/models'

echarts.use([
  PieChart,
  BarChart,
  HeatmapChart,
  GridComponent,
  TooltipComponent,
  LegendComponent,
  TitleComponent,
  VisualMapComponent,
  CanvasRenderer,
])

const analytics = ref<PatentAnalytics | null>(null)
const heatmap = ref<PatentHeatmapCell[]>([])

const statusEl = ref<HTMLElement | null>(null)
const applicantEl = ref<HTMLElement | null>(null)
const subclassEl = ref<HTMLElement | null>(null)
const heatmapEl = ref<HTMLElement | null>(null)

let charts: echarts.ECharts[] = []

const STATUS_LABEL: Record<string, string> = {
  disclosure: '交底',
  drafting: '起草中',
  filed: '已申请',
  substantive_pending: '实审中',
  oa_pending: '待答复 OA',
  granted: '已授权',
  rejected_final: '驳回',
}

const renderStatus = (a: PatentAnalytics) => {
  if (!statusEl.value) return
  const c = echarts.init(statusEl.value)
  c.setOption({
    title: { text: '法律状态分布', left: 'left', textStyle: { fontSize: 14 } },
    tooltip: { trigger: 'item' },
    series: [
      {
        type: 'pie',
        radius: ['40%', '70%'],
        data: a.by_legal_status.map((d) => ({
          name: STATUS_LABEL[d.code] ?? d.code,
          value: d.count,
        })),
      },
    ],
    color: ['#1f9e6e', '#1e88e5', '#fb8c00', '#7b1fa2', '#9ca3af', '#c62828', '#43a047'],
  })
  charts.push(c)
}

const renderApplicants = (a: PatentAnalytics) => {
  if (!applicantEl.value) return
  const c = echarts.init(applicantEl.value)
  const sorted = [...a.by_top_applicant].slice(0, 10).reverse()
  c.setOption({
    title: { text: 'Top 10 申请人', left: 'left', textStyle: { fontSize: 14 } },
    grid: { left: 160, right: 30, top: 30, bottom: 30 },
    xAxis: { type: 'value' },
    yAxis: { type: 'category', data: sorted.map((d) => d.code) },
    tooltip: {},
    series: [
      {
        type: 'bar',
        data: sorted.map((d) => d.count),
        itemStyle: { color: '#1f9e6e' },
        label: { show: true, position: 'right' },
      },
    ],
  })
  charts.push(c)
}

const renderSubclass = (a: PatentAnalytics) => {
  if (!subclassEl.value) return
  const c = echarts.init(subclassEl.value)
  c.setOption({
    title: { text: 'IPC 大类分布', left: 'left', textStyle: { fontSize: 14 } },
    grid: { left: 50, right: 30, top: 30, bottom: 60 },
    xAxis: { type: 'category', data: a.by_subclass.map((d) => d.code), axisLabel: { rotate: 30 } },
    yAxis: { type: 'value' },
    tooltip: {},
    series: [
      {
        type: 'bar',
        data: a.by_subclass.map((d) => d.count),
        itemStyle: { color: '#3949ab' },
      },
    ],
  })
  charts.push(c)
}

const renderHeatmap = (cells: PatentHeatmapCell[]) => {
  if (!heatmapEl.value || cells.length === 0) return
  const domains = Array.from(new Set(cells.map((c) => c.domain)))
  const grades = Array.from(new Set(cells.map((c) => c.grade)))
  const data = cells.map((c) => [
    domains.indexOf(c.domain),
    grades.indexOf(c.grade),
    c.count,
  ])
  const c = echarts.init(heatmapEl.value)
  c.setOption({
    title: { text: '领域 × 牌号 热力矩阵', left: 'left', textStyle: { fontSize: 14 } },
    tooltip: {
      formatter: (p: { value: [number, number, number] }) =>
        `${domains[p.value[0]]} × ${grades[p.value[1]]}<br/>专利数：${p.value[2]}`,
    },
    grid: { left: 100, right: 20, top: 40, bottom: 80 },
    xAxis: { type: 'category', data: domains, axisLabel: { rotate: 30 } },
    yAxis: { type: 'category', data: grades },
    visualMap: {
      min: 0,
      max: Math.max(...cells.map((c) => c.count)),
      show: true,
      calculable: true,
      orient: 'horizontal',
      left: 'center',
      bottom: 0,
      inRange: { color: ['#e6f5ee', '#1f9e6e'] },
    },
    series: [
      {
        type: 'heatmap',
        data,
        label: { show: true },
      },
    ],
  })
  charts.push(c)
}

const renderAll = () => {
  charts.forEach((c) => c.dispose())
  charts = []
  if (analytics.value) {
    renderStatus(analytics.value)
    renderApplicants(analytics.value)
    renderSubclass(analytics.value)
  }
  renderHeatmap(heatmap.value)
}

onMounted(async () => {
  analytics.value = await fetchAnalytics()
  heatmap.value = await fetchHeatmap()
  renderAll()
  window.addEventListener('resize', () => charts.forEach((c) => c.resize()))
})

watch([analytics, heatmap], renderAll, { deep: true })
</script>

<template>
  <div class="analytics" v-loading="!analytics">
    <header class="head">
      <h1>专利研究分析</h1>
      <p class="muted" v-if="analytics">
        累计 {{ analytics.total }} 件专利 ·
        覆盖 {{ analytics.by_country.length }} 个国家/地区 ·
        {{ analytics.by_top_applicant.length }} 位申请人 ·
        {{ analytics.by_subclass.length }} 个 IPC 大类
      </p>
    </header>

    <div class="grid">
      <div class="chart" ref="statusEl" />
      <div class="chart" ref="applicantEl" />
    </div>
    <div class="chart" ref="subclassEl" />
    <div class="chart tall" ref="heatmapEl" />
  </div>
</template>

<style scoped>
.analytics {
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.head h1 {
  margin: 0;
  font-size: 24px;
}
.muted {
  color: var(--pha-muted);
  margin: 4px 0 0;
  font-size: 13px;
}
.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}
@media (max-width: 720px) { .grid { grid-template-columns: 1fr; } }
.chart {
  background: var(--pha-card-bg);
  border: 1px solid var(--pha-border);
  border-radius: var(--pha-radius);
  padding: 14px;
  height: 320px;
}
.chart.tall { height: 480px; }
</style>
