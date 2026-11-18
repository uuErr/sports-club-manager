<template>
  <VCode :show="loginVCodeShow"
         slider-text="拖动滑块完成验证"
         fail-text="验证失败，请重试"
         success-text="验证通过"
         :range="5"
         @success="onSubmitLogin"
         @close="loginVCodeClose"
  />
  <main class="club-auth">
    <div class="club-auth__cover">
      <p class="club-auth__brand">体育俱乐部</p>
      <a class="club-auth__credit" href="https://unsplash.com/photos/empty-indoor-badminton-courts-with-blue-flooring-AILEpOyczIk" target="_blank" rel="noopener noreferrer">球场摄影 · Palak Pitroda</a>
    </div>
    <div class="club-auth__main">
      <div class="club-auth__panel">
        <h1 class="club-auth__heading">管理员登录</h1>
        <form class="club-auth__form" @submit.prevent="onLoginClick">
          <label class="club-auth__label">
            用户名
            <input class="club-auth__input" v-model="username" type="text" autocomplete="username" placeholder="请输入用户名" />
          </label>
          <label class="club-auth__label">
            密码
            <input class="club-auth__input" v-model="password" type="password" autocomplete="current-password" placeholder="请输入密码" />
          </label>
          <button class="club-auth__button club-auth__button--primary" type="submit" :disabled="disabled">登录</button>
        </form>
        <div class="club-auth__links">
          <button class="club-auth__text-button" type="button" @click="openFindAccount">查询账号</button>
          <button class="club-auth__text-button" type="button" @click="openResetPassword">重置密码</button>
        </div>
        <p class="club-auth__notice">会员请前往会员端登录。</p>
      </div>
    </div>
  </main>
</template>

<script>
import { layer } from "@layui/layui-vue";
import Cookies from 'js-cookie';

export default {
  data(){
    return{
      username: '',
      password: '',
      loginVCodeShow: false,
      disabled: false
    };
  },
  methods:{
    openFindAccount() {
      layer.open({
        type: "iframe",
        title: "查询账号",
        area: ['320pt','370pt'],
        content: this.$findUrl + "/adminFindAccount"
      })
    },
    openResetPassword() {
      layer.open({
        id: "reset-password",
        type: "iframe",
        title: "重置密码",
        area: ['320pt','400pt'],
        content: this.$findUrl +  "/adminResetPassword"
      })
    },
    onLoginClick(){
      if(this.username === '' || this.password === ''){
        layer.msg("请输入用户名和密码。", { icon : 7, time: 1500});
        return;
      }
      this.loginVCodeShow = true;
    },
    onSubmitLogin(){
      this.loginVCodeShow = false;
      this.disabled = true;
      this.$http({
        method: 'POST',
        url: `/user/login?username=${encodeURIComponent(this.username)}&password=${encodeURIComponent(this.password)}`,
      }).then((response) => {
        this.disabled = false;
        if(response.data.status === -2){
          layer.msg('用户名或密码错误。', { icon : 2, time: 1500});
          return;
        }
        if(response.data.status === -1){
          layer.msg('当前账号没有管理员权限', { icon : 7, time: 1500});
          return;
        }
        //Cookies.set('token', response.data.data);
        Cookies.set('token', response.data.data);
        this.$router.push('/main');
        layer.msg('登录成功', { icon : 1, time: 1500});
      }).catch((error) => {
            // console.log(error);
            layer.msg('网络连接失败', { icon : 2, time: 1500});
            this.disabled = false;
          }
      );
    },
    loginVCodeClose(){
      this.loginVCodeShow = false;
    }
  }
}
</script>

