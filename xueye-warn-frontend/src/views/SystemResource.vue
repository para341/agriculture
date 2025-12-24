<template>
  <div class="system-resource-container">
    <el-card>
      <template #header>
        <div class="card-header">
          <span>系统资源监控</span>
          <el-button type="primary" @click="refreshData">
            <el-icon><Refresh /></el-icon>
            刷新
          </el-button>
        </div>
      </template>

      <el-row :gutter="20">
        <el-col :span="8">
          <el-card shadow="hover" class="info-card">
            <div class="info-title">操作系统</div>
            <div class="info-value">{{ resourceInfo.osName || '-' }}</div>
            <div class="info-sub">{{ resourceInfo.osVersion || '-' }}</div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card shadow="hover" class="info-card">
            <div class="info-title">CPU核心数</div>
            <div class="info-value">{{ resourceInfo.availableProcessors || '-' }}</div>
            <div class="info-sub">系统负载: {{ resourceInfo.systemLoadAverage?.toFixed(2) || '-' }}</div>
          </el-card>
        </el-col>
        <el-col :span="8">
          <el-card shadow="hover" class="info-card">
            <div class="info-title">线程数</div>
            <div class="info-value">{{ resourceInfo.threadCount || '-' }}</div>
            <div class="info-sub">活跃线程</div>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="20" style="margin-top: 20px;">
        <el-col :span="12">
          <el-card shadow="hover">
            <template #header>
              <div class="card-header">
                <span>内存使用情况</span>
              </div>
            </template>
            <div ref="memoryChartRef" style="height: 300px;"></div>
            <el-descriptions :column="2" border style="margin-top: 20px;">
              <el-descriptions-item label="总内存">{{ formatMemory(resourceInfo.totalMemory) }}</el-descriptions-item>
              <el-descriptions-item label="已用内存">{{ formatMemory(resourceInfo.usedMemory) }}</el-descriptions-item>
              <el-descriptions-item label="可用内存">{{ formatMemory(resourceInfo.freeMemory) }}</el-descriptions-item>
              <el-descriptions-item label="最大内存">{{ formatMemory(resourceInfo.maxMemory) }}</el-descriptions-item>
              <el-descriptions-item label="内存使用率" :span="2">
                <el-progress
                    :percentage="resourceInfo.memoryUsagePercent?.toFixed(1) || 0"
                    :color="getProgressColor(resourceInfo.memoryUsagePercent)"
                />
              </el-descriptions-item>
            </el-descriptions>
          </el-card>
        </el-col>
        <el-col :span="12">
          <el-card shadow="hover">
            <template #header>
              <div class="card-header">
                <span>JVM内存详情</span>
              </div>
            </template>
            <div ref="jvmMemoryChartRef" style="height: 300px;"></div>
            <el-descriptions :column="2" border style="margin-top: 20px;">
              <el-descriptions-item label="堆内存已用">{{ formatMemory(resourceInfo.heapMemoryUsed) }}</el-descriptions-item>
              <el-descriptions-item label="堆内存最大">{{ formatMemory(resourceInfo.heapMemoryMax) }}</el-descriptions-item>
              <el-descriptions-item label="非堆内存已用" :span="2">{{ formatMemory(resourceInfo.nonHeapMemoryUsed) }}</el-descriptions-item>
            </el-descriptions>
          </el-card>
        </el-col>
      </el-row>

      <el-row :gutter="20" style="margin-top: 20px;">
        <el-col :span="24">
          <el-card shadow="hover">
            <template #header>
              <div class="card-header">
                <span>GPU信息</span>
              </div>
            </template>
            <div v-if="resourceInfo.gpuAvailable && resourceInfo.gpuList && resourceInfo.gpuList.length > 0">
              <el-row :gutter="20">
                <el-col :span="12" v-for="(gpu, index) in resourceInfo.gpuList" :key="index">
                  <el-card shadow="hover" class="gpu-card">
                    <div class="gpu-header">
                      <el-tag type="success">GPU {{ gpu.index }}</el-tag>
                      <span class="gpu-name">{{ gpu.name }}</span>
                    </div>
                    <div class="gpu-info-grid">
                      <div class="gpu-info-item">
                        <div class="gpu-info-label">温度</div>
                        <div class="gpu-info-value" :style="{ color: getTemperatureColor(gpu.temperature) }">
                          {{ gpu.temperature }}°C
                        </div>
                      </div>
                      <div class="gpu-info-item">
                        <div class="gpu-info-label">GPU使用率</div>
                        <div class="gpu-info-value">
                          {{ gpu.gpuUtilization }}%
                          <el-progress
                              :percentage="gpu.gpuUtilization"
                              :color="getProgressColor(gpu.gpuUtilization)"
                              :show-text="false"
                              :stroke-width="4"
                          />
                        </div>
                      </div>
                      <div class="gpu-info-item">
                        <div class="gpu-info-label">显存使用率</div>
                        <div class="gpu-info-value">
                          {{ gpu.memoryUtilization }}%
                          <el-progress
                              :percentage="gpu.memoryUtilization"
                              :color="getProgressColor(gpu.memoryUtilization)"
                              :show-text="false"
                              :stroke-width="4"
                          />
                        </div>
                      </div>
                      <div class="gpu-info-item">
                        <div class="gpu-info-label">显存使用</div>
                        <div class="gpu-info-value">
                          {{ formatMemory(gpu.usedMemory) }} / {{ formatMemory(gpu.totalMemory) }}
                        </div>
                      </div>
                    </div>
                  </el-card>
                </el-col>
              </el-row>
            </div>
            <el-alert
                v-else
                :title="resourceInfo.gpuInfo || 'GPU信息不可用'"
                type="info"
                :closable="false"
                show-icon
            />
          </el-card>
        </el-col>
      </el-row>
    </el-card>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue';
