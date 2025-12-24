<template>
  <div class="student-warning-status-container">
    <div class="student-header">
      <div class="header-content">
        <h2>学业预警系统</h2>
        <div class="header-actions">
          <span class="welcome-text">欢迎，学生</span>
          <el-button type="danger" size="small" @click="handleLogout">退出登录</el-button>
        </div>
      </div>
    </div>

    <el-card class="query-card">
      <div class="query-header">
        <h2>学生预警状态查询</h2>
      </div>
      
      <el-form :model="queryForm" :rules="queryRules" ref="queryFormRef" label-width="80px">
        <el-form-item label="学号" prop="studentId">
          <el-input 
            v-model="queryForm.studentId" 
            placeholder="请输入学号" 
            clearable
            @keyup.enter="handleQuery"
          />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="handleQuery" :loading="loading">查询</el-button>
          <el-button @click="resetQuery">重置</el-button>
        </el-form-item>
      </el-form>
    </el-card>

    <el-card class="result-card" v-if="warningData">
      <div class="result-header">
        <h3>预警信息</h3>
      </div>

      <el-descriptions title="学生基本信息" :column="2" border>
        <el-descriptions-item label="学号">{{ warningData.studentId }}</el-descriptions-item>
        <el-descriptions-item label="姓名">{{ warningData.name }}</el-descriptions-item>
        <el-descriptions-item label="性别">{{ warningData.gender }}</el-descriptions-item>
        <el-descriptions-item label="专业">{{ warningData.major }}</el-descriptions-item>
        <el-descriptions-item label="平均绩点">
          <el-tag :type="getGradeType(warningData.grade)">
            {{ warningData.grade ? warningData.grade.toFixed(2) : '-' }}
          </el-tag>
        </el-descriptions-item>
        <el-descriptions-item label="预警等级">
          <el-tag :type="getWarningLevelType(warningData.warningLevel)">
            {{ getWarningLevelText(warningData.warningLevel) }}
          </el-tag>
        </el-descriptions-item>
      </el-descriptions>

      <div class="warning-details" v-if="warningData.warningLevel !== 'normal'">
        <h4>预警详情</h4>
        <el-alert
          :title="getWarningTitle(warningData.warningLevel)"
          :type="getWarningLevelType(warningData.warningLevel)"
          :description="getWarningDescription(warningData.warningLevel)"
          show-icon
          :closable="false"
        />
      </div>

      <div class="warning-suggestions" v-if="warningData.warningLevel !== 'normal'">
        <h4>改进建议</h4>
        <ul>
          <li v-for="(suggestion, index) in getSuggestions(warningData.warningLevel)" :key="index">
            {{ suggestion }}
          </li>
        </ul>
      </div>
    </el-card>

    <el-empty v-else-if="!loading && hasQueried" description="未找到相关预警信息" />
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue';
import { useRouter } from 'vue-router';
import { ElMessage } from 'element-plus';
import { getStudentWarningStatus } from '@/api/student';

const router = useRouter();
const queryFormRef = ref<any>(null);
const loading = ref(false);
const hasQueried = ref(false);
const warningData = ref<any>(null);

const queryForm = reactive({
  studentId: ''
});

const queryRules = reactive({
  studentId: [
    { required: true, message: '请输入学号', trigger: 'blur' }
  ]
});

const getWarningLevelType = (level: string) => {
  switch (level) {
    case 'serious': return 'danger';
    case 'warning': return 'warning';
    default: return 'success';
  }
};

const getGradeType = (grade: number) => {
  if (!grade) return 'info';
  if (grade >= 70) return 'success';
  if (grade >= 60) return 'warning';
  return 'danger';
};

const getWarningLevelText = (level: string) => {
  switch (level) {
    case 'serious': return '严重预警';
    case 'warning': return '预警';
    default: return '正常';
  }
};

const getWarningTitle = (level: string) => {
  switch (level) {
    case 'serious': return '学业严重预警';
    case 'warning': return '学业预警';
    default: return '学业正常';
  }
};

const getWarningDescription = (level: string) => {
  switch (level) {
    case 'serious': return '您的学业状况存在严重问题，请立即采取行动改善学习状态。';
    case 'warning': return '您的学业状况需要关注，建议及时调整学习方法。';
    default: return '您的学业状况良好，请继续保持。';
  }
};

const getSuggestions = (level: string) => {
  switch (level) {
    case 'serious':
      return [
        '立即联系辅导员或导师，制定详细的学习计划',
        '分析挂科原因，寻求任课老师的帮助',
        '积极参加辅导课程和答疑活动',
        '调整作息时间，保证充足的学习时间',
        '寻求心理咨询，缓解学习压力'
      ];
    case 'warning':
      return [
        '关注学习进度，及时复习课程内容',
        '主动与任课老师沟通，了解学习要求',
        '参加学习小组，与同学互助学习',
        '合理安排时间，平衡各科学习',
        '定期自我评估，及时调整学习策略'
      ];
    default:
      return [
        '保持良好的学习习惯',
        '积极参与课堂互动',
        '定期复习巩固知识',
        '关注课程进度，提前预习'
      ];
  }
};

