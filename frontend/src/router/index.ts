import { createRouter, createWebHistory, type RouteRecordRaw } from 'vue-router'

const routes: RouteRecordRaw[] = [
  { path: '/', name: 'home', component: () => import('@/views/HomeView.vue') },
  {
    path: '/domains/:code',
    name: 'domain-detail',
    component: () => import('@/views/DomainDetailView.vue'),
  },
  {
    path: '/scenarios/:code',
    name: 'scenario-detail',
    component: () => import('@/views/ScenarioDetailView.vue'),
  },
  {
    path: '/grades',
    name: 'grade-list',
    component: () => import('@/views/GradeListView.vue'),
  },
  {
    path: '/grades/:code',
    name: 'grade-detail',
    component: () => import('@/views/GradeDetailView.vue'),
  },
  {
    path: '/search',
    name: 'search',
    component: () => import('@/views/SearchResultsView.vue'),
  },
  {
    path: '/patents',
    name: 'patent-list',
    component: () => import('@/views/PatentListView.vue'),
  },
  {
    path: '/patents/analytics',
    name: 'patent-analytics',
    component: () => import('@/views/PatentAnalyticsView.vue'),
  },
  {
    path: '/patents/import',
    name: 'patent-import',
    component: () => import('@/views/PatentImportView.vue'),
  },
  {
    path: '/patents/:code',
    name: 'patent-detail',
    component: () => import('@/views/PatentDetailView.vue'),
    children: [
      {
        path: '',
        name: 'patent-detail-overview',
        component: () => import('@/views/patent/PatentOverview.vue'),
      },
      {
        path: 'disclosure',
        name: 'patent-detail-disclosure',
        component: () => import('@/views/patent/PatentDisclosure.vue'),
      },
      {
        path: 'drafts',
        name: 'patent-detail-drafts',
        component: () => import('@/views/patent/PatentDrafts.vue'),
      },
      {
        path: 'office-actions',
        name: 'patent-detail-oas',
        component: () => import('@/views/patent/PatentOAs.vue'),
      },
    ],
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFoundView.vue'),
  },
]

export const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    return { top: 0 }
  },
})
