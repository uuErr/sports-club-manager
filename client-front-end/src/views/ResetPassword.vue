<template>
  <van-toast v-model:show="disabled" type="loading" overlay="true" duration="0"
             forbid_click="true" message="加载中…"></van-toast>
  <Vcode :show="isShow"
         slider-text="拖动滑块完成验证"
         fail-text="验证失败，请重试"
         success-text="验证通过"
         :range="5"
         @success="onSubmitQuery"
         @close="close"
  />
  <van-nav-bar
      title="重置密码"
      left-text="返回"
      left-arrow
      fixed
      @click-left="onClickLeft"
      placeholder
      v-if="$route.path !== '/adminResetPassword'"
  />
  <van-steps :active="step" style="margin-top: 12pt; width: 60%; margin-left: 17.5%">
    <van-step>发送验证邮件</van-step>
    <van-step>重置密码</van-step>
  </van-steps>
  <br/>
  <div v-if="step === 0">
    <van-cell-group inset>
      <van-cell title="请填写以下信息以发送验证邮件"/>
      <van-field
          v-model="username"
          name="賬號"
          label="用户名"
          placeholder="请输入用户名"
      />
      <van-field
          v-model="student_name"
          name="真實姓名"
          label="姓名"
          placeholder="请输入真实姓名"
      />
      <van-field
          v-model="student_id"
          name="學號"
          label="学号"
          placeholder="请输入学号"
      />
      <van-cell center title="发送到校园邮箱">
        <template #right-icon>
          <van-switch v-model="useStudentEmail" />
        </template>
      </van-cell>
    </van-cell-group>
    <br/><br/>
    <van-button round block icon="envelop-o" style="width: 50%; margin-left: 25%" type="primary" @click="onSubmitCheck" :disabled="disabled">发送邮件</van-button>
    <center>
      <p style="font-size: 9pt" v-if="!useStudentEmail">
       无法使用登记的邮箱？ <a @click="this.useStudentEmail = true" style="cursor: pointer; text-decoration: underline">发送到校园邮箱</a>
      </p>
      <p style="font-size: 9pt" v-if="useStudentEmail">
        在校园里频繁登录不方便？ <a @click="this.useStudentEmail = false" style="cursor: pointer; text-decoration: underline">发送到登记邮箱</a>
      </p>
      <p style="font-size: 9pt; margin-top: -7pt">
        已收到验证邮件？ <a @click="this.step = 1" style="cursor: pointer; text-decoration: underline">点击直接重置密码</a>
      </p>
    </center>
  </div>
  <div v-if="step === 1">
    <van-cell-group inset>
      <van-cell title="请填写以下信息以重置密码"/>
      <van-field
          label-width="8em"
          v-model="verify_code"
          name="驗證碼"
          label="验证码"
          placeholder="请输入邮件中的验证码"
      />
      <van-field
          label-width="8em"
          v-model="password"
          name="重置密碼"
          label="重置密码"
          placeholder="请输入新密码"
          type="password"
      />
      <van-field
          label-width="9em"
          v-model="password_confirm"
          name="密碼確認"
          label="确认密码"
          placeholder="请再次输入密码"
          type="password"
      />
    </van-cell-group>
    <br/>
    <br/>
    <van-button round block icon="setting-o" style="width: 50%; margin-left: 25%" type="warning" @click="onCheckReset" :disabled="disabled">重置密码</van-button>
    <center>
      <p style="font-size: 9pt">没收到邮件，或者邮件已过期？ <a @click="this.step = 0" style="cursor: pointer; text-decoration: underline">返回上一步</a></p>
    </center>
  </div>

</template>

<script>
import {showToast, showSuccessToast, showFailToast, showConfirmDialog, showDialog} from 'vant';

