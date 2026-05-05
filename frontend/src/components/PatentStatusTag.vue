<script setup lang="ts">
defineProps<{ status: string }>()

const STATUS_LABEL: Record<string, string> = {
  disclosure: '交底',
  drafting: '起草中',
  filed: '已申请',
  pre_examination_pending: '初审中',
  pre_examination_passed: '初审通过',
  published_no_substantive_request: '已公开',
  substantive_pending: '实审中',
  oa_pending: '待答复 OA',
  oa_responded: '已答复 OA',
  pre_grant_notice: '授权通知',
  granted: '已授权',
  annual_fee_due: '年费到期',
  lapsed_unpaid: '未缴年费',
  terminated_no_fee: '终止',
  reexamination: '复审',
  invalidation: '无效宣告',
  rejected_final: '驳回',
  withdrawn: '撤回',
  abandoned: '放弃',
  expired: '失效',
}

const STATUS_COLOR: Record<string, string> = {
  disclosure: '#9ca3af',
  drafting: '#fb8c00',
  filed: '#1e88e5',
  pre_examination_pending: '#1e88e5',
  pre_examination_passed: '#3949ab',
  published_no_substantive_request: '#3949ab',
  substantive_pending: '#7b1fa2',
  oa_pending: '#c62828',
  oa_responded: '#6a1b9a',
  pre_grant_notice: '#43a047',
  granted: '#1f9e6e',
  annual_fee_due: '#f57c00',
  lapsed_unpaid: '#c62828',
  terminated_no_fee: '#9e9e9e',
  reexamination: '#7b1fa2',
  invalidation: '#c62828',
  rejected_final: '#9e9e9e',
  withdrawn: '#9e9e9e',
  abandoned: '#9e9e9e',
  expired: '#9e9e9e',
}

const labelOf = (s: string) => STATUS_LABEL[s] ?? s
const colorOf = (s: string) => STATUS_COLOR[s] ?? '#9ca3af'
</script>

<template>
  <span
    class="status-tag"
    :style="{
      backgroundColor: colorOf(status) + '20',
      color: colorOf(status),
      borderColor: colorOf(status) + '40',
    }"
  >
    {{ labelOf(status) }}
  </span>
</template>

<style scoped>
.status-tag {
  display: inline-block;
  padding: 1px 8px;
  border: 1px solid;
  border-radius: 6px;
  font-size: 12px;
  line-height: 1.6;
  font-weight: 500;
}
</style>
