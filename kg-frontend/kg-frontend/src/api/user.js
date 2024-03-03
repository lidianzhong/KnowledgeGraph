import { request } from './index.js'
import qs from 'qs'

/*
    登录
    email: string
    password: string
*/
export function login(data) {
    return request({
        method: 'POST',
        url: '/user/login',
        data: qs.stringify(data),
    })
}

/*
    注册
    email: string
    password: string
    username: string
*/
export function register(data) {
    return request({
        method: 'POST',
        url: '/user/register',
        data: qs.stringify(data),
    })
}

/*
    注销
*/
export function layout() {
    return request({
        method: 'GET',
        url: '/user/deleteSelf',
    })
}

/*
    获取用户列表
    page: string
    pageSize: string
*/
export function getUserList(data) {
    return request({
        method: 'GET',
        url: '/user/getUserList',
        params: data
    })
}

/*
    发送验证码
    email: string
*/
export function sendCode(data) {
    return request({
        method: 'POST',
        url: '/user/getVerificationCode',
        data: qs.stringify(data)
    })
}