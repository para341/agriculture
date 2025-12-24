import request from '@/utils/request'

export function getLoginLogPage(params: any) {
    return request({
        url: '/loginLog/page',
        method: 'get',
        params
    })
}

export function deleteLoginLog(id: number) {
    return request({
        url: `/loginLog/${id}`,
        method: 'delete'
    })
}

export function batchDeleteLoginLog(ids: number[]) {
    return request({
        url: '/loginLog/batch',
        method: 'delete',
        data: ids
    })
}

// 导出登录日志为Excel
export function exportLoginLogExcel() {
    return request({
        url: '/loginLog/export',
        method: 'get',
        responseType: 'blob'
    })
}
