<script setup lang="ts">
import { onMounted, reactive, ref, watch } from 'vue'
import { ElMessage } from 'element-plus'
import { fetchDisclosure, upsertDisclosure } from '@/api/patents'
import type { Disclosure, PatentDetail } from '@/types/models'

const props = defineProps<{ patent: PatentDetail }>()
const emit = defineEmits<{ reload: [] }>()

const initial: Disclosure = {
  id: 0,
  patent_id: props.patent.id,
  submitted_by: null,
  problem_statement: null,
  existing_solutions: null,
  proposed_solution: null,
  key_points: [],
  advantages: null,
  embodiments: [],
  attachments: [],
  confidentiality_level: 'internal',
  status: 'submitted',
}
const form = reactive<Disclosure>({ ...initial })
const loading = ref(false)
const saving = ref(false)

const load = async () => {
  loading.value = true
  try {
    const cur = await fetchDisclosure(props.patent.internal_code)
    if (cur) Object.assign(form, cur)
    else Object.assign(form, { ...initial, patent_id: props.patent.id })
  } finally {
    loading.value = false
  }
}

onMounted(load)
watch(() => props.patent.internal_code, load)

const save = async () => {
  saving.value = true
  try {
    await upsertDisclosure(props.patent.internal_code, {
      submitted_by: form.submitted_by,
      problem_statement: form.problem_statement,
      existing_solutions: form.existing_solutions,
      proposed_solution: form.proposed_solution,
      key_points: form.key_points,
      advantages: form.advantages,
      embodiments: form.embodiments,
      attachments: form.attachments,
      confidentiality_level: form.confidentiality_level,
      status: form.status,
    })
    ElMessage.success('技术交底书已保存')
    emit('reload')
  } finally {
    saving.value = false
  }
}
</script>

<template>
  <div class="disclosure" v-loading="loading">
    <p class="hint">
      技术交底书是 AI 起草权利要求 / 说明书的输入源。建议字段填写完整后再触发 AI 起草。
    </p>

    <el-form :model="form" label-width="120px" label-position="top">
      <el-form-item label="提交人">
        <el-input v-model="form.submitted_by" placeholder="提交人 / 发明人姓名" />
      </el-form-item>

      <el-form-item label="技术问题（要解决什么）">
        <el-input
          v-model="form.problem_statement"
          type="textarea"
          :rows="3"
          placeholder="本技术方案要解决的技术问题"
        />
      </el-form-item>

      <el-form-item label="现有技术（已有方案）">
        <el-input
          v-model="form.existing_solutions"
          type="textarea"
          :rows="4"
          placeholder="对比文件 / 现有产品 / 已有方案"
        />
      </el-form-item>

      <el-form-item label="技术方案（核心思路）">
        <el-input
          v-model="form.proposed_solution"
          type="textarea"
          :rows="6"
          placeholder="本方案的关键技术特征、参数范围、实施路径"
        />
      </el-form-item>

      <el-form-item label="发明点（关键点列表）">
        <el-input
          :model-value="(form.key_points as string[]).join('\n')"
          @update:model-value="(v: string) => form.key_points = v.split(/\r?\n/).filter(Boolean)"
          type="textarea"
          :rows="4"
          placeholder="每行一条发明点（关键技术特征）"
        />
      </el-form-item>

      <el-form-item label="有益效果">
        <el-input
          v-model="form.advantages"
          type="textarea"
          :rows="3"
          placeholder="性能提升幅度、对比优势、定量数据"
        />
      </el-form-item>

      <el-form-item label="实施例（可填多条 JSON）">
        <el-input
          :model-value="JSON.stringify(form.embodiments, null, 2)"
          @update:model-value="(v: string) => { try { form.embodiments = JSON.parse(v) } catch {} }"
          type="textarea"
          :rows="6"
          placeholder='[{"id":1,"title":"实施例 1","content":"按权利要求 1 配比制备…"}]'
        />
      </el-form-item>

      <el-form-item label="保密等级">
        <el-select v-model="form.confidentiality_level" style="width: 200px">
          <el-option value="public" label="公开" />
          <el-option value="internal" label="内部" />
          <el-option value="secret" label="保密" />
          <el-option value="top_secret" label="绝密" />
        </el-select>
      </el-form-item>

      <el-form-item label="审核状态">
        <el-select v-model="form.status" style="width: 200px">
          <el-option value="submitted" label="已提交" />
          <el-option value="reviewing" label="评审中" />
          <el-option value="approved" label="已通过" />
          <el-option value="rejected" label="已驳回" />
        </el-select>
      </el-form-item>

      <el-form-item>
        <el-button type="primary" :loading="saving" @click="save">保存交底书</el-button>
      </el-form-item>
    </el-form>
  </div>
</template>

<style scoped>
.disclosure {
  background: var(--pha-card-bg);
  border: 1px solid var(--pha-border);
  border-radius: var(--pha-radius);
  padding: 20px;
}
.hint {
  background: #fff8e1;
  border-left: 3px solid #f59e0b;
  padding: 10px 14px;
  border-radius: 4px;
  margin: 0 0 16px;
  font-size: 13px;
  color: #854d0e;
}
</style>