export default {
  setup() {
    const getUrlKey = function (name) {
      return decodeURIComponent(
          (new RegExp('[?|&]'+name+'='+'([^&;]+?)(&|#|;|$)').exec(location.href)||[,""])[1].replace(/\+/g,'%20'))||null;
    }
    const onClickLeft = () => history.back();
    return {
      onClickLeft,
      getUrlKey
    };
  },
  data(){
    return {
      step: 0,
      student_name: '',
      student_id: '',
      username: '',
      verify_code: '',
      password: '',
      password_confirm: '',
      state: -2,
      account: '',
      isShow: false,
      disabled: false,
      useStudentEmail: false,
      loading: false,
      call: 0
    };
  },
  methods: {
    onSuccess(){
      if(this.step === 0)
        this.onSubmitQuery();
      if(this.step === 1)
        this.onSubmitReset();
    },
    onSubmitQuery() {
      this.isShow = false;
      this.disabled = true;
      if(this.useStudentEmail){
        this.sendToStudentEmail();
        return;
      }
      this.$http.post(`/find/sendResetEmail?student_id=${encodeURIComponent(this.student_id)}&name=${encodeURIComponent(this.student_name)}&username=${encodeURIComponent(this.username)}`, {}, {timeout: 10000})
          .then(response => {
            this.disabled = false;
            if(response.status !== 200){
              showFailToast("系统错误");
              return;
            }
            if(response.data.status === -2){
              showFailToast("账号信息填写有误");
              return;
            }
            if(response.data.status === -1){
              showToast("邮件已发送，请在两分钟后再试");
              this.verify_code = this.password = this.password_confirm = this.student_name = this.username = this.student_id = '';
              this.useStudentEmail = false;
              this.step = 1;
              return;
            }
            if(response.data.status === 0){
              showConfirmDialog({
                title: '注册邮箱有误',
                message:
                    '账号未登记邮箱或邮箱格式有误。你可以向校园邮箱发送验证码，也可以取消操作并联系客服重置密码。',
                confirmButtonText: '发送到校园邮箱',
                cancelButtonText: '取消'
              })
                  .then(() => {
                    this.sendToStudentEmail();
                  })
                  .catch(() => {
                    if(this.$route.path !== '/adminResetPassword')
                      this.$router.push('/inbox');
                    showDialog({
                      message: '已取消在线重置，请携带身份证复印件联系客服重置密码。',
                      confirmButtonText: '确定'
                    });
                  });
              //
              return;
            }
            showSuccessToast("邮件发送成功，请继续重置密码");
            this.verify_code = this.password = this.password_confirm = this.student_name = this.username = this.student_id = '';
            this.useStudentEmail = false;
            this.step = 1;
          }).catch(error => {
            this.disabled = false;
            showFailToast('网络连接失败');
          });
    },
    onSubmitCheck() {
      if (this.username.length === 0) {
        showToast({
          message: '请输入用户名',
          position: 'top',
        });
        return;
      }
      if (this.student_name.length === 0) {
        showToast({
          message: '请输入姓名',
          position: 'top',
        });
        return;
      }
      if (this.student_id.length === 0) {
        showToast({
          message: '请输入学号。',
          position: 'top',
        });
        return;
      }
      this.isShow = true;
    },
    onSubmitReset(){
      this.isShow = false;
      this.disabled = true;
      const pattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}/;
      if(pattern.test(this.password) === false){
        this.disabled = false;
        showToast("密码至少要有 8 个字符，并包含大写字母、小写字母、数字和特殊字符。");
        return;
      }
      this.$http.post(`/find/resetPassword?code=${encodeURIComponent(this.verify_code)}&password=${encodeURIComponent(this.password)}`)
          .then(response =>{
            this.disabled = false;
            if(response.status !== 200){
              showFailToast("系统错误");
              return;
            }
            if(response.data.status === -2){
              showFailToast("验证码错误");
              return;
            }
            if(response.data.status === -1){
              showFailToast("验证码已过期，请重新发送邮件。");
              this.step = 0;
              this.verify_code = this.password = this.password_confirm = this.student_name = this.username = this.student_id = '';
              this.useStudentEmail = false;
              return;
            }
            showSuccessToast("密码已重置，请妥善保管新密码。");
            if(this.$route.path !== '/adminResetPassword')
              this.$router.push("/login");
            this.step = 0;
            this.verify_code = this.password = this.password_confirm = this.student_name = this.username = this.student_id = '';
            this.useStudentEmail = false;
          }).
      catch(error =>{
        this.disabled = false;
        showFailToast('网络连接失败');
      });
    },
    onCheckReset(){
      if(this.verify_code.length === 0){
        showToast({
          message: '请输入验证码。',
          position: 'top',
        });
        return;
      }
      if(this.password.length === 0){
        showToast({
          message: '请输入新密码',
          position: 'top',
        });
        return;
      }
      if(this.password !== this.password_confirm){
        showToast({
          message: '两次输入的密码不一致。',
          position: 'top',
        });
        return;
      }
      this.isShow = true;
    },
    sendToStudentEmail(){
      this.isShow = false;
      this.disabled = true;
      this.$http.post(`/find/sendResetEmail?student_id=${encodeURIComponent(this.student_id)}&name=${encodeURIComponent(this.student_name)}&username=${encodeURIComponent(this.username)}&StudentEmail=1`, {}, {timeout: 10000})
          .then(response => {
            this.disabled = false;
            if(response.status !== 200){
              showFailToast("系统错误");
              return;
            }
            if(response.data.status === -2){
              showFailToast("账号信息填写有误");
              return;
            }
            if(response.data.status === -1){
              showToast("邮件已发送，请在两分钟后再试");
              this.verify_code = this.password = this.password_confirm = '';
              this.useStudentEmail = false;
              this.step = 1;
              return;
            }
            showSuccessToast("验证码已发送到校园邮箱，请继续重置密码。");
            this.verify_code = this.password = this.password_confirm = this.student_name = this.username = this.student_id = '';
            this.useStudentEmail = false;
            this.step = 1;
          }).catch(error => {
        this.disabled = false;
        showFailToast('网络连接失败');
      });
    }
  }
}
</script>

<style scoped lang="scss">

</style>