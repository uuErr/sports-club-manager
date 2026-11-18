<template>
  <VCode :show="verifyCodeShow"
         slider-text="拖动滑块完成验证"
         fail-text="验证失败，请重试"
         success-text="验证通过"
         :range="5"
         @success="onVerifyCodeSuccess"
         @close="onVerifyCodeClose"
         z-index="10000"
  />
  <lay-layer v-model="changePasswordShow" title="密码设置" :area="['500px', '320px']" z-index="1000">
    <div style="padding: 20px;">
      <lay-form :model="changeInf" required>
        <lay-form-item label="原密码" prop="password" label-width="130px">
          <lay-input v-model="changeInf.ori_pass" type="password">></lay-input>
        </lay-form-item>
        <lay-form-item label="新密码" prop="password" label-width="130px">
          <lay-input v-model="changeInf.new_pass" type="password">></lay-input>
        </lay-form-item>
        <lay-form-item label="确认密码" prop="password" label-width="130px">
          <lay-input v-model="changeInf.cfm_pass" type="password">></lay-input>
        </lay-form-item>
        <div style="text-align: right">
          <lay-button style="margin-top: 10px;" @click="this.changePasswordShow = false"><lay-icon type="layui-icon-close"/> 取消</lay-button>
          <lay-button type="primary" style="margin-top: 10px; " @click="onVerifyCodeCall(1)"><lay-icon type="layui-icon-release"/> 提交</lay-button>
        </div>
      </lay-form>
    </div>
  </lay-layer>

  <lay-layer v-model="updateContactShow" title="更新联系方式" :area="['500px', '375px']" z-index="1000">
    <div style="padding: 20px;">
      <lay-form :model="changeInf">
        <lay-form-item label="密码" prop="password" required>
          <lay-input v-model="changeInf.ori_pass" type="password">></lay-input>
        </lay-form-item>
        <lay-form-item label="手机号" prop="text" required>
          <lay-input v-model="changeInf.phone" type="test">></lay-input>
        </lay-form-item>
        <lay-form-item label="微信号" prop="text" required>
          <lay-input v-model="changeInf.wechat_id" type="text">></lay-input>
        </lay-form-item>
        <lay-form-item label="邮箱" prop="text">
          <lay-input v-model="changeInf.email" type="text">></lay-input>
        </lay-form-item>
        <div style="text-align: right">
          <lay-button style="margin-top: 10px;" @click="this.updateContactShow = false"><lay-icon type="layui-icon-close"/> 取消</lay-button>
          <lay-button type="primary" style="margin-top: 10px; " @click="onVerifyCodeCall(2)"><lay-icon type="layui-icon-release"/> 提交</lay-button>
        </div>
      </lay-form>
    </div>
  </lay-layer>

  <lay-layout class="admin-shell">
    <lay-header class="admin-header">
      <router-link class="admin-header__brand" to="/main/inbox">
        <lay-icon type="layui-icon-template"/> 体育俱乐部管理后台
      </router-link>
      <div class="admin-header__account">
        <span>{{ userInf.name }}</span>
        <lay-button size="sm" @click="onEventCall(2)">更新联系方式</lay-button>
        <lay-button size="sm" @click="onEventCall(1)">密码设置</lay-button>
        <lay-button size="sm" @click="logout">退出登录</lay-button>
      </div>
    </lay-header>
    <lay-layout class="admin-workspace">
      <lay-side class="admin-sidebar">
        <lay-menu v-model:selected-key="selectedKey" inverted v-model:openKeys="openKeys" :tree="true" @change-selected-key="onMenuClicked">
          <lay-menu-item id="1">
            <lay-icon type="layui-icon-home"/> 首页
          </lay-menu-item>
          <lay-sub-menu id="A">
            <template #title>
              <lay-icon type="layui-icon-username"/> 账号管理
            </template>
            <lay-menu-item id="2">
              <lay-icon type="layui-icon-user"/> 账号列表
            </lay-menu-item>
            <lay-menu-item id="3">
              <lay-icon type="layui-icon-vercode"/> 账号审核
            </lay-menu-item>
            <lay-menu-item id="4">
              <lay-icon type="layui-icon-face-cry"/> 失信管理
            </lay-menu-item>
          </lay-sub-menu>
          <lay-sub-menu id="B">
            <template #title>
              <lay-icon type="layui-icon-template"/> 活动
            </template>
            <lay-menu-item id="5">
              <lay-icon type="layui-icon-addition"/> 创建活动
            </lay-menu-item>
            <lay-menu-item id="6">
              <lay-icon type="layui-icon-app"/> 活动列表
            </lay-menu-item>
          </lay-sub-menu>
          <lay-sub-menu id="C">
            <template #title>
              <lay-icon type="layui-icon-template-one"/> 记录
            </template>
            <lay-menu-item id="7">
              <lay-icon type="layui-icon-form"/> 报名记录
            </lay-menu-item>
            <lay-menu-item id="8">
              <lay-icon type="layui-icon-log"/> 值班
            </lay-menu-item>
          </lay-sub-menu>
        </lay-menu>
      </lay-side>
      <lay-body class="admin-content">
        <router-view />
      </lay-body>
    </lay-layout>
  </lay-layout>
