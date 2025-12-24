<template>
  <div class="student-container">
    <el-card>
      <!-- 新增/修改弹窗 -->
      <el-dialog
          v-model="dialogVisible"
          :title="isEdit ? '编辑学生' : '新增学生'"
          width="500px"
          @close="resetForm"
      >
        <el-form ref="studentFormRef" :model="studentForm" :rules="studentRules" label-width="100px">
          <el-form-item label="学号" prop="studentId">
            <el-input v-model="studentForm.studentId" placeholder="请输入学号" />
          </el-form-item>
          <el-form-item label="姓名" prop="name">
            <el-input v-model="studentForm.name" placeholder="请输入姓名" />
          </el-form-item>
          <el-form-item label="性别" prop="gender">
            <el-select v-model="studentForm.gender" placeholder="请选择性别">
              <el-option label="男" value="男" />
              <el-option label="女" value="女" />
            </el-select>
          </el-form-item>
          <el-form-item label="专业" prop="major">
            <el-input v-model="studentForm.major" placeholder="请输入专业" />
          </el-form-item>
          <el-form-item label="平均绩点" prop="grade">
            <el-input-number v-model="studentForm.grade" :min="0" :max="100" :precision="2" placeholder="请输入平均绩点" style="width: 100%;" />
          </el-form-item>
          <el-form-item label="预警等级" prop="warningLevel">
            <el-select v-model="studentForm.warningLevel" placeholder="请选择预警等级">
              <el-option label="正常" value="normal" />
              <el-option label="预警" value="warning" />
              <el-option label="严重" value="serious" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm">提交</el-button>
            <el-button @click="resetForm">重置</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>

      <!-- 操作区域 -->
      <div class="operation-bar">
        <el-button type="primary" @click="openAddDialog">新增学生</el-button>
        <el-button type="success" @click="handleExport">
          <el-icon><Download /></el-icon>
          导出Excel
        </el-button>
        <el-input
            v-model="searchText"
            placeholder="搜索学号/姓名/专业"
            class="search-input"
            clearable
            @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <!-- 调试信息 -->
        <div class="debug-info">
          数据总数: {{ studentList.length }} | 过滤后: {{ filteredStudentList.length }}
        </div>
      </div>

      <!-- 虚拟滚动表格 -->
      <el-table
          :data="filteredStudentList"
          border
          height="600"
          style="margin-top: 20px;"
          stripe
          v-loading="loading"
          :empty-text="loading ? '加载中...' : '暂无数据'"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="studentId" label="学号" width="120" />
        <el-table-column prop="name" label="姓名" width="100" />
        <el-table-column prop="gender" label="性别" width="80" />
        <el-table-column prop="major" label="专业" width="150" />
        <el-table-column prop="grade" label="平均绩点" width="120">
          <template #default="scope">
            <el-tag
                :type="scope.row.grade >= 70 ? 'success' :
                     scope.row.grade >= 60 ? 'warning' : 'danger'"
            >
              {{ scope.row.grade ? scope.row.grade.toFixed(2) : '-' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="warningLevel" label="预警等级" width="120">
          <template #default="scope">
            <el-tag
                :type="scope.row.warningLevel === 'serious' ? 'danger' :
                     scope.row.warningLevel === 'warning' ? 'warning' : 'success'"
            >
              {{ scope.row.warningLevel === 'normal' ? '正常' :
                scope.row.warningLevel === 'warning' ? '预警' : '严重' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editStudent(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="delStudent(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>

    <div class="page-footer">
      <a href="https://github.com/para341/school" target="_blank" class="github-link">
        GitHub: https://github.com/para341/school
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Search, Download } from '@element-plus/icons-vue';
import type { FormInstance } from 'element-plus';
import { getStudentList, addStudent, updateStudent, deleteStudent, exportStudentExcel } from '@/api/student';
import type { Student } from '@/api/type';

// 状态变量
const studentList = ref<Student[]>([]);
const loading = ref(false);
const searchText = ref('');

// 弹窗相关
const dialogVisible = ref(false);
const studentFormRef = ref<FormInstance>();
const isEdit = ref(false);

// 表单数据
const studentForm = reactive<Student>({
  id: undefined,
  studentId: '',
  name: '',
  gender: '',
  major: '',
  grade: undefined,
  warningLevel: ''
});

// 表单校验规则
const studentRules = reactive({
  studentId: [{ required: true, message: '请输入学号', trigger: 'blur' }],
  name: [{ required: true, message: '请输入姓名', trigger: 'blur' }],
  gender: [{ required: true, message: '请选择性别', trigger: 'change' }],
  major: [{ required: true, message: '请输入专业', trigger: 'blur' }],
  warningLevel: [{ required: true, message: '请选择预警等级', trigger: 'change' }]
});

// 过滤后的学生列表
const filteredStudentList = computed(() => {
  if (!searchText.value) return studentList.value;

  const searchLower = searchText.value.toLowerCase();
  return studentList.value.filter(student =>
      student.studentId.toLowerCase().includes(searchLower) ||
      student.name.toLowerCase().includes(searchLower) ||
      student.major.toLowerCase().includes(searchLower)
  );
});

// 获取所有学生数据（增强版）
const getList = async () => {
  loading.value = true;
  try {
    console.log('开始获取学生数据...');
    const res = await getStudentList();
    console.log('API响应:', res);

    // 检查响应格式
    if (res && typeof res === 'object') {
      // 如果是ApiResponse格式，提取data
      if (res.code !== undefined && res.data !== undefined) {
        if (res.code === 200 && Array.isArray(res.data)) {
          studentList.value = res.data;
          console.log('数据加载成功，总数:', studentList.value.length);
          ElMessage.success(`成功加载 ${studentList.value.length} 条学生数据`);
        } else {
          console.error('API返回格式错误:', res);
          ElMessage.error('数据格式错误');
        }
      }
      // 如果直接返回数组（可能API没有包装）
      else if (Array.isArray(res)) {
        studentList.value = res;
        console.log('直接数组数据加载成功，总数:', studentList.value.length);
        ElMessage.success(`成功加载 ${studentList.value.length} 条学生数据`);
      }
      // 其他格式
      else {
        console.error('未知响应格式:', res);
        ElMessage.error('未知响应格式');
      }
    } else {
      console.error('响应不是对象:', res);
      ElMessage.error('响应格式错误');
    }
  } catch (error) {
    console.error('获取列表异常:', error);
    ElMessage.error('获取列表失败: ' + (error as Error).message);
  } finally {
    loading.value = false;
  }
};

// 搜索处理（防抖）
let searchTimer: NodeJS.Timeout;
const handleSearch = () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => {
    console.log('搜索关键词:', searchText.value);
  }, 300);
};

// 打开新增弹窗
const openAddDialog = () => {
  isEdit.value = false;
  studentForm.id = undefined;
  studentForm.studentId = '';
  studentForm.name = '';
  studentForm.gender = '';
  studentForm.major = '';
  studentForm.grade = undefined;
  studentForm.warningLevel = '';
  dialogVisible.value = true;
};

const resetForm = () => {
  if (studentFormRef.value) {
    studentFormRef.value.resetFields();
  }
  // 确保所有字段都有初始值
  Object.assign(studentForm, {
    id: undefined,
    studentId: '',
    name: '',
    gender: '',
    major: '',
    grade: undefined,
    warningLevel: ''
  });
};

const editStudent = (row: Student) => {
  isEdit.value = true;
  // 处理可能为null的字段
  const processedRow = {
    ...row,
    studentId: row.studentId || '',
    name: row.name || '',
    gender: row.gender || '',
    major: row.major || '',
    grade: row.grade,
    warningLevel: row.warningLevel || ''
  };
  Object.assign(studentForm, processedRow);
  dialogVisible.value = true;
};


// 删除学生
const delStudent = async (id: number) => {
  try {
    await ElMessageBox.confirm(
        '确定要删除该学生信息吗？',
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        }
    );

    const res = await deleteStudent(id);
    if (res.code === 200) {
      ElMessage.success('删除成功');
      getList();
    } else {
      ElMessage.error(res.msg || '删除失败');
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败');
    }
  }
};

// 提交表单（新增/编辑）
const submitForm = async () => {
  if (!studentFormRef.value) return;

  try {
    await studentFormRef.value.validate();

    let res: any;

    if (isEdit.value) {
      res = await updateStudent(studentForm);
      if (res.code === 200) {
        ElMessage.success('修改成功');
      } else {
        ElMessage.error(res.msg || '修改失败');
        return;
      }
    } else {
      res = await addStudent(studentForm);
      if (res.code === 200) {
        ElMessage.success('新增成功');
      } else {
        ElMessage.error(res.msg || '新增失败');
        return;
      }
    }

    dialogVisible.value = false;
    getList();
  } catch (error) {
    console.error('表单验证失败:', error);
  }
};

// 导出学生信息为Excel
const handleExport = async () => {
  try {
    const res = await exportStudentExcel();
    const blob = new Blob([res.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `学生信息_${new Date().getTime()}.xlsx`;
    link.click();
    window.URL.revokeObjectURL(url);
    ElMessage.success('导出成功');
  } catch (error) {
    console.error('导出失败:', error);
    ElMessage.error('导出失败');
  }
};

// 初始化加载
onMounted(() => {
  getList();
});
</script>

<style scoped>
.student-container {
  padding: 0;
}

:deep(.el-card) {
  border-radius: 20px;
  box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
  border: none;
  overflow: hidden;
  background: rgba(255, 255, 255, 0.95);
  backdrop-filter: blur(10px);
}

:deep(.el-card__body) {
  padding: 30px;
}

.operation-bar {
  display: flex;
  align-items: center;
  margin-bottom: 25px;
  gap: 15px;
}

.search-input {
  width: 320px;
}

.debug-info {
  margin-left: auto;
  color: #666;
  font-size: 14px;
  font-weight: 500;
  padding: 8px 16px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
  border-radius: 10px;
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 10px;
  padding: 10px 24px;
  font-size: 14px;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
  transition: all 0.3s ease;
}

:deep(.el-button--primary:hover) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
}

:deep(.el-button--primary:active) {
  transform: translateY(0);
}

:deep(.el-button--default) {
  border-radius: 10px;
  padding: 10px 24px;
  font-size: 14px;
  transition: all 0.3s ease;
  border: 2px solid #e8ecf1;
}

:deep(.el-button--default:hover) {
  transform: translateY(-2px);
  border-color: #667eea;
  color: #667eea;
}

:deep(.el-button--danger) {
  background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
  border: none;
  border-radius: 8px;
  padding: 8px 16px;
  font-size: 13px;
  transition: all 0.3s ease;
}

:deep(.el-button--danger:hover) {
  transform: translateY(-2px);
  box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
}

:deep(.el-button--small) {
  padding: 8px 16px;
  border-radius: 8px;
}

:deep(.el-input__wrapper) {
  border-radius: 10px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  border: 2px solid #e8ecf1;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
  border-color: #c4c9d2;
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  border-color: #667eea;
}

:deep(.el-select .el-input__wrapper) {
  cursor: pointer;
}

:deep(.el-table) {
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.05);
}

:deep(.el-table th) {
  background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
  color: #2c3e50;
  font-weight: 600;
  font-size: 14px;
}

:deep(.el-table tr:hover > td) {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.05) 0%, rgba(118, 75, 162, 0.05) 100%);
}

