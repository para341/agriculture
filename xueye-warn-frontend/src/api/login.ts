import request from '@/utils/request';

// 登录接口 - 支持管理员和学生角色
export function login(data: { username: string; password: string; role: string }) {
    return request({
        url: '/login',
        method: 'post',
        data,
    });
}
