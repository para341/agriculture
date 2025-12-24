import request from '@/utils/request';
import type { User, ApiResponse } from './type';

export function getUserList(): Promise<any> {
    return request({
        url: '/user/list',
        method: 'get',
    }).then((res: any) => {
        if (res && typeof res === 'object') {
            if (res.code !== undefined && res.data !== undefined) {
                return res.data;
            } else if (Array.isArray(res)) {
                return res;
            }
        }
        return res;
    }).catch(error => {
        console.error('API调用失败:', error);
        throw error;
    });
}

export function addUser(user: Omit<User, 'id'>): Promise<any> {
    return request({
        url: '/user/add',
        method: 'post',
        data: user,
    });
}

export function updateUser(user: User): Promise<any> {
    return request({
        url: '/user/update',
        method: 'put',
        data: user,
    });
}

export function deleteUser(id: number): Promise<any> {
    return request({
        url: `/user/delete/${id}`,
        method: 'delete',
    });
}
