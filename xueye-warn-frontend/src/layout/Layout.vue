<template>
  <el-container class="layout-container">
    <el-aside width="220px" class="layout-aside">
      <el-menu
          default-active="1"
          class="el-menu-vertical-demo"
      >
        <el-menu-item index="1">
          <router-link to="/dashboard">
            <el-icon><DataAnalysis /></el-icon>
            <span>学业信息图</span>
          </router-link>
        </el-menu-item>
        <el-menu-item index="2">
          <router-link to="/student">
            <el-icon><User /></el-icon>
            <span>学生信息</span>
          </router-link>
        </el-menu-item>
        <el-menu-item index="3">
          <router-link to="/hadoop">
            <el-icon><UploadFilled /></el-icon>
            <span>Hadoop文件管理</span>
          </router-link>
        </el-menu-item>
        <el-menu-item index="4">
          <router-link to="/user">
            <el-icon><UserFilled /></el-icon>
            <span>用户管理</span>
          </router-link>
        </el-menu-item>
        <el-menu-item index="5">
          <router-link to="/loginLog">
            <el-icon><Document /></el-icon>
            <span>日志管理</span>
          </router-link>
        </el-menu-item>
        <el-menu-item index="6">
          <router-link to="/systemResource">
            <el-icon><Monitor /></el-icon>
            <span>资源管理</span>
          </router-link>
        </el-menu-item>
        <el-menu-item index="7" @click="logout">
          <el-icon><SwitchButton /></el-icon>
          <span>退出登录</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <el-container>
      <el-header class="layout-header">
        <el-dropdown>
          <i class="el-icon-setting"></i>
          <template #dropdown>
            <el-dropdown-menu>
              <el-dropdown-item>查看</el-dropdown-item>
              <el-dropdown-item>新增</el-dropdown-item>
              <el-dropdown-item>删除</el-dropdown-item>
            </el-dropdown-menu>
          </template>
        </el-dropdown>
        <span>管理员</span>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </el-container>
</template>

<!-- 必须有完整的 script 标签（即使逻辑为空，也要保留） -->
<script setup lang="ts">
// 导入必要的组件和方法
import { ElMessage } from 'element-plus';
import { DataAnalysis, User, UploadFilled, SwitchButton, UserFilled, Document, Monitor } from '@element-plus/icons-vue';
import { useRouter } from 'vue-router';

// 路由实例
const router = useRouter();

// 退出登录逻辑
const logout = () => {
  localStorage.removeItem('token');
  ElMessage.success('退出成功');
  router.push('/login');
};
</script>

<!-- 样式标签（可选，但建议保留） -->
<style scoped>
.layout-container {
  height: 100vh;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
}

.layout-aside {
  background: linear-gradient(180deg, #1a1c2e 0%, #2d3250 100%);
  box-shadow: 4px 0 20px rgba(0, 0, 0, 0.15);
  position: relative;
  overflow: hidden;
}

.layout-aside::before {
  content: '';
  position: absolute;
  top: -100px;
  right: -50px;
  width: 150px;
  height: 150px;
  background: radial-gradient(circle, rgba(102, 126, 234, 0.15) 0%, transparent 70%);
  border-radius: 50%;
}

.layout-header {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  line-height: 60px;
  box-shadow: 0 4px 20px rgba(102, 126, 234, 0.3);
  position: relative;
  z-index: 10;
  text-align: right;
  padding-right: 30px;
}

.layout-header::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  border-radius: 50%;
}

.layout-header span {
  font-size: 15px;
  font-weight: 600;
  color: #fff;
}

:deep(.el-menu-vertical-demo) {
  border: none;
  padding: 20px 0;
  font-size: 15px;
  font-weight: 500;
  background: transparent;
}

:deep(.el-menu-item) {
  margin: 8px 16px;
  border-radius: 12px;
  transition: all 0.3s ease;
  height: 50px;
  line-height: 50px;
  display: flex;
  align-items: center;
  background: rgba(255, 255, 255, 0.05);
}

:deep(.el-menu-item:hover) {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.3) 0%, rgba(118, 75, 162, 0.3) 100%);
  transform: translateX(5px);
}

:deep(.el-menu-item.is-active) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

:deep(.el-menu-item .el-icon) {
  font-size: 18px;
  margin-right: 12px;
  color: #fff;
}

:deep(.el-menu-item span) {
  color: #fff;
  font-weight: 500;
}

:deep(.el-menu-item a) {
  display: flex;
  align-items: center;
  width: 100%;
  height: 100%;
  text-decoration: none;
  color: inherit;
}

:deep(.el-dropdown) {
  cursor: pointer;
}

:deep(.el-icon-setting) {
  font-size: 18px;
  color: #fff;
  transition: all 0.3s ease;
  margin-right: 15px;
}

:deep(.el-icon-setting:hover) {
  transform: rotate(90deg);
}

:deep(.el-dropdown-menu) {
  border-radius: 12px;
  box-shadow: 0 8px 30px rgba(0, 0, 0, 0.15);
  border: none;
  padding: 8px 0;
}

:deep(.el-dropdown-menu__item) {
  padding: 12px 20px;
  font-size: 14px;
  color: #2c3e50;
  transition: all 0.3s ease;
}

:deep(.el-dropdown-menu__item:hover) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

.el-main {
  padding: 30px;
  background: transparent;
}
</style>
