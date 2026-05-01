<script setup lang="ts">
import { onMounted, ref, watch } from 'vue'
import * as echarts from 'echarts/core'
import { RadarChart } from 'echarts/charts'
import {
  TitleComponent,
  TooltipComponent,
  LegendComponent,
} from 'echarts/components'
import { CanvasRenderer } from 'echarts/renderers'
import type { Grade } from '@/types/models'

echarts.use([RadarChart, TitleComponent, TooltipComponent, LegendComponent, CanvasRenderer])

const props = defineProps<{ grade: Grade }>()
const el = ref<HTMLElement | null>(null)
let chart: echarts.ECharts | null = null

const buildOption = (grade: Grade) => ({
  tooltip: {},
  radar: {
    indicator: [
      { name: '熔点 Tm (℃)', max: 200 },
      { name: '断裂伸长 (%)', max: 1000 },
      { name: '拉伸强度 (MPa)', max: 60 },
      { name: '结晶度 (%)', max: 80 },
      { name: '土壤降解 (月)', max: 24 },
      { name: '海水降解 (月)', max: 24 },
    ],
    radius: 90,
  },
  series: [
    {
      name: grade.code,
      type: 'radar',
      data: [
        {
          name: grade.code,
          value: [
            grade.tm_celsius ?? 0,
            grade.elongation_at_break_pct ?? 0,
            grade.tensile_strength_mpa ?? 0,
            grade.crystallinity_pct ?? 0,
            grade.degradation_months_soil ?? 0,
            grade.degradation_months_marine ?? 0,
          ],
          areaStyle: { color: 'rgba(31,158,110,0.20)' },
          lineStyle: { color: '#1f9e6e' },
          itemStyle: { color: '#1f9e6e' },
        },
      ],
    },
  ],
})

onMounted(() => {
  if (!el.value) return
  chart = echarts.init(el.value)
  chart.setOption(buildOption(props.grade))
  window.addEventListener('resize', () => chart?.resize())
})

watch(
  () => props.grade,
  (g) => chart?.setOption(buildOption(g)),
  { deep: true },
)
</script>

<template>
  <div ref="el" class="radar"></div>
</template>

<style scoped>
.radar {
  width: 100%;
  height: 320px;
}
</style>
