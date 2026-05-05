<script setup lang="ts">
import { onMounted, reactive, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { createOA, listOAs } from '@/api/patents'
import type { OfficeAction, PatentDetail } from '@/types/models'

const props = defineProps<{ patent: PatentDetail }>()

const oas = ref<OfficeAction[]>([])
const dialogVisible = ref(false)
const newOA = reactive<Partial<OfficeAction>>({
  action_no: '1',
  oa_type: 'first_oa',
  status: 'received',
  issues: [],
})

const load = async () => {
  oas.value = await listOAs(props.patent.internal_code)
}

onMounted(load)
watch(() => props.patent.internal_code, load)

const submit = async () => {
  await createOA(props.patent.internal_code, newOA)
  ElMessage.success('OA 已记录')
  dialogVisible.value = false
  Object.assign(newOA, { action_no: '1', oa_type: 'first_oa', status: 'received', issues: [] })
  load()
}
</script>

<template>
  <div class="oas">
    <header class="oas-head">
      <h3>审查意见 / OA 答辩</h3>
      <el-button type="primary" @click="dialogVisible = true">+ 新增 OA 记录</el-button>
    </header>

    <el-empty v-if="oas.length === 0" description="暂无审查意见" />
    <ul v-else class="timeline">
      <li v-for="oa in oas" :key="oa.id">
        <div class="head">
          <span class="badge">第 {{ oa.action_no }} 次 · {{ oa.oa_type }}</span>
          <span class="status">{{ oa.status }}</span>
        </div>
        <ul class="kv">
          <li><span>收文日</span><b>{{ oa.received_date ?? '—' }}</b></li>
          <li><span>答复期限</span><b>{{ oa.due_date ?? '—' }}</b></li>
          <li><span>审查员</span><b>{{ oa.examiner_name ?? '—' }}</b></li>
          <li><span>实际答复</span><b>{{ oa.responded_at ?? '—' }}</b></li>
        </ul>
        <p v-if="oa.response_content" class="response">{{ oa.response_content }}</p>
      </li>
    </ul>

    <el-dialog v-model="dialogVisible" title="新增审查意见 / OA 记录" width="600">
      <el-form :model="newOA" label-position="top">
        <el-form-item label="OA 编号">
          <el-input v-model="newOA.action_no" />
        </el-form-item>
        <el-form-item label="OA 类型">
          <el-select v-model="newOA.oa_type" style="width: 100%">
            <el-option value="notice_to_make_correction" label="补正通知" />
            <el-option value="first_oa" label="第一次 OA" />
            <el-option value="second_oa" label="第二次 OA" />
            <el-option value="nth_oa" label="第 N 次 OA" />
            <el-option value="pre_grant_notice" label="授权前通知" />
            <el-option value="reexamination" label="复审通知" />
            <el-option value="invalidation" label="无效宣告" />
          </el-select>
        </el-form-item>
        <el-form-item label="收文日 / 答复期限">
          <div style="display: flex; gap: 12px">
            <el-date-picker v-model="newOA.received_date" type="date" value-format="YYYY-MM-DD" placeholder="收文日" />
            <el-date-picker v-model="newOA.due_date" type="date" value-format="YYYY-MM-DD" placeholder="答复期限" />
          </div>
        </el-form-item>
        <el-form-item label="审查员姓名">
          <el-input v-model="newOA.examiner_name" />
        </el-form-item>
        <el-form-item label="答辩内容（草稿）">
          <el-input v-model="newOA.response_content" type="textarea" :rows="6" />
        </el-form-item>
        <el-form-item label="状态">
          <el-select v-model="newOA.status" style="width: 200px">
            <el-option value="received" label="已收文" />
            <el-option value="responding" label="答辩中" />
            <el-option value="responded" label="已答复" />
            <el-option value="closed" label="已结案" />
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <el-button @click="dialogVisible = false">取消</el-button>
        <el-button type="primary" @click="submit">提交</el-button>
      </template>
    </el-dialog>
  </div>
</template>

<style scoped>
.oas { display: flex; flex-direction: column; gap: 12px; }
.oas-head { display: flex; justify-content: space-between; align-items: center; }
h3 { margin: 0; font-size: 15px; }
.timeline { list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 12px; }
.timeline > li {
  background: var(--pha-card-bg);
  border: 1px solid var(--pha-border);
  border-radius: var(--pha-radius);
  padding: 14px 16px;
}
.head { display: flex; justify-content: space-between; margin-bottom: 8px; }
.badge { background: var(--pha-primary-soft); color: var(--pha-primary); padding: 2px 8px; border-radius: 6px; font-size: 12px; font-weight: 600; }
.status { color: var(--pha-muted); font-size: 12px; }
.kv { list-style: none; padding: 0; margin: 0 0 8px; display: grid; grid-template-columns: 1fr 1fr; gap: 4px 14px; font-size: 13px; }
.kv li { display: flex; justify-content: space-between; }
.kv span { color: var(--pha-muted); }
.response { margin: 0; font-size: 13px; color: var(--pha-text); line-height: 1.7; background: #f6f8f7; padding: 10px; border-radius: 4px; }
</style>
