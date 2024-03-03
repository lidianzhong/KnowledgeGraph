import { request } from './index.js'
import qs from 'qs'

/*
    匹配近似问答对
    question: string
*/
export function search(data) {
    return request({
        method: 'POST',
        url: '/answer/getSimilarAnswer',
        data: qs.stringify(data),
    })
}

/*
    获取问答对列表
    page: string
    pageSize: string
*/
export function getAllAnswer(data) {
    return request({
        method: 'GET',
        url: '/answer/getAnswerList',
        params: data,
    })
}

/*
    删除问答对
    id: string
*/
export function deleteAnswer(data) {
    return request({
        method: 'POST',
        url: '/answer/deleteAnswer',
        data: qs.stringify(data),
    })
}


/*
    修改问答对
    id: string
    question: string
    answer: string
*/
export function updateAnswer(data) {
    return request({
        method: 'POST',
        url: '/answer/changeAnswer',
        data: qs.stringify(data),
    })
}