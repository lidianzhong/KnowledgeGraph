import { request } from './index.js'
import qs from 'qs'

/*
    获取用户权限
    user_id: string
*/
export function getPermission(data) {
    return request({
        method: 'GET',
        url: '/permission/getUserPermission',
        params: data
    })
}

/*
    修改权限
    user_id: string
    permission_id: array
    is_allowed: array
*/
export function updatePermission(data) {
    return request({
        method: 'POST',
        url: '/permission/changePermission',
        data: qs.stringify(data)
    })
}

/*
    授予管理员权限
    user_id: string
*/
export function guardAdmin(data) {
    return request({
        method: 'POST',
        url: '/permission/grantAdmin',
        data: qs.stringify(data)
    })
}

/*
    注销用户
    user_id: string
*/
export function deleteUser(data) {
    return request({
        method: 'POST',
        url: '/permission/deleteUser',
        data: qs.stringify(data)
    })
}