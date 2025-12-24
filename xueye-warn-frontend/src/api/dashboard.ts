// src/api/dashboard.ts
import request from '@/utils/request' // 假设你项目有封装的axios请求工具（无则替换为原生axios）

// 1. 获取数据卡片统计
export function getDashboardCards() {
    return request({
        url: '/dashboard/cards',
        method: 'get'
    })
}

// 2. 获取专业分布饼图数据
export function getMajorDistribution() {
    return request({
        url: '/dashboard/majorDistribution',
        method: 'get'
    })
}

// 3. 获取各专业预警人数柱状图数据
export function getMajorWarningData() {
    return request({
        url: '/dashboard/majorWarning',
        method: 'get'
    })
}

// 4. 获取预警等级性别分布数据
export function getGenderWarningData() {
    return request({
        url: '/dashboard/genderWarning',
        method: 'get'
    })
}

// 5. 获取各专业平均绩点数据
export function getMajorAvgGrade() {
    return request({
        url: '/dashboard/majorAvgGrade',
        method: 'get'
    })
}