<template>
  <div class="hadoop-container">
    <el-card>
      <h3>HDFS文件上传/下载</h3>
      <!-- 文件上传 -->
      <el-upload
          action="http://localhost:8081/api/hadoop/upload"
          :on-success="uploadSuccess"
          :on-error="uploadError"
          drag
          style="margin-bottom: 20px;"
      >
        <i class="el-icon-upload"></i>
        <div class="el-upload__text">将文件拖到此处，或<em>点击上传</em></div>
        <div class="el-upload__tip" slot="tip">只能上传csv/xlsx文件，且不超过10MB</div>
      </el-upload>

      <!-- 文件下载 -->
      <el-form :model="downloadForm" inline>
        <el-form-item label="文件名">
          <el-input v-model="downloadForm.fileName" placeholder="请输入HDFS中的文件名"></el-input>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="downloadFile">下载文件</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { reactive } from 'vue';
import { ElMessage } from 'element-plus';

// 下载表单
const downloadForm = reactive({
  fileName: '',
});

// 上传成功
const uploadSuccess = () => {
  ElMessage.success('文件上传成功');
};

// 上传失败
const uploadError = () => {
  ElMessage.error('文件上传失败');
};

// 下载文件
const downloadFile = () => {
  if (!downloadForm.fileName) {
    ElMessage.warning('请输入文件名');
    return;
  }
  // 跳转到下载接口
  window.open(`http://localhost:8081/api/hadoop/download?fileName=${downloadForm.fileName}`);
};
</script>

<style scoped>
.hadoop-container {
  padding: 30px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
  min-height: calc(100vh - 60px);
}

:deep(.el-card) {
  border-radius: 20px;
  border: none;
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

:deep(.el-card:hover) {
  box-shadow: 0 12px 35px rgba(102, 126, 234, 0.2);
}

:deep(.el-card__body) {
  padding: 35px;
}

:deep(.el-card h3) {
  margin: 0 0 30px 0;
  padding: 18px 25px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 12px;
  font-size: 20px;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
}

:deep(.el-upload-dragger) {
  border: 2px dashed #667eea;
  border-radius: 16px;
  background: linear-gradient(135deg, #f8f9ff 0%, #f0f4ff 100%);
  transition: all 0.3s ease;
  padding: 40px 20px;
}

:deep(.el-upload-dragger:hover) {
  border-color: #764ba2;
  background: linear-gradient(135deg, #f0f4ff 0%, #e8ecff 100%);
  box-shadow: 0 8px 25px rgba(102, 126, 234, 0.2);
}

:deep(.el-icon-upload) {
  font-size: 60px;
  color: #667eea;
  margin-bottom: 15px;
}

:deep(.el-upload__text) {
  color: #666;
  font-size: 16px;
}

:deep(.el-upload__text em) {
  color: #667eea;
  font-weight: 600;
  font-style: normal;
}

:deep(.el-upload__tip) {
  color: #999;
  font-size: 14px;
  margin-top: 10px;
}

:deep(.el-form-item__label) {
  color: #666;
  font-weight: 500;
}

:deep(.el-input__wrapper) {
  border-radius: 10px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.08);
  transition: all 0.3s ease;
}

:deep(.el-input__wrapper:hover) {
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.2);
}

:deep(.el-input__wrapper.is-focus) {
  box-shadow: 0 0 0 2px rgba(102, 126, 234, 0.2);
}

:deep(.el-button--primary) {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border: none;
  border-radius: 10px;
  padding: 12px 30px;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
  transition: all 0.3s ease;
}

:deep(.el-button--primary:hover) {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
}

:deep(.el-button--primary:active) {
  transform: translateY(0);
}
</style>