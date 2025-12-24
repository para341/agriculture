import axios from 'axios';
import { ElMessage } from 'element-plus';

// 创建axios实例
const service = axios.create({
    baseURL: 'http://localhost:8081/api',  // 后端接口前缀
    timeout: 5000,  // 请求超时时间
});

// 请求拦截器（添加token）
service.interceptors.request.use(
    (config) => {
        // 从本地存储获取token
        const token = localStorage.getItem('token');
        if (token) {
            config.headers['Authorization'] = token;  // 携带token到后端
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 响应拦截器（统一处理结果）
service.interceptors.response.use(
    (response) => {
        const res = response.data;
        // 后端返回失败（code=500）
        if (res.code !== 200) {
            ElMessage.error(res.msg || '请求失败');
            return Promise.reject(res);
        }
        // 成功
        return res;
    },
    (error) => {
        ElMessage.error(error.message || '服务器错误');
        return Promise.reject(error);
    }
);

export default service;