const handleQuery = async () => {
  try {
    await queryFormRef.value.validate();
    loading.value = true;
    hasQueried.value = true;
    
    const res = await getStudentWarningStatus({
      studentId: queryForm.studentId
    });
    
    if (res && res.data) {
      warningData.value = res.data;
      ElMessage.success('查询成功');
    } else {
      warningData.value = null;
      ElMessage.warning('未找到相关学生信息');
    }
  } catch (error) {
    console.error('查询失败:', error);
    ElMessage.error('查询失败，请检查学号是否正确');
    warningData.value = null;
  } finally {
    loading.value = false;
  }
};

const resetQuery = () => {
  queryFormRef.value?.resetFields();
  warningData.value = null;
  hasQueried.value = false;
};

const handleLogout = () => {
  localStorage.removeItem('token');
  localStorage.removeItem('role');
  ElMessage.success('退出成功');
  router.push('/login');
};
</script>

<style scoped>
.student-warning-status-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

.student-header {
  background: linear-gradient(135deg, #1a1c2e 0%, #2d3250 100%);
  color: white;
  padding: 0 20px;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2);
  border-radius: 16px;
  margin-bottom: 30px;
  position: relative;
  overflow: hidden;
}

.student-header::before {
  content: '';
  position: absolute;
  top: -50%;
  right: -10%;
  width: 200px;
  height: 200px;
  background: radial-gradient(circle, rgba(255, 255, 255, 0.1) 0%, transparent 70%);
  border-radius: 50%;
}

.header-content {
  max-width: 1200px;
  margin: 0 auto;
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 70px;
  position: relative;
  z-index: 1;
}

.header-content h2 {
  margin: 0;
  font-size: 24px;
  font-weight: 600;
  background: linear-gradient(90deg, #fff 0%, #a8c0ff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 20px;
}

.welcome-text {
  font-size: 15px;
  color: #ffffff;
  font-weight: 500;
}

.query-card {
  max-width: 900px;
  margin: 0 auto 30px;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  border: none;
  overflow: hidden;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
}

.query-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2);
}

.query-header {
  text-align: center;
  margin-bottom: 30px;
  padding: 20px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  margin: -20px -20px 30px -20px;
}

.query-header h2 {
  color: #fff;
  margin: 0;
  font-size: 22px;
  font-weight: 600;
}

.result-card {
  max-width: 900px;
  margin: 0 auto;
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.15);
  border: none;
  overflow: hidden;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
}

.result-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 50px rgba(0, 0, 0, 0.2);
}

.result-header {
  margin-bottom: 25px;
  padding: 20px 0;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  margin: -20px -20px 25px -20px;
}

.result-header h3 {
  color: #fff;
  margin: 0;
  font-size: 20px;
  font-weight: 600;
  text-align: center;
}

.warning-details {
  margin-top: 25px;
  padding: 20px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
  border-radius: 12px;
  border-left: 4px solid #667eea;
}

.warning-details h4 {
  color: #2c3e50;
  margin-bottom: 15px;
  font-size: 16px;
  font-weight: 600;
}

.warning-suggestions {
  margin-top: 25px;
  padding: 25px;
  background: linear-gradient(135deg, #fff9e6 0%, #fff3cd 100%);
  border-radius: 12px;
  border-left: 4px solid #ffc107;
}

.warning-suggestions h4 {
  color: #2c3e50;
  margin: 0 0 15px 0;
  font-size: 16px;
  font-weight: 600;
}

.warning-suggestions ul {
  margin: 0;
  padding-left: 20px;
}

.warning-suggestions li {
  color: #555;
  line-height: 2;
  margin: 8px 0;
  font-size: 14px;
  position: relative;
  padding-left: 10px;
}

.warning-suggestions li::before {
  content: '✓';
  position: absolute;
  left: -20px;
  color: #ffc107;
  font-weight: bold;
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  padding: 12px 30px;
  font-size: 15px;
  border-radius: 10px;
  transition: all 0.3s ease;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}

:deep(.el-button--primary:hover) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}

:deep(.el-button--default) {
  border-radius: 10px;
  padding: 12px 30px;
  font-size: 15px;
  transition: all 0.3s ease;
}

:deep(.el-button--default:hover) {
  transform: translateY(-2px);
}

:deep(.el-button--danger) {
  background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
  border: none;
  border-radius: 8px;
  padding: 8px 20px;
  transition: all 0.3s ease;
}

:deep(.el-button--danger:hover) {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
}

:deep(.el-input__wrapper) {
  border-radius: 10px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
}

:deep(.el-descriptions) {
  border-radius: 12px;
  overflow: hidden;
}

:deep(.el-descriptions__label) {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  font-weight: 600;
  color: #2c3e50;
}

:deep(.el-descriptions__body) {
  background: #fff;
}

:deep(.el-alert) {
  border-radius: 10px;
  border: none;
}

:deep(.el-empty) {
  padding: 60px 0;
}

:deep(.el-empty__description) {
  color: #666;
  font-size: 16px;
}
</style>
