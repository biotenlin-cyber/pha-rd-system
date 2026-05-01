<script setup lang="ts">
import { computed } from 'vue'

interface MatchRow {
  match_score: number
  recommendation_level: string
  rationale: string | null
  key_metrics?: Record<string, unknown>
  // For scenario detail (matched grades):
  grade_code?: string
  grade_name_zh?: string
  // For grade detail (matched scenarios):
  scenario_code?: string
  scenario_name_zh?: string
  domain_code?: string
}

const props = defineProps<{
  matches: MatchRow[]
  // 'grade' = each row is a matched grade for a scenario
  // 'scenario' = each row is a matched scenario for a grade
  rowType: 'grade' | 'scenario'
}>()

const levelColors: Record<string, string> = {
  preferred: '#1f9e6e',
  suitable: '#3b82f6',
  marginal: '#eab308',
  not_recommended: '#9ca3af',
}

const levelText: Record<string, string> = {
  preferred: '优先推荐',
  suitable: '合适',
  marginal: '勉强可用',
  not_recommended: '不推荐',
}

const sorted = computed(() =>
  [...props.matches].sort((a, b) => b.match_score - a.match_score),
)

const linkTo = (row: MatchRow) =>
  props.rowType === 'grade'
    ? `/grades/${row.grade_code}`
    : `/scenarios/${row.scenario_code}`

const titleOf = (row: MatchRow) =>
  props.rowType === 'grade'
    ? `${row.grade_code}  ·  ${row.grade_name_zh}`
    : `${row.scenario_name_zh}  ·  ${row.scenario_code}`
</script>

<template>
  <el-table :data="sorted" stripe>
    <el-table-column :label="rowType === 'grade' ? '匹配牌号' : '匹配场景'" min-width="220">
      <template #default="{ row }">
        <RouterLink :to="linkTo(row)">{{ titleOf(row) }}</RouterLink>
        <div v-if="rowType === 'scenario' && row.domain_code" class="domain-line">
          领域：{{ row.domain_code }}
        </div>
      </template>
    </el-table-column>
    <el-table-column label="评分" width="160">
      <template #default="{ row }">
        <div class="score-cell">
          <el-progress
            :percentage="row.match_score"
            :stroke-width="6"
            :color="levelColors[row.recommendation_level] ?? '#9ca3af'"
            :show-text="false"
          />
          <span class="score">{{ row.match_score }}</span>
        </div>
      </template>
    </el-table-column>
    <el-table-column label="推荐等级" width="120">
      <template #default="{ row }">
        <el-tag
          :color="levelColors[row.recommendation_level] + '20'"
          :style="{ color: levelColors[row.recommendation_level], border: 'none' }"
        >
          {{ levelText[row.recommendation_level] ?? row.recommendation_level }}
        </el-tag>
      </template>
    </el-table-column>
    <el-table-column label="说明" min-width="280">
      <template #default="{ row }">
        <div class="rationale">{{ row.rationale }}</div>
      </template>
    </el-table-column>
  </el-table>
</template>

<style scoped>
.score-cell {
  display: flex;
  align-items: center;
  gap: 8px;
}
.score {
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-weight: 600;
  width: 28px;
  text-align: right;
}
.rationale {
  color: var(--pha-text);
  font-size: 13px;
  line-height: 1.6;
}
.domain-line {
  color: var(--pha-muted);
  font-size: 12px;
  margin-top: 2px;
}
</style>