import { ElMessage } from 'element-plus';
import { Refresh } from '@element-plus/icons-vue';
import { getSystemResourceInfo } from '@/api/systemResource';
import * as echarts from 'echarts';

const resourceInfo = ref<any>({});
const loading = ref(false);
const memoryChartRef = ref<HTMLDivElement>();
const jvmMemoryChartRef = ref<HTMLDivElement>();
let memoryChart: echarts.ECharts | null = null;
let jvmMemoryChart: echarts.ECharts | null = null;
let refreshTimer: number | null = null;

const formatMemory = (value: number) => {
  if (!value) return '-';
  return `${value.toFixed(2)} MB`;
};

const getProgressColor = (percentage: number) => {
  if (percentage < 50) return '#67c23a';
  if (percentage < 80) return '#e6a23c';
  return '#f56c6c';
};

const getTemperatureColor = (temperature: number) => {
  if (temperature < 60) return '#67c23a';
  if (temperature < 80) return '#e6a23c';
  return '#f56c6c';
};

const initMemoryChart = () => {
  if (!memoryChartRef.value) return;
  
  memoryChart = echarts.init(memoryChartRef.value);
  
  const option = {
    tooltip: {
      trigger: 'item',
      formatter: '{b}: {c} MB ({d}%)'
    },
    legend: {
      orient: 'vertical',
      left: 'left'
    },
    series: [
      {
        name: '内存使用',
        type: 'pie',
        radius: ['40%', '70%'],
        avoidLabelOverlap: false,
        itemStyle: {
          borderRadius: 10,
          borderColor: '#fff',
          borderWidth: 2
        },
        label: {
          show: false,
          position: 'center'
        },
        emphasis: {
          label: {
            show: true,
            fontSize: 20,
            fontWeight: 'bold'
          }
        },
        labelLine: {
          show: false
        },
        data: [
          { value: resourceInfo.value.usedMemory || 0, name: '已用内存', itemStyle: { color: '#f56c6c' } },
          { value: resourceInfo.value.freeMemory || 0, name: '可用内存', itemStyle: { color: '#67c23a' } }
        ]
      }
    ]
  };
  
  memoryChart.setOption(option);
};

