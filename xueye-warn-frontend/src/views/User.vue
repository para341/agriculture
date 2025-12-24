<template>
  <div class="user-container">
    <el-card>
      <el-dialog
          v-model="dialogVisible"
          :title="isEdit ? '编辑用户' : '新增用户'"
          width="500px"
          @close="resetForm"
      >
        <el-form ref="userFormRef" :model="userForm" :rules="userRules" label-width="100px">
          <el-form-item label="用户名" prop="username">
            <el-input v-model="userForm.username" placeholder="请输入用户名" />
          </el-form-item>
          <el-form-item label="密码" prop="password">
            <el-input v-model="userForm.password" type="password" placeholder="请输入密码" show-password />
          </el-form-item>
          <el-form-item label="角色" prop="role">
            <el-select v-model="userForm.role" placeholder="请选择角色">
              <el-option label="管理员" value="admin" />
              <el-option label="学生" value="student" />
            </el-select>
          </el-form-item>
          <el-form-item>
            <el-button type="primary" @click="submitForm">提交</el-button>
            <el-button @click="resetForm">重置</el-button>
          </el-form-item>
        </el-form>
      </el-dialog>

      <div class="operation-bar">
        <el-button type="primary" @click="openAddDialog">新增用户</el-button>
        <el-input
            v-model="searchText"
            placeholder="搜索用户名/角色"
            class="search-input"
            clearable
            @input="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <div class="debug-info">
          数据总数: {{ userList.length }} | 过滤后: {{ filteredUserList.length }}
        </div>
      </div>

      <el-table
          :data="filteredUserList"
          border
          height="600"
          style="margin-top: 20px;"
          stripe
          v-loading="loading"
          :empty-text="loading ? '加载中...' : '暂无数据'"
      >
        <el-table-column prop="id" label="ID" width="80" />
        <el-table-column prop="username" label="用户名" width="150" />
        <el-table-column prop="role" label="角色" width="120">
          <template #default="scope">
            <el-tag
                :type="scope.row.role === 'admin' ? 'danger' : 'success'"
            >
              {{ scope.row.role === 'admin' ? '管理员' : '学生' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="password" label="密码" width="200">
          <template #default="scope">
            <span>{{ '••••••••' }}</span>
          </template>
        </el-table-column>
        <el-table-column label="操作" width="200" fixed="right">
          <template #default="scope">
            <el-button type="primary" size="small" @click="editUser(scope.row)">编辑</el-button>
            <el-button type="danger" size="small" @click="delUser(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted, computed } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Search } from '@element-plus/icons-vue';
import type { FormInstance } from 'element-plus';
import { getUserList, addUser, updateUser, deleteUser } from '@/api/user';
import type { User } from '@/api/type';

const userList = ref<User[]>([]);
const loading = ref(false);
const searchText = ref('');

const dialogVisible = ref(false);
const userFormRef = ref<FormInstance>();
const isEdit = ref(false);

const userForm = reactive<User>({
  id: undefined,
  username: '',
  password: '',
  role: ''
});

const userRules = reactive({
  username: [{ required: true, message: '请输入用户名', trigger: 'blur' }],
  password: [{ required: true, message: '请输入密码', trigger: 'blur' }],
  role: [{ required: true, message: '请选择角色', trigger: 'change' }]
});

const filteredUserList = computed(() => {
  if (!searchText.value) return userList.value;

  const searchLower = searchText.value.toLowerCase();
  return userList.value.filter(user =>
      user.username.toLowerCase().includes(searchLower) ||
      user.role.toLowerCase().includes(searchLower)
  );
});

const getList = async () => {
  loading.value = true;
  try {
    console.log('开始获取用户数据...');
    const res = await getUserList();
    console.log('API响应:', res);

    if (res && typeof res === 'object') {
      if (res.code !== undefined && res.data !== undefined) {
        if (res.code === 200 && Array.isArray(res.data)) {
          userList.value = res.data;
          console.log('数据加载成功，总数:', userList.value.length);
          ElMessage.success(`成功加载 ${userList.value.length} 条用户数据`);
        } else {
          console.error('API返回格式错误:', res);
          ElMessage.error('数据格式错误');
        }
      } else if (Array.isArray(res)) {
        userList.value = res;
        console.log('直接数组数据加载成功，总数:', userList.value.length);
        ElMessage.success(`成功加载 ${userList.value.length} 条用户数据`);
      } else {
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

let searchTimer: NodeJS.Timeout;
const handleSearch = () => {
  clearTimeout(searchTimer);
  searchTimer = setTimeout(() => {
    console.log('搜索关键词:', searchText.value);
  }, 300);
};

const openAddDialog = () => {
  isEdit.value = false;
  userForm.id = undefined;
  userForm.username = '';
  userForm.password = '';
  userForm.role = '';
  dialogVisible.value = true;
};

const resetForm = () => {
  if (userFormRef.value) {
    userFormRef.value.resetFields();
  }
  Object.assign(userForm, {
    id: undefined,
    username: '',
    password: '',
    role: ''
  });
};

const editUser = (row: User) => {
  isEdit.value = true;
  const processedRow = {
    ...row,
    username: row.username || '',
    password: row.password || '',
    role: row.role || ''
  };
  Object.assign(userForm, processedRow);
  dialogVisible.value = true;
};

const delUser = async (id: number) => {
  try {
    await ElMessageBox.confirm(
        '确定要删除该用户吗？',
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        }
    );

    const res = await deleteUser(id);
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

const submitForm = async () => {
  if (!userFormRef.value) return;

  try {
    await userFormRef.value.validate();

    let res: any;

    if (isEdit.value) {
      res = await updateUser(userForm);
      if (res.code === 200) {
        ElMessage.success('修改成功');
      } else {
        ElMessage.error(res.msg || '修改失败');
        return;
      }
    } else {
      res = await addUser(userForm);
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

onMounted(() => {
  getList();
});
</script>

<style scoped>
.user-container {
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
</style>
