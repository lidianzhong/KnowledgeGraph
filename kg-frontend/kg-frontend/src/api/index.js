import axios from 'axios'

let vm = null
export function setThis(that) {
    vm = that
}

export function request(config) {
    const instance = axios.create({
        baseURL: 'http://localhost:8081/',
        timeout: 50000,
    })

    // 后端验证token，有token(未登录)去验证，没token直接越过
    //请求拦截器
    instance.interceptors.request.use(config => {
        const userinfo = localStorage.getItem('USER')
        if (userinfo) config.headers.Authorization = JSON.parse(userinfo).token
        return config
    })

    //响应拦截器
    instance.interceptors.response.use(
        res => {
            console.log(res)
            switch (res.status) {
                case 200: return res; break;
                case 201: vm.$message.error('请输入完整数据'); break;
                case 202: vm.$message.error('账号或用户名已存在'); break;
                case 203: vm.$message.error('请求出错'); break;
                case 204: vm.$message.error('数据不存在'); break;
                case 205: vm.$message.error('用户不存在'); break;
                case 206: vm.$message.error('您无权限此操作'); break;
                case 209: vm.$message.error('没有身份信息'); break;
                case 210: vm.$message.error('登录已过期，请重新登录');
                    localStorage.removeItem('USER')
                    vm.$store.commit("clearUser")
                    window.location.href = '/login'
                    break;
                case 211: vm.$message.error('密码错误'); break;
                case 212: vm.$message.error('管理员无法注销'); break;
                case 216: vm.$message.error('验证码错误'); break;
                case 300: vm.$message.error('您无权限此操作'); break;
                case 320: vm.$message.error('文献不存在'); break;
                case 404: vm.$message.error('页码不存在'); break;
            }
        },
        err => {
            console.log(err)
        }
    )
    return instance(config)
}


