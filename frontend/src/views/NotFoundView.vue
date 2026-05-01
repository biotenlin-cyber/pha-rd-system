<script setup lang="ts"></script>

<template>
  <div class="not-found">
    <el-empty description="页面不存在">
      <RouterLink to="/">
        <el-button type="primary">返回首页</el-button>
      </RouterLink>
    </el-empty>
  </div>
</template>

<style scoped>
.not-found {
  padding: 60px 0;
}
</style>
