// vue-router 4.x 内置类型，TS 可自动识别，无需额外导入
import { createRouter, createWebHistory } from 'vue-router';

// 导入组件（路径已存在）
import Login from '@/views/Login.vue';
import Layout from '@/layout/Layout.vue';

// 路由规则：补充 meta 鉴权标识，保持 any 兜底兼容你的 TS 配置
const routes = [
  {
    path: '/login',
    name: 'Login',
    component: Login,
    meta: { requiresAuth: false } // 登录页不需要鉴权
  },
  {
    path: '/student-warning-status',
    name: 'StudentWarningStatus',
    component: () => import('@/views/StudentWarningStatus.vue'),
    meta: { requiresAuth: true, role: 'student' } // 学生专属页面，不使用Layout
  },
  {
    path: '/',
    name: 'Layout',
    component: Layout,
    redirect: '/dashboard',
    meta: { requiresAuth: true, role: 'admin' }, // 管理员主布局需要鉴权
    children: [
      {
        path: 'dashboard',
        name: 'Dashboard',
        component: () => import('@/views/Dashboard.vue')
      },
      {
        path: 'student',
        name: 'Student',
        component: () => import('@/views/Student.vue')
      },
      {
        path: 'hadoop',
        name: 'Hadoop',
        component: () => import('@/views/Hadoop.vue')
      },
      {
        path: 'user',
        name: 'User',
        component: () => import('@/views/User.vue')
      },
      {
        path: 'loginLog',
        name: 'LoginLog',
        component: () => import('@/views/LoginLog.vue')
      },
      {
        path: 'systemResource',
        name: 'SystemResource',
        component: () => import('@/views/SystemResource.vue')
      },
    ],
  },
];

// 创建路由实例（Vue CLI 适配）
const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

// 核心新增：首次加载页面时，强制清除 LocalStorage 中的 token
// 用 sessionStorage 标记"是否已清除过token"，避免每次路由跳转都清
if (!sessionStorage.getItem('tokenCleared')) {
  localStorage.removeItem('token'); // 清除登录凭证
  sessionStorage.setItem('tokenCleared', 'true'); // 标记已清除，仅首次加载执行
}

// 路由守卫：优化鉴权逻辑，补充"已登录禁止回登录页"和"角色权限控制"
router.beforeEach((to: any, from: any, next: any) => {
  const token = localStorage.getItem('token');
  const role = localStorage.getItem('role');

  // 场景1：要访问需要鉴权的页面，但没有token → 强制跳登录页
  if (to.meta.requiresAuth && !token) {
    next('/login');
  }
  // 场景2：已有token，却要访问登录页 → 自动跳首页（避免重复登录）
  else if (to.path === '/login' && token) {
    if (role === 'admin') {
      next('/dashboard');
    } else {
      next('/student-warning-status');
    }
  }
  // 场景3：学生尝试访问管理员页面 → 重定向到学生页面
  else if (role === 'student' && to.meta.role === 'admin') {
    next('/student-warning-status');
  }
  // 场景4：管理员尝试访问学生页面 → 重定向到管理员页面
  else if (role === 'admin' && to.meta.role === 'student') {
    next('/dashboard');
  }
  // 场景5：其他情况 → 正常放行
  else {
    next();
  }
});

export default router;
