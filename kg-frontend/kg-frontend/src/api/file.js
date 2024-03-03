import { request } from './index.js'
import qs from 'qs'

/*
    上传文献
    title: string
    content: string
*/
export function uploadFile(data) {
    return request({
        method: 'POST',
        url: '/file/uploadFile',
        data: qs.stringify(data),
    })
}

/*
    查询所有文献
    page: string
    pageSize: string
*/
export function getAllFiles(data) {
    return request({
        method: 'GET',
        url: '/file/getAllFiles',
        params: data,
    })
}

/*
    查询单个文献详情
    document_id: string
*/
export function getFileDetail(data) {
    return request({
        method: 'GET',
        url: '/file/getFileDetail',
        params: data
    })
}

/*
    修改文献
    document_id: string
    title: string
    content: string
*/
export function updateFile(data) {
    return request({
        method: 'POST',
        url: '/file/changeFile',
        data: qs.stringify(data),
    })
}

/*
    删除文献
    document_id: string
*/
export function deleteFile(data) {
    return request({
        method: 'POST',
        url: '/file/deleteFile',
        data: qs.stringify(data),
    })
}

