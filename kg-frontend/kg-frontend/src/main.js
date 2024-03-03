import Vue from 'vue';
import store from './store/index';
import ElementUI from 'element-ui';
import 'element-ui/lib/theme-chalk/index.css';
import App from './App.vue';
import router from './router';
import echarts from 'echarts';
import VueClipBoard from 'vue-clipboard2';


Vue.use(ElementUI);
Vue.use(VueClipBoard);

Vue.config.productionTip = false
Vue.prototype.$echarts = echarts

new Vue({
    router,
    store,
    render: h => h(App),
    beforeCreate() {//定义全局事件总线
        Vue.prototype.$bus = this
    }
}).$mount('#app')
