import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

//保存状态
const state = {
    userinfo: JSON.parse(localStorage.getItem('USER') || '{}')
}
const getters = {
    getUser(state) {
        return state.userinfo.username
    },
    getIdentity(state) {
        return state.userinfo.role
    }
}
//实现方法
const mutations = {
    updateUser(state, data) {
        // 1. vuex做更新，使得有响应式
        state.userinfo = data
        // 2. localStorage做持久更新
        localStorage.setItem('USER', JSON.stringify(data))
    },
    // 清除用户信息
    clearUser(state) {
        state.userinfo = {}
        localStorage.removeItem('USER')
    }
}

export default new Vuex.Store({
    state,
    mutations,
    getters
})