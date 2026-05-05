<script setup lang="ts">
import { onMounted, reactive, ref, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { listAIJobs, listDrafts, streamAIDraft } from '@/api/patents'
import type { AIDraftJob, Draft, PatentDetail } from '@/types/models'

const props = defineProps<{ patent: PatentDetail }>()
const emit = defineEmits<{ reload: [] }>()

const drafts = ref<Draft[]>([])
const jobs = ref<AIDraftJob[]>([])

const SCENARIOS = [
  { value: 'claims_from_disclosure', label: '从技术交底起草权利要求 + 说明书' },
  { value: 'dependent_claims', label: '从权 1 扩展从属权利要求' },
  { value: 'spec_from_claims', label: '从权利要求扩写说明书' },
  { value: 'oa_response', label: 'OA 答辩与权项修改' },
]

const aiForm = reactive({
  scenario: 'claims_from_disclosure',
  section: 'claims',
  extra_context: '',
})

const streaming = ref(false)
const streamText = ref('')
const streamMeta = ref<Record<string, unknown> | null>(null)
let abortCtrl: AbortController | null = null

const loadDrafts = async () => {
  drafts.value = await listDrafts(props.patent.internal_code)
  jobs.value = await listAIJobs(props.patent.internal_code)
}

onMounted(loadDrafts)
watch(() => props.patent.internal_code, loadDrafts)

const triggerAI = async () => {
  if (aiForm.scenario === 'claims_from_disclosure' && !props.patent.has_disclosure) {
    ElMessage.warning('请先填写技术交底书')
    return
  }
  streamText.value = ''
  streamMeta.value = null
  streaming.value = true
  abortCtrl?.abort()
  abortCtrl = streamAIDraft(
    props.patent.internal_code,
    {
      scenario: aiForm.scenario,
      section: aiForm.section,
      extra_context: aiForm.extra_context || undefined,
      save_as_draft: true,
    },
    (event, data) => {
      if (event === 'job_created') {
        streamMeta.value = data as Record<string, unknown>
      } else if (event === 'delta' && typeof data === 'string') {
        streamText.value += data
      } else if (event === 'done') {
        streamMeta.value = { ...(streamMeta.value || {}), ...(data as Record<string, unknown>) }
        streaming.value = false
        ElMessage.success('AI 起草完成')
        loadDrafts()
        emit('reload')
      } else if (event === 'error') {
        streaming.value = false
        const msg = (data as { message?: string }).message || '起草失败'
        ElMessage.error(msg)
      }
    },
  )
}

const cancelStream = () => {
  abortCtrl?.abort()
  streaming.value = false
  ElMessage.info('已取消起草')
}

const previewDraft = async (d: Draft) => {
  await ElMessageBox.alert(d.content, `${d.section} v${d.version}`, {
    confirmButtonText: '关闭',
    customClass: 'draft-preview',
    dangerouslyUseHTMLString: false,
  })
}
</script>

<template>
  <div class="drafts">
    <section class="ai-panel">
      <h3>AI 辅助起草</h3>
      <p class="hint">
        模型：默认 <code>claude-sonnet-4-6</code>（OA 场景自动升级到 <code>claude-opus-4-7</code>）。
        起草内容仅作初稿参考，必须经人工专代师复核后再递交。后端需配置 <code>ANTHROPIC_API_KEY</code>。
      </p>
      <el-form :model="aiForm" label-position="top">
        <el-form-item label="起草场景">
          <el-radio-group v-model="aiForm.scenario">
            <el-radio v-for="s in SCENARIOS" :key="s.value" :label="s.value">
              {{ s.label }}
            </el-radio>
          </el-radio-group>
        </el-form-item>
        <el-form-item label="保存为申请文件版本（section）">
          <el-select v-model="aiForm.section" style="width: 220px">
            <el-option value="claims" label="权利要求 (claims)" />
            <el-option value="description" label="说明书 (description)" />
            <el-option value="abstract" label="摘要 (abstract)" />
            <el-option value="background" label="背景技术 (background)" />
            <el-option value="embodiments" label="具体实施方式 (embodiments)" />
          </el-select>
        </el-form-item>
        <el-form-item label="补充上下文（OA 通知、权 1 等）">
          <el-input
            v-model="aiForm.extra_context"
            type="textarea"
            :rows="4"
            placeholder="可选：粘贴 OA 通知书全文 / 已有权利要求 1 等"
          />
        </el-form-item>
        <el-form-item>
          <el-button v-if="!streaming" type="primary" @click="triggerAI">触发 AI 起草</el-button>
          <el-button v-else type="danger" @click="cancelStream">取消起草</el-button>
        </el-form-item>
      </el-form>

      <div v-if="streamText || streamMeta" class="stream-output">
        <h4>实时输出</h4>
        <pre>{{ streamText }}</pre>
        <div v-if="streamMeta" class="muted">{{ JSON.stringify(streamMeta) }}</div>
      </div>
    </section>

    <section class="drafts-panel">
      <h3>申请文件版本（{{ drafts.length }}）</h3>
      <el-table v-if="drafts.length" :data="drafts" stripe>
        <el-table-column label="section" width="160">
          <template #default="{ row }"><code>{{ row.section }}</code></template>
        </el-table-column>
        <el-table-column label="版本" width="80">
          <template #default="{ row }">v{{ row.version }}</template>
        </el-table-column>
        <el-table-column label="来源" width="100">
          <template #default="{ row }">
            <el-tag size="small" v-if="row.ai_generated" type="warning">AI</el-tag>
            <el-tag size="small" v-else type="success">人工</el-tag>
          </template>
        </el-table-column>
        <el-table-column label="模型" width="180">
          <template #default="{ row }">{{ row.ai_model ?? '—' }}</template>
        </el-table-column>
        <el-table-column label="预览" min-width="300">
          <template #default="{ row }">
            <span class="muted">{{ row.content.slice(0, 80) }}…</span>
          </template>
        </el-table-column>
        <el-table-column label="审核">
          <template #default="{ row }">
            <span v-if="row.review_decision">{{ row.review_decision }}</span>
            <span v-else class="muted">—</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="100">
          <template #default="{ row }">
            <el-button size="small" link @click="previewDraft(row)">查看</el-button>
          </template>
        </el-table-column>
      </el-table>
      <el-empty v-else description="暂无申请文件版本" />
    </section>

    <section v-if="jobs.length" class="jobs-panel">
      <h3>AI 起草历史</h3>
      <el-table :data="jobs" size="small">
        <el-table-column label="场景" prop="scenario" />
        <el-table-column label="状态" prop="status" width="100" />
        <el-table-column label="模型" prop="model" width="200" />
        <el-table-column label="输入 tok" prop="input_tokens" width="100" />
        <el-table-column label="输出 tok" prop="output_tokens" width="100" />
        <el-table-column label="缓存命中 tok" prop="cache_read_tokens" width="120" />
        <el-table-column label="开始时间" prop="started_at" width="180" />
      </el-table>
    </section>
  </div>
</template>

<style scoped>
.drafts {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.ai-panel,
.drafts-panel,
.jobs-panel {
  background: var(--pha-card-bg);
  border: 1px solid var(--pha-border);
  border-radius: var(--pha-radius);
  padding: 18px 20px;
}
h3 {
  margin: 0 0 12px;
  font-size: 15px;
}
h4 {
  margin: 8px 0 4px;
  font-size: 13px;
}
.hint {
  background: #f0fdf4;
  border-left: 3px solid var(--pha-primary);
  padding: 10px 14px;
  border-radius: 4px;
  margin: 0 0 14px;
  font-size: 13px;
  color: #14532d;
}
.stream-output {
  margin-top: 12px;
  padding: 12px;
  background: #0f172a;
  color: #e2e8f0;
  border-radius: 6px;
  max-height: 320px;
  overflow: auto;
}
.stream-output pre {
  margin: 0;
  white-space: pre-wrap;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size: 12px;
  line-height: 1.6;
}
.stream-output .muted {
  color: #94a3b8;
  font-size: 11px;
}
.muted {
  color: var(--pha-muted);
}
</style>
