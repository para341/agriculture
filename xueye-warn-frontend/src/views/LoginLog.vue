<template>
  <div class="loginlog-container">
    <el-card>
      <div class="operation-bar">
        <el-input
            v-model="searchForm.username"
            placeholder="搜索用户名"
            class="search-input"
            clearable
            @clear="handleSearch"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <el-select
            v-model="searchForm.role"
            placeholder="选择角色"
            class="search-select"
            clearable
            @clear="handleSearch"
            @change="handleSearch"
        >
          <el-option label="管理员" value="admin" />
          <el-option label="学生" value="student" />
        </el-select>
        <el-button type="success" @click="handleExport">
          <el-icon><Download /></el-icon>
          导出Excel
        </el-button>
        <el-button type="danger" @click="handleBatchDelete" :disabled="selectedIds.length === 0">
          批量删除
        </el-button>
        <el-button @click="handleRefresh">
          <el-icon><Refresh /></el-icon>
          刷新
        </el-button>
      </div>

      <el-table
          :data="loginLogList"
          border
          height="600"
          style="margin-top: 20px;"
          stripe
          v-loading="loading"
          @selection-change="handleSelectionChange"
      >
        <el-table-column type="selection" width="55" />
        <el-table-column prop="username" label="用户名" width="200" />
        <el-table-column prop="role" label="角色" width="150">
          <template #default="scope">
            <el-tag
                :type="scope.row.role === 'admin' ? 'danger' : 'success'"
            >
              {{ scope.row.role === 'admin' ? '管理员' : '学生' }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="loginTime" label="登录时间" width="200" />
        <el-table-column label="操作" width="100" fixed="right">
          <template #default="scope">
            <el-button type="danger" size="small" @click="handleDelete(scope.row.id)">删除</el-button>
          </template>
        </el-table-column>
      </el-table>

      <el-pagination
          v-model:current-page="pagination.current"
          v-model:page-size="pagination.size"
          :total="pagination.total"
          :page-sizes="[10, 20, 50, 100]"
          layout="total, sizes, prev, pager, next, jumper"
          @size-change="handleSearch"
          @current-change="handleSearch"
          style="margin-top: 20px; justify-content: flex-end;"
      />
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue';
import { ElMessage, ElMessageBox } from 'element-plus';
import { Search, Refresh, Download } from '@element-plus/icons-vue';
import { getLoginLogPage, deleteLoginLog, batchDeleteLoginLog, exportLoginLogExcel } from '@/api/loginLog';

const loginLogList = ref<any[]>([]);
const loading = ref(false);
const selectedIds = ref<number[]>([]);

const searchForm = reactive({
  username: '',
  role: ''
});

const pagination = reactive({
  current: 1,
  size: 10,
  total: 0
});

const getList = async () => {
  loading.value = true;
  try {
    const res: any = await getLoginLogPage({
      current: pagination.current,
      size: pagination.size,
      username: searchForm.username || undefined,
      role: searchForm.role || undefined
    });

    if (res && res.code === 200) {
      loginLogList.value = res.data.records || [];
      pagination.total = res.data.total || 0;
    } else {
      ElMessage.error('获取日志列表失败');
    }
  } catch (error) {
    console.error('获取日志列表异常:', error);
    ElMessage.error('获取日志列表失败');
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => {
  pagination.current = 1;
  getList();
};

const handleRefresh = () => {
  searchForm.username = '';
  searchForm.role = '';
  pagination.current = 1;
  getList();
};

const handleSelectionChange = (selection: any[]) => {
  selectedIds.value = selection.map(item => item.id);
};

const handleDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm(
        '确定要删除该日志吗？',
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        }
    );

    const res = await deleteLoginLog(id);
    if (res.data && res.data.code === 200) {
      ElMessage.success('删除成功');
      getList();
    } else {
      ElMessage.error(res.data?.msg || '删除失败');
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('删除失败');
    }
  }
};

const handleBatchDelete = async () => {
  if (selectedIds.value.length === 0) {
    ElMessage.warning('请选择要删除的日志');
    return;
  }

  try {
    await ElMessageBox.confirm(
        `确定要删除选中的 ${selectedIds.value.length} 条日志吗？`,
        '提示',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning',
        }
    );

    const res = await batchDeleteLoginLog(selectedIds.value);
    if (res.data && res.data.code === 200) {
      ElMessage.success('批量删除成功');
      selectedIds.value = [];
      getList();
    } else {
      ElMessage.error(res.data?.msg || '批量删除失败');
    }
  } catch (error) {
    if (error !== 'cancel') {
      ElMessage.error('批量删除失败');
    }
  }
};

const handleExport = async () => {
  try {
    const res = await exportLoginLogExcel();
    const blob = new Blob([res.data], { type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet' });
    const url = window.URL.createObjectURL(blob);
    const link = document.createElement('a');
    link.href = url;
    link.download = `登录日志_${new Date().getTime()}.xlsx`;
    link.click();
    window.URL.revokeObjectURL(url);
    ElMessage.success('导出成功');
  } catch (error) {
    console.error('导出失败:', error);
    ElMessage.error('导出失败');
  }
};

onMounted(() => {
  getList();
});
</script>

<style scoped>
.loginlog-container {
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
  width: 250px;
}

.search-select {
  width: 150px;
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

:deep(.el-button--danger) {
  background: linear-gradient(135deg, #f5576c 0%, #f093fb 100%);
  border: none;
  border-radius: 10px;
  padding: 10px 24px;
  font-size: 14px;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(245, 87, 108, 0.4);
  transition: all 0.3s ease;
}

:deep(.el-button--danger:hover) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(245, 87, 108, 0.5);
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

:deep(.el-pagination) {
  display: flex;
  align-items: center;
}

:deep(.el-pagination.is-background .el-pager li:not(.is-disabled).is-active) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
}

:deep(.el-pagination.is-background .el-pager li:hover) {
  color: #667eea;
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