</template>

<script>
import Cookies from "js-cookie";
import { layer } from "@layui/layui-vue";

export default {
  setup(){
  },
  created() {
    this.$http.post('/user/verify?token='+Cookies.get('token'))
        .then(response => {
          this.userInf = response.data.data;
        })
        .catch(error =>{
          // console.log(error);
        });
    for(var i in this.route_inf){
      if(this.$route.path === this.route_inf[i].path || this.$route.path === this.route_inf[i].path + '/'){
        this.selectedKey = this.route_inf[i].id;
        return;
      }
    }
  },
  data(){
    return{
      isLevel: false,
      openKeys: [],
      selectedKey: [],
      verifyCodeShow: false,
      verifyEventId: 0,
      changePasswordShow: false,
      updateContactShow: false,
      changeInf:{
        ori_pass: '',
        new_pass: '',
        cfm_pass:'',
        phone: '',
        email: '',
        wechat_id: ''
      },
      userInf:{
      },
      route_inf:[
        {id:"1", path:"/main/inbox"},
        {id:"2", path:"/main/user"},
        {id:"3", path:"/main/user/approve"},
        {id:"4", path:"/main/user/credit"},
        {id:"5", path:"/main/action/create"},
        {id:"6", path:"/main/action"},
        {id:"7", path:"/main/records"},
        {id:"8", path:"/main/records/worker"},
      ]
    }
  },
  watch: {
    '$route'(to, from) {
      if(to.path !== from.path){
        for(var i in this.route_inf){
          if(to.path === this.route_inf[i].path || to.path === this.route_inf[i].path + '/'){
            this.selectedKey = this.route_inf[i].id;
            return;
          }
        }
      }
    }
  },
  methods:{
    logout(){
      this.$http.post('/user/logout?token='+Cookies.get('token')).then(function (a){}).catch(function(a){});
      Cookies.remove('token');
      layer.msg('退出成功', {time: 1500});
      this.$router.push('/login');
    },
    onMenuClicked(){
      for(var i in this.route_inf){
        if(this.selectedKey === this.route_inf[i].id){
          this.$router.push(this.route_inf[i].path);
          return;
        }
      }
    },
    onVerifyCodeSuccess(){
      this.verifyCodeShow = false;
      if(this.verifyEventId === 1){
        const pattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}/;
        if(pattern.test(this.changeInf.new_pass) === false){
          this.disabled = false;
          layer.msg("密码至少要有 8 个字符，并包含大写字母、小写字母、数字和特殊字符。",
              {icon:7, time: 1500});
          return;
        }
        const token = Cookies.get('token');
        this.$http.post(`/user/password?token=${token}&origin_pass=${encodeURIComponent(this.changeInf.ori_pass)}&new_pass=${encodeURIComponent(this.changeInf.new_pass)}`)
            .then(response =>{
              if(response.data.status <= 0){
                layer.msg('账号状态异常', {icon: 2, time: 1500});
              }
              if(response.data.status === 1){
                layer.msg('原密码错误。', {icon: 2, time: 1500});
              }
              if(response.data.status === 2){
                layer.msg('数据库异常', {icon: 2, time: 1500});
              }
              if(response.data.status === 3){
                layer.msg('修改成功', {icon: 1, time: 1500});
                this.changePasswordShow = false;
              }
            })
            .catch(error =>{
              // console.log(error);
              layer.msg('网络连接失败', {icon: 2, time: 1500});
            });
      }
      if(this.verifyEventId === 2){
        const token = Cookies.get('token');
        this.$http.post(`/user/contact?token=${token}&origin_pass=${encodeURIComponent(this.changeInf.ori_pass)}&email=${encodeURIComponent(this.changeInf.email)}&phone=${encodeURIComponent(this.changeInf.phone)}&wechat_id=${encodeURIComponent(this.changeInf.wechat_id)}`)
            .then(response =>{
              if(response.data.status <= 0){
                layer.msg('账号状态异常', {icon: 2, time: 1500});
              }
              if(response.data.status === 1){
                layer.msg('原密码错误。', {icon: 2, time: 1500});
              }
              if(response.data.status === 2){
                layer.msg('数据库异常', {icon: 2, time: 1500});
              }
              if(response.data.status === 3){
                layer.msg('更新成功', {icon: 1, time: 1500});
                this.userInf.wechat_id = this.changeInf.wechat_id;
                this.userInf.phone = this.changeInf.phone;
                this.userInf.email = this.changeInf.email;
                this.updateContactShow = false;
                setTimeout(() => {
                  this.$router.go(0);
                }, 1500);
              }
            })
            .catch(error =>{
              // console.log(error);
              layer.msg('网络连接失败', {icon: 2, time: 1500});
            });
      }
    },
    onVerifyCodeClose(){
      this.verifyCodeShow = false;
    },
    onVerifyCodeCall(id){
      this.verifyEventId = id;
      if(id === 1){
        if(this.changeInf.ori_pass === '' || this.changeInf.new_pass === '' || this.changeInf.cfm_pass === ''){
          layer.msg('请输入密码', {icon: 7, time: 1500});
          return;
        }
        if(this.changeInf.new_pass !== this.changeInf.cfm_pass){
          layer.msg('两次输入的密码不一致', {icon: 7, time: 1500});
          return;
        }
      }
      if(id === 2){
        if(this.changeInf.ori_pass === ''){
          layer.msg('请验证密码', {icon: 7, time: 1500});
          return;
        }
        if(this.changeInf.wechat_id === ''){
          layer.msg('请输入微信号', {icon: 7, time: 1500});
          return;
        }
        if(this.changeInf.phone === ''){
          layer.msg('请输入手机号', {icon: 7, time: 1500});
          return;
        }
      }
      this.verifyCodeShow = true;
    },
    onEventCall(value){
      if(value === 1){
        this.changeInf.ori_pass = '';
        this.changeInf.new_pass = '';
        this.changeInf.cfm_pass = '';
        this.changePasswordShow = true;
      }
      if(value === 2){
        this.changeInf.ori_pass = '';
        this.changeInf.phone = this.userInf.phone;
        this.changeInf.email = this.userInf.email;
        this.changeInf.wechat_id = this.userInf.wechat_id;
        this.updateContactShow = true;
      }
    }
  }
}
</script>
<style>
.admin-shell {
  height: 100vh;
  height: 100dvh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
  color: #132b24;
  background: #f2f6f3;
  --global-primary-color: #11684f;
}

