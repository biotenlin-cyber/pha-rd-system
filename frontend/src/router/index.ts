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