:deep(.el-table td) {
  border-bottom: 1px solid #f0f0f0;
}

:deep(.el-table--border .el-table__cell) {
  border-right: 1px solid #f0f0f0;
}

:deep(.el-table--border::after),
:deep(.el-table--group::after),
:deep(.el-table::before) {
  background-color: #f0f0f0;
}

:deep(.el-tag) {
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 13px;
  font-weight: 500;
  border: none;
}

:deep(.el-tag--success) {
  background: linear-gradient(135deg, #84fab0 0%, #8fd3f4 100%);
  color: #fff;
}

:deep(.el-tag--warning) {
  background: linear-gradient(135deg, #f6d365 0%, #fda085 100%);
  color: #fff;
}

:deep(.el-tag--danger) {
  background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
  color: #fff;
}

:deep(.el-dialog) {
  border-radius: 20px;
  overflow: hidden;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
}

:deep(.el-dialog__header) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px 25px;
  margin: 0;
}

:deep(.el-dialog__title) {
  color: #fff;
  font-size: 18px;
  font-weight: 600;
}

:deep(.el-dialog__headerbtn .el-dialog__close) {
  color: #fff;
  font-size: 20px;
  transition: all 0.3s ease;
}

:deep(.el-dialog__headerbtn .el-dialog__close:hover) {
  transform: rotate(90deg);
}

:deep(.el-dialog__body) {
  padding: 30px 25px;
}

:deep(.el-form-item__label) {
  color: #2c3e50;
  font-weight: 600;
  font-size: 14px;
}

:deep(.el-form-item) {
  margin-bottom: 22px;
}

:deep(.el-select-dropdown__item) {
  border-radius: 8px;
  margin: 4px 8px;
  transition: all 0.3s ease;
}

:deep(.el-select-dropdown__item:hover) {
  background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
  color: #667eea;
}

:deep(.el-select-dropdown__item.is-selected) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

:deep(.el-message-box) {
  border-radius: 16px;
  box-shadow: 0 20px 60px rgba(0, 0, 0, 0.25);
}

:deep(.el-message-box__header) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  padding: 20px;
}

:deep(.el-message-box__title) {
  color: #fff;
  font-weight: 600;
}

:deep(.el-message-box__content) {
  padding: 30px 20px;
}

:deep(.el-message-box__btns) {
  padding: 15px 20px;
  border-top: 1px solid #f0f0f0;
}

.page-footer {
  margin-top: 30px;
  text-align: center;
  padding: 20px 0;
}

.github-link {
  color: #999;
  font-size: 12px;
  text-decoration: none;
  transition: color 0.3s ease;
}

.github-link:hover {
  color: #667eea;
}
</style>
