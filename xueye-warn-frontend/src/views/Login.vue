<template>
  <!-- 全屏根容器：实现渐变背景 + 装饰元素 -->
  <div class="login-page">
    <!-- 背景装饰圆形 -->
    <div class="bg-decoration">
      <div class="circle circle-1"></div>
      <div class="circle circle-2"></div>
    </div>

    <!-- 手机插画装饰 -->
    <div class="illustration">
      <div class="phone">
        <div class="phone-screen"></div>
        <div class="person person-1"></div>
        <div class="person person-2"></div>
      </div>
    </div>

    <!-- 装饰性小图标 -->
    <div class="decoration-icon icon-1"></div>
    <div class="decoration-icon icon-2"></div>
    <div class="decoration-icon icon-3"></div>

    <!-- 登录容器：保留Element Plus表单逻辑，替换样式 -->
    <div class="login-container">
      <!-- 系统logo + 标题 -->
      <div class="logo-container">
        <div class="logo"></div>
        <div class="logo-text">学业预警系统</div>
      </div>

      <!-- 角色选择按钮 -->
      <div class="role-selector">
        <el-radio-group v-model="selectedRole" size="large">
          <el-radio-button label="admin">管理员登录</el-radio-button>
          <el-radio-button label="student">学生登录</el-radio-button>
        </el-radio-group>
      </div>

      <!-- 保留原有Element Plus表单校验逻辑 -->
      <el-form
          :model="loginForm"
          :rules="loginRules"
          ref="loginFormRef"
          label-width="0"
          class="login-form"
      >
        <el-form-item prop="username">
          <label class="form-label">请输入用户名</label>
          <el-input
              v-model="loginForm.username"
              placeholder="请输入用户名"
              class="form-input"
          ></el-input>
        </el-form-item>
        <el-form-item prop="password">
          <label class="form-label">请输入密码</label>
          <el-input
              v-model="loginForm.password"
              type="password"
              placeholder="请输入密码"
              class="form-input"
          ></el-input>
        </el-form-item>
        <el-form-item>
          <el-button
              type="primary"
              @click="handleLogin"
              class="login-btn"
          >
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </div>
  </div>
</template>

<script setup lang="ts">
// 保留原有TS逻辑，无任何修改
import { ref, reactive } from 'vue';
import { ElMessage } from 'element-plus';
import { useRouter } from 'vue-router';
import { login } from '@/api/login';

const router = useRouter();
const loginFormRef = ref<any>(null);

// 登录表单
const loginForm = reactive({
  username: '',
  password: '',
});

// 表单校验规则
const loginRules = reactive({
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
});

// 角色选择
const selectedRole = ref('admin'); // 默认选择管理员

const handleLogin = async () => {
  try {
    await loginFormRef.value.validate();
    const res = await login({
      username: loginForm.username,
      password: loginForm.password,
      role: selectedRole.value
    });

    localStorage.setItem('token', res.data);
    localStorage.setItem('role', selectedRole.value);

    ElMessage.success('登录成功');

    // 根据角色跳转到不同页面
    if (selectedRole.value === 'admin') {
      router.push('/dashboard');
    } else {
      router.push('/student-warning-status'); // 学生跳转到预警状态页面
    }
  } catch (error) {
    console.error('登录失败:', error);
    ElMessage.error('登录失败，请检查账号密码或网络');
  }
};

</script>

<style scoped>
.login-page {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
  overflow: hidden;
  margin: 0;
  padding: 20px;
  box-sizing: border-box;
  font-family: 'Microsoft YaHei', sans-serif;
}

.bg-decoration {
  position: absolute;
  width: 100%;
  height: 100%;
  z-index: 0;
}

.bg-decoration .circle {
  position: absolute;
  border-radius: 50%;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.15) 0%, transparent 70%);
}

.circle-1 {
  width: 400px;
  height: 400px;
  top: -200px;
  left: -150px;
}

.circle-2 {
  width: 300px;
  height: 300px;
  bottom: -150px;
  right: -100px;
}

.illustration {
  position: absolute;
  bottom: 80px;
  left: 80px;
  z-index: 1;
}

.phone {
  width: 280px;
  height: 480px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 30px;
  position: relative;
  perspective: 500px;
  transform: rotate(-15deg);
  -webkit-transform: rotate(-15deg);
  -moz-transform: rotate(-15deg);
  -ms-transform: rotate(-15deg);
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
  backdrop-filter: blur(10px);
}