const initJvmMemoryChart = () => {
  if (!jvmMemoryChartRef.value) return;
  
  jvmMemoryChart = echarts.init(jvmMemoryChartRef.value);
  
  const option = {
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'shadow'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ['堆内存', '非堆内存']
    },
    yAxis: {
      type: 'value',
      name: 'MB'
    },
    series: [
      {
        name: '内存使用',
        type: 'bar',
        data: [
          {
            value: resourceInfo.value.heapMemoryUsed || 0,
            itemStyle: { color: '#409eff' }
          },
          {
            value: resourceInfo.value.nonHeapMemoryUsed || 0,
            itemStyle: { color: '#67c23a' }
          }
        ],
        label: {
          show: true,
          position: 'top',
          formatter: '{c} MB'
        }
      }
    ]
  };
  
  jvmMemoryChart.setOption(option);
};

const updateCharts = () => {
  if (memoryChart) {
    memoryChart.setOption({
      series: [
        {
          data: [
            { value: resourceInfo.value.usedMemory || 0, name: '已用内存', itemStyle: { color: '#f56c6c' } },
            { value: resourceInfo.value.freeMemory || 0, name: '可用内存', itemStyle: { color: '#67c23a' } }
          ]
        }
      ]
    });
  }
  
  if (jvmMemoryChart) {
    jvmMemoryChart.setOption({
      series: [
        {
          data: [
            {
              value: resourceInfo.value.heapMemoryUsed || 0,
              itemStyle: { color: '#409eff' }
            },
            {
              value: resourceInfo.value.nonHeapMemoryUsed || 0,
              itemStyle: { color: '#67c23a' }
            }
          ]
        }
      ]
    });
  }
};

const refreshData = async () => {
  loading.value = true;
  try {
    const res: any = await getSystemResourceInfo();
    if (res && res.code === 200) {
      resourceInfo.value = res.data;
      updateCharts();
      ElMessage.success('数据刷新成功');
    } else {
      ElMessage.error('获取资源信息失败');
    }
  } catch (error) {
    console.error('获取资源信息异常:', error);
    ElMessage.error('获取资源信息失败');
  } finally {
    loading.value = false;
  }
};

onMounted(async () => {
  await refreshData();
  
  setTimeout(() => {
    initMemoryChart();
    initJvmMemoryChart();
  }, 100);
  
  refreshTimer = window.setInterval(() => {
    refreshData();
  }, 5000);
  
  window.addEventListener('resize', () => {
    memoryChart?.resize();
    jvmMemoryChart?.resize();
  });
});

onUnmounted(() => {
  if (refreshTimer) {
    clearInterval(refreshTimer);
  }
  memoryChart?.dispose();
  jvmMemoryChart?.dispose();
});
</script>

<style scoped>
.system-resource-container {
  padding: 20px;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.info-card {
  text-align: center;
  padding: 20px 0;
}

.info-title {
  font-size: 14px;
  color: #909399;
  margin-bottom: 10px;
}

.info-value {
  font-size: 28px;
  font-weight: bold;
  color: #303133;
  margin-bottom: 5px;
}

.info-sub {
  font-size: 12px;
  color: #909399;
}

.gpu-card {
  margin-bottom: 20px;
}

.gpu-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 15px;
}

.gpu-name {
  font-size: 16px;
  font-weight: bold;
  color: #303133;
}

.gpu-info-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 15px;
}

.gpu-info-item {
  padding: 10px;
  background-color: #f5f7fa;
  border-radius: 4px;
}

.gpu-info-label {
  font-size: 12px;
  color: #909399;
  margin-bottom: 5px;
}

.gpu-info-value {
  font-size: 18px;
  font-weight: bold;
  color: #303133;
}
</style>
