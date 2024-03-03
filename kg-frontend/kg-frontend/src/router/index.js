import Vue from 'vue'
import VueRouter from 'vue-router'


const originPush = VueRouter.prototype.push
const originReplace = VueRouter.prototype.replace
VueRouter.prototype.push = function (location, resolve, reject) {
    if (resolve && reject) {
        originPush.call(this, location, resolve, reject);
    } else {
        originPush.call(this, location, () => { }, () => { });
    }
}

VueRouter.prototype.replace = function (location, resolve, reject) {
    if (resolve && reject) {
        originReplace.call(this, location, resolve, reject)
    } else {
        originReplace.call(this, location, () => { }, () => { })
    }
}

Vue.use(VueRouter)

const routes = [
    {
        path: '/',
        redirect: '/login'
    },
    {
        path: '/main',
        redirect: '/main/upload',
    },
    {
        path: '/main',
        name: 'Main',
        component: () => import('views/main/Main.vue'),
        children: [
            {
                path: 'upload',
                name: 'Upload',
                component: () => import('views/main/upload/UploadFile.vue'),
            },
            {
                path: 'graph',
                name: 'Graph',
                component: () => import('views/main/graph/Graph.vue'),
            },
            {
                path: 'answer',
                name: 'Answer',
                component: () => import('views/main/answer/Answer.vue'),
            },
        ]
    },
    {
        path: '/login',
        name: 'Login',
        component: () => import('components/Login.vue')
    },
    {
        path: '/changeFile',
        name: 'ChangeFile',
        component: () => import('views/main/upload//ChangeFile.vue')
    }
]

const router = new VueRouter({
    routes,
    mode: 'history'
})
const route = {
    path: "management",
    name: "Management",
    component: () => import("views/main/management/Management.vue")
}
// 导航守卫
router.beforeEach((to, from, next) => {
    //刷新页面时，重新添加路由
    if (to.name == null) {
        router.addRoute('Main', route)
        next({ ...to, replace: true });
    }
    if (to.path == ('/login')) {
        if (localStorage.getItem('USER')) {
            next({ path: '/main' })
        }
        else next()
    } else {
        if (!localStorage.getItem('USER')) {
            next({ path: '/login' })
        } else {
            next()
        }
    }
})

export default router