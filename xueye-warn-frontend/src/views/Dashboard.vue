<template>
  <div class="dashboard-container">
    <!-- 顶部数据卡片区（基于现有表字段） -->
    <el-row :gutter="20" style="margin-bottom: 20px;">
      <el-col :span="6">
        <el-card shadow="hover" class="card-item">
          <div class="card-icon"><el-icon><User /></el-icon></div>
          <div class="card-info">
            <div class="card-title">学生总数</div>
            <div class="card-value">{{ cardData.studentCount }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="card-item">
          <div class="card-icon"><el-icon><School /></el-icon></div>
          <div class="card-info">
            <div class="card-title">专业个数</div>
            <div class="card-value">{{ cardData.majorCount }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="card-item">
          <div class="card-icon"><el-icon><Check /></el-icon></div>
          <div class="card-info">
            <div class="card-title">正常人数</div>
            <div class="card-value">{{ cardData.normalCount }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="card-item">
          <div class="card-icon"><el-icon><Warning /></el-icon></div>
          <div class="card-info">
            <div class="card-title">预警人数</div>
            <div class="card-value">{{ cardData.warningCount }}</div>
          </div>
        </el-card>
      </el-col>
      <el-col :span="6">
        <el-card shadow="hover" class="card-item">
          <div class="card-icon"><el-icon><Close /></el-icon></div>
          <div class="card-info">
            <div class="card-title">严重预警人数</div>
            <div class="card-value">{{ cardData.severeCount }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 中间主图表：专业分布饼图 -->
    <el-card style="margin-bottom: 20px;">
      <h3>专业分布</h3>
      <div ref="majorPieChartRef" style="width: 100%; height: 300px;"></div>
    </el-card>

    <!-- 下方多图表区 -->
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card>
          <h3>各专业预警人数</h3>
          <div ref="majorBarChartRef" style="width: 100%; height: 250px;"></div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card>
          <h3>预警等级性别分布</h3>
          <div ref="genderChartRef" style="width: 100%; height: 250px;"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 专业平均绩点图表 -->
    <el-card style="margin-top: 20px;">
      <h3>各专业平均绩点</h3>
      <div ref="majorAvgGradeChartRef" style="width: 100%; height: 300px;"></div>
    </el-card>

    <div class="page-footer">
      <a href="https://github.com/para341/school" target="_blank" class="github-link">
        GitHub: https://github.com/para341/school
      </a>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue';
import * as echarts from 'echarts';
import { User, School, Check, Warning, Close } from '@element-plus/icons-vue';
import { getDashboardCards, getMajorDistribution, getMajorWarningData, getGenderWarningData, getMajorAvgGrade } from '@/api/dashboard';


// 数据卡片数据
const cardData = reactive({
  studentCount: 0,
  majorCount: 0,
  normalCount: 0,
  warningCount: 0,
  severeCount: 0 // 新增严重预警人数
});

// 图表容器引用
const majorPieChartRef = ref<any>(null);
const majorBarChartRef = ref<any>(null);
const genderChartRef = ref<any>(null);
const majorAvgGradeChartRef = ref<any>(null);


const initCards = async () => {
  try {
    const res = await getDashboardCards();
    console.log('Dashboard cards response:', res); // 添加调试日志
    console.log('Dashboard cards data:', res.data); // 添加调试日志
    Object.assign(cardData, res.data);
  } catch (error) {
    console.error('获取数据卡片失败：', error);
  }
};


// 2. 初始化"专业分布"饼图
const initMajorPieChart = async () => {
  try {
    const res = await getMajorDistribution();
    const chart = echarts.init(majorPieChartRef.value);
    chart.setOption({
      series: [{
        type: 'pie',
        radius: ['40%', '70%'],
        data: res.data.majorNames.map((name: string, i: number) => ({
          name, value: res.data.counts[i]
        })),
        label: { show: true, formatter: '{b}: {c}' }
      }]
    });
    // 适配窗口大小变化
    window.addEventListener('resize', () => chart.resize());
  } catch (error) {
    console.error('初始化专业分布饼图失败：', error);
  }
};

// 3. 初始化"各专业预警人数"柱状图
const initMajorBarChart = async () => {
  try {
    const res = await getMajorWarningData();
    const chart = echarts.init(majorBarChartRef.value);
    chart.setOption({
      legend: { data: ['正常', '预警', '严重'] }, // 添加严重预警
      xAxis: { type: 'category', data: res.data.majors },
      yAxis: { type: 'value' },
      series: [
        { name: '正常', type: 'bar', data: res.data.normalList, itemStyle: { color: '#67C23A' } },
        { name: '预警', type: 'bar', data: res.data.warningList, itemStyle: { color: '#E6A23C' } },
        { name: '严重', type: 'bar', data: res.data.severeList, itemStyle: { color: '#F56C6C' } } // 新增严重预警系列
      ]
    });
    window.addEventListener('resize', () => chart.resize());
  } catch (error) {
    console.error('初始化各专业预警人数柱状图失败：', error);
  }
};

// 4. 初始化"预警等级性别分布"图表
const initGenderChart = async () => {
  try {
    const res = await getGenderWarningData();
    const chart = echarts.init(genderChartRef.value);
    chart.setOption({
      legend: { data: ['男', '女'] },
      xAxis: { type: 'category', data: ['正常', '预警', '严重'] },
      yAxis: { type: 'value' },
      series: [
        { name: '男', type: 'bar', data: res.data.maleData, itemStyle: { color: '#409EFF' } },
        { name: '女', type: 'bar', data: res.data.femaleData, itemStyle: { color: '#F56C6C' } }
      ]
    });
    window.addEventListener('resize', () => chart.resize());
  } catch (error) {
    console.error('初始化预警等级性别分布图表失败：', error);
  }
};

// 5. 初始化"各专业平均绩点"图表
const initMajorAvgGradeChart = async () => {
  try {
    const res = await getMajorAvgGrade();
    const chart = echarts.init(majorAvgGradeChartRef.value);
    chart.setOption({
      tooltip: {
        trigger: 'axis',
        formatter: '{b}: {c}'
      },
      xAxis: {
        type: 'category',
        data: res.data.majors,
        axisLabel: {
          rotate: 30
        }
      },
      yAxis: {
        type: 'value',
        name: '平均绩点'
      },
      series: [{
        name: '平均绩点',
        type: 'bar',
        data: res.data.avgGrades.map((grade: number) => grade.toFixed(2)),
        itemStyle: {
          color: function(params: any) {
            const grade = res.data.avgGrades[params.dataIndex];
            if (grade >= 70) return '#67C23A';
            if (grade >= 60) return '#E6A23C';
            return '#F56C6C';
          }
        },
        label: {
          show: true,
          position: 'top',
          formatter: '{c}'
        }
      }]
    });
    window.addEventListener('resize', () => chart.resize());
  } catch (error) {
    console.error('初始化各专业平均绩点图表失败：', error);
  }
};

// 页面加载时初始化
onMounted(async () => {
  await initCards();
  await initMajorPieChart();
  await initMajorBarChart();
  await initGenderChart();
  await initMajorAvgGradeChart();
});
</script>

<style scoped>
.dashboard-container {
  padding: 30px;
  background: linear-gradient(135deg, #f5f7fa 0%, #e8ecf1 100%);
  min-height: calc(100vh - 60px);
}

.card-item {
  display: flex;
  align-items: center;
  padding: 25px 20px;
  border-radius: 20px;
  transition: all 0.4s ease;
  cursor: pointer;
  border: none;
}

.card-item:hover {
  transform: translateY(-8px);
  box-shadow: 0 15px 40px rgba(102, 126, 234, 0.25);
}

.card-icon {
  font-size: 28px;
  margin-right: 20px;
  width: 60px;
  height: 60px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  box-shadow: 0 8px 20px rgba(102, 126, 234, 0.3);
  transition: all 0.3s ease;
}

.card-item:hover .card-icon {
  transform: scale(1.1) rotate(5deg);
  box-shadow: 0 12px 30px rgba(102, 126, 234, 0.5);
}

.card-title {
  font-size: 15px;
  color: #666;
  font-weight: 500;
  margin-bottom: 5px;
}

.card-value {
  font-size: 28px;
  font-weight: 700;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
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
  padding: 25px;
}

:deep(.el-card h3) {
  margin: 0 0 20px 0;
  padding: 15px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: #fff;
  border-radius: 12px;
  font-size: 18px;
  font-weight: 600;
  box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
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
