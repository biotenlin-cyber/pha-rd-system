<script setup lang="ts">
import type { PatentDetail } from '@/types/models'

defineProps<{ patent: PatentDetail }>()
</script>

<template>
  <div class="overview">
    <section class="card">
      <h3>摘要</h3>
      <p>{{ patent.abstract_zh ?? '—' }}</p>
    </section>

    <div class="grid">
      <section class="card">
        <h3>申请人 ({{ patent.applicants.length }})</h3>
        <ul class="people">
          <li v-for="a in patent.applicants" :key="a.applicant_id">
            <span class="role-chip" :class="a.role">{{ a.role }}</span>
            <b>{{ a.name_zh }}</b>
            <span class="muted" v-if="a.country_code">{{ a.country_code }}</span>
          </li>
        </ul>
      </section>
      <section class="card">
        <h3>发明人 ({{ patent.inventors.length }})</h3>
        <ul class="people">
          <li v-for="i in patent.inventors" :key="i.inventor_id">
            <span class="seq">#{{ i.seq }}</span>
            <b>{{ i.name_zh }}</b>
            <span v-if="i.is_corresponding" class="muted">通讯</span>
          </li>
        </ul>
      </section>
    </div>

    <section class="card">
      <h3>技术分类（IPC / CPC）</h3>
      <ul class="classifs">
        <li
          v-for="c in patent.classifications"
          :key="c.id"
          :class="{ primary: c.is_primary }"
        >
          <span class="scheme">{{ c.scheme }}</span>
          <code>{{ c.full_symbol ?? c.code }}</code>
          <span v-if="c.is_primary" class="muted">主分类</span>
          <span v-if="c.subclass" class="muted">大类 {{ c.subclass }}</span>
        </li>
      </ul>
    </section>

    <div class="grid">
      <section class="card">
        <h3>关联应用场景</h3>
        <ul class="links">
          <li v-for="s in patent.scenarios" :key="s.scenario_id">
            <RouterLink :to="`/scenarios/${s.scenario_code}`">
              <b>{{ s.scenario_name_zh }}</b>
              <span class="muted">({{ s.scenario_code }})</span>
            </RouterLink>
          </li>
          <li v-if="patent.scenarios.length === 0" class="muted">暂无关联</li>
        </ul>
      </section>
      <section class="card">
        <h3>关联牌号</h3>
        <ul class="links">
          <li v-for="g in patent.grades" :key="g.grade_id">
            <RouterLink :to="`/grades/${g.grade_code}`">
              <b>{{ g.grade_code }}</b>
              <span class="muted">{{ g.grade_name_zh }}</span>
            </RouterLink>
          </li>
          <li v-if="patent.grades.length === 0" class="muted">暂无关联</li>
        </ul>
      </section>
    </div>

    <section class="card">
      <h3>法律状态时序</h3>
      <ol class="timeline">
        <li v-for="ev in patent.legal_events" :key="ev.id">
          <span class="date">{{ ev.event_date }}</span>
          <span class="dot" />
          <span>
            <b>{{ ev.event_code }}</b>
            <span class="muted" v-if="ev.event_desc"> — {{ ev.event_desc }}</span>
          </span>
        </li>
        <li v-if="patent.legal_events.length === 0" class="muted">暂无法律事件记录</li>
      </ol>
    </section>

    <section class="card">
      <h3>合规与权属</h3>
      <ul class="kv">
        <li><span>是否职务发明</span><b>{{ patent.is_service_invention ? '是' : '否' }}</b></li>
        <li><span>申请路线</span><b>{{ patent.application_route }}</b></li>
        <li><span>代理机构</span><b>{{ patent.agency_name ?? '—' }}</b></li>
        <li><span>内部责任人</span><b>{{ patent.internal_owner ?? '—' }}</b></li>
        <li><span>下次年费到期</span><b>{{ patent.next_annual_fee_due ?? '—' }}</b></li>
        <li><span>权利要求总数</span><b>{{ patent.claim_count ?? '—' }}</b></li>
        <li><span>独立权项数</span><b>{{ patent.independent_claim_count ?? '—' }}</b></li>
      </ul>
    </section>

    <section class="card stats">
      <div class="stat">
        <span class="big">{{ patent.draft_count }}</span>
        <span class="lbl">申请文件版本</span>
      </div>
      <div class="stat">
        <span class="big">{{ patent.oa_count }}</span>
        <span class="lbl">审查意见</span>
      </div>
      <div class="stat">
        <span class="big">{{ patent.has_disclosure ? '✓' : '—' }}</span>
        <span class="lbl">技术交底书</span>
      </div>
    </section>
  </div>
</template>

<style scoped>
.overview {
  display: flex;
  flex-direction: column;
  gap: 14px;
}
.grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 14px;
}
@media (max-width: 720px) { .grid { grid-template-columns: 1fr; } }
.card {
  background: var(--pha-card-bg);
  border: 1px solid var(--pha-border);
  border-radius: var(--pha-radius);
  padding: 16px 18px;
}
.card h3 {
  font-size: 14px;
  margin: 0 0 10px;
}
.card p {
  margin: 0;
  color: var(--pha-text);
  line-height: 1.7;
  font-size: 14px;
}
.people {
  list-style: none;
  padding: 0;
  margin: 0;
}
.people li {
  display: flex;
  gap: 8px;
  align-items: baseline;
  padding: 4px 0;
  font-size: 13px;
  border-bottom: 1px dashed var(--pha-border);
}
.people li:last-child { border-bottom: 0; }
.seq {
  font-family: ui-monospace, monospace;
  color: var(--pha-muted);
  width: 28px;
}
.role-chip {
  font-size: 11px;
  padding: 1px 6px;
  border-radius: 4px;
  background: var(--pha-primary-soft);
  color: var(--pha-primary);
}
.role-chip.co {
  background: #eef2ff;
  color: #4338ca;
}
.classifs {
  list-style: none;
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.classifs li {
  display: flex;
  gap: 10px;
  align-items: baseline;
  font-size: 13px;
}
.classifs .scheme {
  background: var(--pha-primary-soft);
  color: var(--pha-primary);
  font-family: monospace;
  font-size: 11px;
  padding: 1px 6px;
  border-radius: 4px;
}
.classifs code {
  font-family: ui-monospace, monospace;
}
.classifs li.primary code { font-weight: 700; }
.muted {
  color: var(--pha-muted);
  font-size: 12px;
}
.links {
  list-style: none;
  padding: 0;
  margin: 0;
}
.links li {
  padding: 4px 0;
  font-size: 13px;
}
.timeline {
  list-style: none;
  padding: 0;
  margin: 0;
}
.timeline li {
  display: flex;
  gap: 12px;
  align-items: baseline;
  padding: 6px 0;
  font-size: 13px;
}
.timeline .date {
  font-family: monospace;
  color: var(--pha-muted);
  min-width: 96px;
}
.timeline .dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: var(--pha-primary);
  display: inline-block;
}
.kv {
  list-style: none;
  padding: 0;
  margin: 0;
}
.kv li {
  display: flex;
  justify-content: space-between;
  padding: 4px 0;
  border-bottom: 1px dashed var(--pha-border);
  font-size: 13px;
}
.kv li:last-child { border-bottom: 0; }
.kv span { color: var(--pha-muted); }
.stats {
  display: flex;
  gap: 24px;
}
.stat {
  display: flex;
  flex-direction: column;
}
.stat .big {
  font-size: 28px;
  font-weight: 700;
  color: var(--pha-primary);
}
.stat .lbl {
  color: var(--pha-muted);
  font-size: 12px;
}
</style>
