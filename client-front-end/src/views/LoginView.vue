<template>
  <Vcode :show="isShow"
         slider-text="拖动滑块完成验证"
         fail-text="验证失败，请重试"
         success-text="验证通过"
         :range="5"
         @success="onSubmitLogin"
         @close="close"
  />
  <van-toast v-model:show="disabled" type="loading" overlay="true" duration="0"
             forbid_click="true" message="加载中…"></van-toast>
  <main class="club-auth">
    <div class="club-auth__cover">
      <p class="club-auth__brand">体育俱乐部</p>
      <a class="club-auth__credit" href="https://unsplash.com/photos/empty-indoor-badminton-courts-with-blue-flooring-AILEpOyczIk" target="_blank" rel="noopener noreferrer">球场摄影 · Palak Pitroda</a>
    </div>
    <div class="club-auth__main">
      <div class="club-auth__panel">
        <router-link class="club-auth__back" to="/inbox">← 返回</router-link>
        <h1 class="club-auth__heading">使用密码登录</h1>
        <van-form class="club-auth__form" @submit="onLogin">
          <div class="club-auth__label">
            <label for="member-username">用户名</label>
            <van-field
              id="member-username"
              v-model="username"
              class="club-auth__field"
              autocomplete="username"
              placeholder="请输入用户名"
              :rules="[{ required: true, message: '请输入用户名' }]"
            />
          </div>
          <div class="club-auth__label">
            <label for="member-password">密码</label>
            <van-field
              id="member-password"
              v-model="password"
              class="club-auth__field"
              type="password"
              autocomplete="current-password"
              placeholder="请输入密码"
              :rules="[{ required: true, message: '请输入密码' }]"
            />
          </div>
          <van-button class="club-auth__button club-auth__button--primary" :disabled="disabled" native-type="submit">登录</van-button>
        </van-form>
        <div class="club-auth__links">
          <router-link to="/findAccount">查询用户名</router-link>
          <router-link to="/resetPassword">重置密码</router-link>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import Cookies from "js-cookie";
import {showToast, showSuccessToast, showFailToast, showDialog  } from "vant";


export default {
  created(){
    const token = Cookies.get('token');
    if(token != null){
      this.$http.post('/user/verify?token='+ Cookies.get('token'))
          .then(response =>{
            if(response.data.status === 3)
              this.$router.push('/staff');
            else if(response.data.status > 0 && response.data.status < 3)
              this.$router.push('/main');
          }).
      catch(error =>{
      });
    }
  },
  data() {
    return {
      username: '',
      password: '',
      isShow: false,
      disabled: false,
      loading: false
    };
  },
  methods: {
    onLogin() {
      this.isShow = true;
    },
    onSubmitLogin(){
      this.isShow = false;
      this.disabled = true;
      this.$http({
        method: 'POST',
        url: `/user/login?username=${encodeURIComponent(this.username)}&password=${encodeURIComponent(this.password)}`,
      }).then((response) => {
        this.disabled = false;
        if(response.data.status === -2){
          showFailToast('用户名或密码错误');
          return;
        }
        if(response.data.status === -1){
          showFailToast('账号正在等待审核。');
          return;
        }
        if(response.data.status === 0){
          showFailToast('该账号已被停用，请联系客服。');
          return;
        }
        if(response.data.status > 3){
          showToast('这是管理员账号，请前往管理后台登录。');
          return;
        }
        Cookies.set('token', response.data.data);
        if(response.data.status === 3)
          this.$router.push('/staff');
        else
          this.$router.push('/main');
        if(response.data.status === 1){
          showDialog({
            title: '账号受限',
            message: '由于你多次报名后缺席，目前只能通过指定账号转让获得名额。活动报名、候补及接收非指定转让暂不可用。详情请联系客服。',
            confirmButtonText: '我知道了'
          }).then(() => {
            // on close
          });
        }else{
          showSuccessToast('登录成功');
        }
      }).catch((error) => {
            console.log(error);
            showFailToast('网络连接失败');
        this.disabled = false;
          }
      );
    },
    close(){
      this.isShow = false;
    }
  }
};
</script>
