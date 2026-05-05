<script setup lang="ts">
import { ref } from 'vue'
import { ElMessage } from 'element-plus'
import { importCSV } from '@/api/patents'

const file = ref<File | null>(null)
const result = ref<{
  received_rows: number
  inserted: number
  updated: number
  skipped: number
  errors: { line: number; error: string }[]
} | null>(null)
const uploading = ref(false)

const onFileChange = (raw: { raw: File } | undefined) => {
  file.value = raw?.raw ?? null
  result.value = null
}

const submit = async () => {
  if (!file.value) {
    ElMessage.warning('请先选择 CSV 文件')
    return
  }
  uploading.value = true
  try {
    result.value = await importCSV(file.value)
    if (result.value.errors.length === 0) {
      ElMessage.success(
        `导入完成：新增 ${result.value.inserted} 条 / 更新 ${result.value.updated} 条`,
      )
    } else {
      ElMessage.warning(`导入完成但有 ${result.value.errors.length} 行失败，详见下方`)
    }
  } finally {
    uploading.value = false
  }
}
</script>

<template>
  <div class="import">
    <RouterLink to="/patents" class="back">← 返回专利列表</RouterLink>
    <h1>专利 CSV 批量导入</h1>

    <section class="card">
      <h3>CSV 字段说明</h3>
      <p>表头必须包含以下列（其余列将忽略）：</p>
      <ul class="cols">
        <li><b>internal_code</b><span class="muted"> 必填，唯一</span></li>
        <li><b>title_zh</b><span class="muted"> 必填</span></li>
        <li>publication_no, application_no, country_code（默认 CN）</li>
        <li>patent_type（默认 invention）, legal_status（默认 disclosure）</li>
        <li>application_date / publication_date / grant_date（YYYY-MM-DD）</li>
        <li>applicant_names / inventor_names / ipc_codes / scenario_codes / grade_codes / tags（| 分隔）</li>
        <li>abstract_zh, tech_field, agency_name, internal_owner</li>
      </ul>
      <p class="example">
        示例：<code>internal_code,title_zh,publication_no,country_code,legal_status,application_date,applicant_names,inventor_names,ipc_codes,scenario_codes,grade_codes</code>
      </p>
    </section>

    <section class="card">
      <h3>上传文件</h3>
      <el-upload
        :auto-upload="false"
        :on-change="onFileChange"
        :show-file-list="true"
        accept=".csv"
        :limit="1"
      >
        <el-button>选择 CSV 文件</el-button>
      </el-upload>
      <el-button type="primary" :loading="uploading" :disabled="!file" @click="submit" style="margin-top: 12px">
        开始导入
      </el-button>
    </section>

    <section v-if="result" class="card">
      <h3>导入结果</h3>
      <ul class="kv">
        <li><span>收到行数</span><b>{{ result.received_rows }}</b></li>
        <li><span>新增</span><b style="color: var(--pha-primary)">{{ result.inserted }}</b></li>
        <li><span>更新</span><b style="color: #1e88e5">{{ result.updated }}</b></li>
        <li><span>失败 / 跳过</span><b style="color: #c62828">{{ result.skipped }}</b></li>
      </ul>
      <div v-if="result.errors.length" class="errors">
        <h4>错误明细</h4>
        <ul>
          <li v-for="(e, i) in result.errors" :key="i">
            <code>第 {{ e.line }} 行</code>：{{ e.error }}
          </li>
        </ul>
      </div>
    </section>
  </div>
</template>

<style scoped>
.import { display: flex; flex-direction: column; gap: 16px; }
.back { font-size: 13px; color: var(--pha-muted); }
h1 { margin: 0; font-size: 24px; }
.card {
  background: var(--pha-card-bg);
  border: 1px solid var(--pha-border);
  border-radius: var(--pha-radius);
  padding: 18px 20px;
}
.card h3 { margin: 0 0 10px; font-size: 14px; }
.cols { padding-left: 20px; font-size: 13px; line-height: 1.8; }
.muted { color: var(--pha-muted); font-size: 12px; }
.example {
  background: #f6f8f7; padding: 10px; border-radius: 4px; font-size: 12px; overflow-x: auto;
}
.kv { list-style: none; padding: 0; margin: 0; display: grid; grid-template-columns: repeat(4, 1fr); gap: 12px; }
.kv li { display: flex; flex-direction: column; }
.kv span { color: var(--pha-muted); font-size: 12px; }
.kv b { font-size: 22px; }
.errors { margin-top: 16px; }
.errors h4 { font-size: 13px; margin: 0 0 6px; }
.errors ul { padding-left: 20px; font-size: 12px; line-height: 1.8; color: #c62828; }
</style>