.admin-shell .admin-header {
  z-index: 2;
  display: flex;
  flex: 0 0 auto;
  justify-content: space-between;
  align-items: center;
  gap: 12px 24px;
  width: 100%;
  height: auto;
  min-height: 64px;
  box-sizing: border-box;
  padding: 12px clamp(16px, 3vw, 32px);
  line-height: 1.4;
  color: #132b24;
  background: #fff;
  border-bottom: 1px solid #dce7df;
}

.admin-header__brand {
  display: flex;
  align-items: center;
  gap: 10px;
  color: inherit;
  font-size: 16px;
  font-weight: 750;
}

.admin-header__brand .layui-icon {
  display: grid;
  place-items: center;
  width: 32px;
  height: 32px;
  border-radius: 8px;
  background: #dff1e7;
  color: #11684f;
}

.admin-header__account {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  justify-content: flex-end;
  gap: 8px 12px;
  color: #52655c;
  font-size: 13px;
}

.admin-header__account .layui-btn {
  margin: 0;
  border-radius: 8px;
}

.admin-shell .admin-workspace {
  display: flex;
  flex: 1 1 0;
  flex-direction: row;
  min-height: 0;
  min-width: 0;
}

.admin-shell .admin-sidebar {
  position: relative;
  inset: auto;
  display: block;
  flex: 0 0 clamp(128px, 17vw, 206px);
  width: auto;
  height: auto;
  overflow-y: auto;
  box-sizing: border-box;
  padding: 12px 0;
  background: #112f26;
}

.admin-sidebar .layui-menu {
  width: 100%;
  background: transparent;
}

.admin-sidebar .layui-menu .layui-icon {
  margin-right: 6px;
}

.admin-shell .admin-content {
  position: relative;
  inset: auto;
  display: flex;
  flex: 1 1 0;
  width: 0;
  min-width: 0;
  height: auto;
  overflow: auto;
  background: #f2f6f3;
}

.admin-content .layui-table {
  font-variant-numeric: tabular-nums;
}

.admin-content .layui-btn {
  border-radius: 7px;
}

@media (max-width: 620px) {
  .admin-shell .admin-header {
    flex-wrap: wrap;
  }

  .admin-header__account {
    justify-content: flex-start;
  }
}
</style>
