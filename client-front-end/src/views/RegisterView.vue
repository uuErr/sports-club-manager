<template>
  <div>
    <Vcode :show="isShow"
           slider-text="拖动滑块完成验证"
           fail-text="验证失败，请重试"
           success-text="验证通过"
           :range="5"
           @success="success"
           @close="close"
    />
  </div>
  <van-nav-bar
      title="注册新账号"
      left-text="返回"
      left-arrow
      fixed
      @click-left="onClickLeft"
  />
  <br/>
  <br/>
  <br/>
  <van-cell-group inset>
    <van-cell title="会员注册" label="欢迎注册！请填写以下信息，审核通过后即可报名参加俱乐部活动。" />
  </van-cell-group>
  <br/>
  <van-form @submit="onSubmit">
    <van-cell-group inset>
      <van-cell title="账号信息"/>
      <van-field
          v-model="username"
          name="賬號"
          label="用户名"
          placeholder="仅限字母和数字"
          :rules="[{ required: true, message: '请输入用户名' }]"
      />
      <van-field
          v-model="password"
          type="password"
          name="密碼"
          label="密码"
          placeholder="设置密码"
          :rules="[{ required: true, message: '请输入密码' }]"
      />
      <van-field
          v-model="password_confirm"
          type="password"
          name="密碼"
          label="确认"
          placeholder="请再次输入密码"
          :rules="[{ required: true, message: '请再次输入密码' }]"
      />
    </van-cell-group>
    <br/>
    <van-cell-group inset>
      <van-cell title="个人信息"/>
      <van-field
          v-model="student_name"
          name="Name"
          label="姓名"
          placeholder="证件上的姓名"
          :rules="[{ required: true, message: '请输入姓名' }]"
      />
      <van-field
          v-model="student_id"
          name="Student ID"
          label="学号"
          placeholder="填写学生证上的学号"
          :rules="[{ required: true, message: '请输入学号' }]"
      />
      <van-field
          v-model="member_id"
          name="會員卡號"
          label="会员编号"
          placeholder="填写会员卡上的编号"
          :rules="[{ required: true, message: '请输入会员编号' }]"
      />
    </van-cell-group>
    <br/>
    <van-cell-group inset>
      <van-cell title="联系方式"/>
      <van-field
          v-model="phone"
          type="tel"
          name="Phone"
          label="手机号"
          placeholder="请输入区号（如 +86、+853）"
          :rules="[{ required: true, message: '请输入手机号' }]"
      />
      <van-field
          v-model="wechat_id"
          name="Wechat ID"
          label="微信号"
          placeholder="用于日常活动联系"
          :rules="[{ required: true, message: '请输入微信号' }]"
      />
      <van-field
          v-model="email"
          name="Email"
          label="邮箱"
          placeholder="可留空"
      />
    </van-cell-group>
    <br/>
    <van-row justify="center">
      <van-space :size="20">
        <van-button round block type="warning" :disabled="disabled" native-type="submit" icon="guide-o" >
          提交注册
        </van-button>
        <van-button round block type="default" :disabled="disabled" icon="replay" @click="onRewrite">
          重填
        </van-button>
      </van-space>
    </van-row>
  </van-form>
  <br/>
</template>

<script>
import {showFailToast, showSuccessToast, showToast, Toast} from 'vant';
export default {
  setup() {
    const onClickLeft = () => history.back();
    return {
      onClickLeft,
    };
  },
  data() {
    return{
      username: '',
      password: '',
      password_confirm: '',
      student_name: '',
      student_id:'',
      member_id:'',
      phone:'',
      email:'',
      wechat_id:'',
      isShow: false,
      disabled: false
    };
  },
  methods: {
    onSubmit(){
      if(this.password !== this.password_confirm){
        this.password = this.password_confirm = "";
        showFailToast("两次输入的密码不一致，请重新输入。\n");
        return;
      }
      this.isShow = true;
    },
    onRewrite(){
      this.username = '';
      this.password = '';
      this.password_confirm = '';
      this.student_name = '';
      this.member_id = '';
      this.student_id = '';
      this.wechat_id = '';
      this.phone = '';
      this.email = '';
    },
    success() {
      this.disabled = true;
      const pattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}/;
      if(pattern.test(this.password) === false){
        this.disabled = false;
        showToast("密码至少要有 8 个字符，并包含大写字母、小写字母、数字和特殊字符。");
        this.isShow = false;
        return;
      }
      this.$http.post(`/user/register?username=${encodeURIComponent(this.username)}&password=${encodeURIComponent(this.password)}&name=${encodeURIComponent(this.student_name)}&card_id=${encodeURIComponent(this.member_id)}&phone=${encodeURIComponent(this.phone)}&wechat_id=${encodeURIComponent(this.wechat_id)}
&student_id=${encodeURIComponent(this.student_id)}&email=${encodeURIComponent(this.email)}`)
          .then(data => {
            console.log(data);
            if(data.status !== 200){
              showFailToast("系统错误");
            }
            if(data.data.status === -1){
              showFailToast(data.data.data);
              this.password = this.password_confirm = '';
            }
            if(data.data.status === 0){
              showSuccessToast(data.data.data);
              this.$router.push("/login");
            }
            this.disabled = false;
          })
          .catch(error =>{
            showFailToast("网络连接失败");
            this.disabled = false;
          });
      this.isShow = false; // 通过验证后，需要手动隐藏模态框
    },
    close() {
      this.isShow = false;
    }
  }
};
</script>