.phone-screen {
  width: 90%;
  height: 80%;
  background: rgba(255, 255, 255, 0.9);
  margin: 5% auto;
  border-radius: 15px;
  position: relative;
  overflow: hidden;
}

.person {
  position: absolute;
  width: 60px;
  height: 80px;
}

.person-1 {
  top: 50px;
  left: 80px;
}

.person-2 {
  bottom: 80px;
  left: 120px;
}

.decoration-icon {
  position: absolute;
  z-index: 1;
}

.icon-1 {
  top: 120px;
  right: 180px;
  width: 60px;
  height: 60px;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 15px;
  backdrop-filter: blur(5px);
}

.icon-2 {
  bottom: 180px;
  right: 120px;
  width: 50px;
  height: 50px;
  background: rgba(255, 255, 255, 0.15);
  border-radius: 50%;
  backdrop-filter: blur(5px);
}

.icon-3 {
  bottom: 250px;
  right: 250px;
  width: 40px;
  height: 40px;
  background: rgba(255, 255, 255, 0.1);
  border-radius: 50%;
  backdrop-filter: blur(5px);
}

.login-container {
  background: rgba(255, 255, 255, 0.95);
  padding: 50px 45px;
  border-radius: 24px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
  width: 420px;
  z-index: 10;
  position: relative;
  backdrop-filter: blur(20px);
  transition: all 0.4s ease;
}

.login-container:hover {
  transform: translateY(-8px);
  box-shadow: 0 30px 80px rgba(0, 0, 0, 0.3);
}

.logo-container {
  text-align: center;
  margin-bottom: 35px;
}

.logo {
  width: 70px;
  height: 70px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  display: inline-block;
  margin-bottom: 15px;
  position: relative;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.logo::after {
  content: "";
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 45px;
  height: 45px;
  border-radius: 50%;
  background: white;
}

.logo-text {
  font-size: 24px;
  font-weight: 700;
  background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.role-selector {
  margin-bottom: 25px;
  text-align: center;
}

.login-form {
  width: 100%;
}

.form-label {
  display: block;
  margin-bottom: 10px;
  color: #2c3e50;
  font-size: 14px;
  font-weight: 600;
}

.form-input {
  width: 100%;
  padding: 14px 18px;
  border: 2px solid #e8ecf1;
  border-radius: 12px;
  font-size: 15px;
  transition: all 0.3s ease;
  background: #f8f9fa;
}

.form-input:focus {
  outline: none;
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
  background: white;
}

.login-btn {
  width: 100%;
  padding: 14px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border: none;
  border-radius: 12px;
  font-size: 16px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
}

.login-btn:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(102, 126, 234, 0.5);
}

.login-btn:active {
  transform: translateY(0);
}

:deep(.el-form-item) {
  margin-bottom: 24px;
}

:deep(.el-form-item__error) {
  color: #f5576c;
  font-size: 13px;
}

:deep(.el-input__wrapper) {
  border: none;
  box-shadow: none;
  padding: 0;
  border-radius: 12px;
  background: transparent;
}

:deep(.el-input__inner) {
  padding: 14px 18px;
  border: 2px solid #e8ecf1;
  border-radius: 12px;
  font-size: 15px;
  transition: all 0.3s ease;
  background: #f8f9fa;
}

:deep(.el-input__inner:focus) {
  border-color: #667eea;
  box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
  background: white;
}

:deep(.el-input__inner:hover) {
  border-color: #c4c9d2;
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 12px;
  padding: 14px 20px;
  font-size: 16px;
  font-weight: 600;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
}

:deep(.el-button--primary:hover) {
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(102, 126, 234, 0.5);
}

:deep(.el-button--primary:active) {
  transform: translateY(0);
}

:deep(.el-radio-group) {
  display: flex;
  width: 100%;
  gap: 10px;
}

:deep(.el-radio-button) {
  flex: 1;
}

:deep(.el-radio-button__inner) {
  width: 100%;
  border-radius: 10px;
  border: 2px solid #e8ecf1;
  background: #f8f9fa;
  color: #2c3e50;
  font-weight: 600;
  padding: 12px 0;
  transition: all 0.3s ease;
}

:deep(.el-radio-button__original-radio:checked + .el-radio-button__inner) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-color: #667eea;
  color: white;
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

:deep(.el-radio-button__inner:hover) {
  border-color: #667eea;
  color: #667eea;
}

:deep(.el-radio-button__original-radio:checked + .el-radio-button__inner:hover) {
  color: white;
}
</style>
