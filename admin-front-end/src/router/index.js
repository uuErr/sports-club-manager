import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Home.vue'
import Cookies from 'js-cookie'
import Axios from "axios"
import {layer} from "@layui/layui-vue";
import NProgress from 'nprogress'
import 'nprogress/nprogress.css'

const Service = Axios.create({
  baseURL: "/admin/api",
  timeout: 2000,
  retry: 3
});

Service.interceptors.response.use(undefined, function axiosRetryInterceptor(err) {
  const config = err.config;
  if (config && config.retry) {
    config.__retryCount = config.__retryCount || 0;
    if (config.__retryCount >= config.retry) {
      return Promise.reject(err);
    }
    config.__retryCount += 1;
    const backoff = new Promise(function(resolve) {
      setTimeout(resolve, config.__retryCount * 1000);
    });
    return backoff.then(function() {
      return Service(config);
    });
  }
  return Promise.reject(err);
});

const routes = [
  { path: '',
    redirect: '/login'},
  {
    path: '/main',
    name: 'home',
    component: HomeView,
    meta:{title: "俱乐部管理后台"},
    children:[
      { path: '',
        redirect: '/main/inbox'},
      {
        path: '/main/inbox',
        component: () => import('@/views/Inbox.vue'),
        meta: {title: '俱乐部后台 · 首页'},
      },
      {
        path: '/main/user/',
        component: () => import('@/views/UserList.vue'),
        meta: {title: '俱乐部后台 · 账号管理', keepAlive: false},
      },
      {
        path: '/main/user/approve',
        component: () => import('@/views/UserReviewList.vue'),
        meta: {title: '俱乐部后台 · 账号审核'},
      },
      {
        path: '/main/user/credit',
        component: () => import('@/views/UserUnsignedList.vue'),
        meta: {title: '俱乐部后台 · 失信管理'},
      },
      {
        path: '/main/action/create',
        component: () => import('@/views/ActionCreate.vue'),
        meta: {title: '俱乐部后台 · 创建活动'},
      },
      {
        path: '/main/action',
        component: () => import('@/views/ActionList.vue'),
        meta: {title: '俱乐部后台 · 活动管理'},
      },
      {
        path: '/main/records',
        component: () => import('@/views/RecordsList.vue'),
        meta: {title: '俱乐部后台 · 报名记录'},
      },
      {
        path: '/main/records/worker',
        component: () => import('@/views/WorkRecordsList.vue'),
        meta: {title: '俱乐部后台 · 值班记录'},
      }
    ]
  },
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/Login.vue'),
    meta:{title: "俱乐部后台 · 登录"}
  },
  {
    path: '/:catchAll(.*)',
    name: '404',
    meta: {title: '页面不存在'},
    component: () => import('../views/404.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

router.beforeEach(async (to, from, next) => {
  NProgress.start();
  if(to.name !== '404') {
    if(to.name !== 'Login' && Cookies.get('token') === undefined) {
      if(from.name !== 'Login' && from.path !== '/'){
        layer.msg( "登录已失效，请重新登录");
      }
      next('/login');
    }
    if(Cookies.get('token') !== undefined){
      try{
        const response = await Service.post('/user/verify?token=' + Cookies.get('token'));
        if(response.status !== 200){
          layer.msg("账号状态已变化，请重新登录");
          Cookies.remove('token');
          next('/login');
        }
        if(response.data.status <= 0){
          layer.msg("账号状态已变化，请重新登录");
          Cookies.remove('token');
          next('/login');
        }
        if(to.name === 'Login' && response.data.status > 0)
          next('/main');
      }
      catch (error) {
        layer.msg("网络连接失败", {icon: 2});
        Cookies.remove('token');
        next('/login');
      }
    }
  }
  if (to.meta && to.meta.title) {
    document.title = to.meta.title;
  }
  next();
});

router.afterEach(() => {
  NProgress.done();
});

router.Axios = Service;
export default router
