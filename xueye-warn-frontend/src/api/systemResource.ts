import request from '@/utils/request'

export function getSystemResourceInfo() {
    return request({
        url: '/systemResource/info',
        method: 'get'
    })
}
