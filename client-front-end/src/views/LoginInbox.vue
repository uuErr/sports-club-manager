<template>
  <Vcode :show="isShow"
         slider-text="拖动滑块完成验证"
         fail-text="验证失败，请重试"
         success-text="验证通过"
         :range="5"
         @success="onSubmitLogin"
         @close="close"
  />
  <van-toast v-model:show="loading" type="loading" overlay="true" duration="0"
             forbid_click="true" message="加载中…"></van-toast>
  <main class="club-auth">
    <div class="club-auth__cover">
      <p class="club-auth__brand">体育俱乐部</p>
      <a class="club-auth__credit" href="https://unsplash.com/photos/empty-indoor-badminton-courts-with-blue-flooring-AILEpOyczIk" target="_blank" rel="noopener noreferrer">球场摄影 · Palak Pitroda</a>
    </div>
    <div class="club-auth__main">
      <div class="club-auth__panel">
        <h1 class="club-auth__heading">会员登录</h1>
        <div class="club-auth__actions">
          <van-button class="club-auth__button club-auth__button--primary" :disabled="disabled" @click="$router.push('/login')">使用密码登录</van-button>
          <van-button class="club-auth__button club-auth__button--secondary" :disabled="disabled" @click="onLogin">一键登录</van-button>
        </div>
        <div class="club-auth__links">
          <button class="club-auth__text-button" type="button" :disabled="disabled" @click="onRegister">注册新账号</button>
        </div>
      </div>
    </div>
  </main>
</template>

<script>
import Cookies from "js-cookie";
import {showToast, showSuccessToast, showFailToast, showDialog} from "vant";
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
      loading: false,
      time_call: new Date('2023-01-01T00:00:00Z')
    };
  },
  methods: {
    onLogin() {
      const now = new Date();
      if(Math.abs(now.getTime() - this.time_call.getTime()) < 5000){
        this.isShow = true;
      }
      else
        this.onSubmitLogin();
    },
    onRegister(){
      this.$router.push('/register');
    },
    async onSubmitLogin(){
      this.loading = true;
      this.time_call = new Date();
      console.log(this.$finger());
      this.isShow = false;
      this.disabled = true;
      this.username = await this.$finger();
      this.$http({
        method: 'POST',
        url: `/user/loginByEquip?equip_id=${encodeURIComponent(this.username)}`,
      }).then((response) => {
        this.disabled = false;
        if(response.data.status === -2){
          this.loading = false;
          showDialog({
                message: "此设备尚未启用一键登录。登录后可前往「我的账号 → 一键登录管理」设置。",
                confirmButtonText: '确定'
          });
          return;
        }
        if(response.data.status === -1){
          this.loading = false;
          showFailToast('账号正在等待审核。');
          return;
        }
        if(response.data.status === 0){
          this.loading = false;
          showFailToast('该账号已被停用，请联系客服。');
          return;
        }
        if(response.data.status > 3){
          this.loading = false;
          showToast('这是管理员账号，请前往管理后台登录。');
          return;
        }
        this.loading = false;
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
          this.loading = false;
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
