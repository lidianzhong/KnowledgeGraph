import { request } from './index.js'


/*
    获取三元组数据
*/
export function getGraphData() {
    return request({
        method: 'GET',
        url: '/graph/getGraph',
    })
}

/*
    获取最新日志
*/
export function getLog() {
    return request({
        method: 'GET',
        url: '/log/getLatestLog',
    })
}

/*
    获取全部日志记录
*/
export function getAllLog() {
    return request({
        method: 'GET',
        url: '/log/getLogList',
    })
}