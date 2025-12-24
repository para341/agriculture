import request from '@/utils/request';
import type { Student, ApiResponse } from './type';

// 查询所有学生（修复版 - 正确处理AxiosResponse）
export function getStudentList(): Promise<any> {
    console.log('调用 getStudentList API...');
    return request({
        url: '/student/list',
        method: 'get',
    }).then((res: any) => {
        console.log('API原始响应:', res);

        // 检查响应格式
        if (res && typeof res === 'object') {
            // 如果是ApiResponse格式，返回data
            if (res.code !== undefined && res.data !== undefined) {
                return res.data;
            }
            // 如果直接返回数组，直接返回
            else if (Array.isArray(res)) {
                return res;
            }
        }

        // 默认返回原始数据
        return res;
    }).catch(error => {
        console.error('API调用失败:', error);
        throw error;
    });
}

// 添加学生
export function addStudent(student: Omit<Student, 'id'>): Promise<any> {
    return request({
        url: '/student/add',
        method: 'post',
        data: student,
    }); // ✅ 直接返回完整响应
}

// 修改学生
export function updateStudent(student: Student): Promise<any> {
    return request({
        url: '/student/update',
        method: 'put',
        data: student,
    });
}

// 删除学生
export function deleteStudent(id: number): Promise<any> {
    return request({
        url: `/student/delete/${id}`,
        method: 'delete',
    });
}
// 预警统计
export function getWarningStats(): Promise<any> {
    return request({
        url: '/student/stats',
        method: 'get',
    }).then((res: any) => res.data);
}

// src/api/student.ts

// 查询学生预警状态
export function getStudentWarningStatus(params: { studentId?: string; name?: string }) {
    return request({
        url: '/student/warning-status',
        method: 'get',
        params
    });
}

// 导出学生信息为Excel
export function exportStudentExcel() {
    return request({
        url: '/student/export',
        method: 'get',
        responseType: 'blob'
    });
}