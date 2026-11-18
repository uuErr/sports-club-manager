<template>
  <van-toast v-model:show="loading" type="loading" overlay="true" duration="0"
             forbid_click="true" message="加載中..."></van-toast>
  <div>
    <QrScanner v-if="showQrCodeReader" @decode="onDecodeHandler" @close="qrReaderClose" />
  </div>
  <van-nav-bar
      title="核验并签到"
      left-text="返回"
      left-arrow
      fixed
      @click-left="onClickLeft"
      placeholder
  />

  <van-notice-bar left-icon="volume-o" color="#1989fa" background="#ecf9ff" v-if="!show_sign && !isLoading"
                  style="position: fixed; z-index: 1000; width: 100%">
    <van-swipe
        vertical
        class="notice-swipe"
        :autoplay="16000"
        :touchable="false"
        :show-indicators="false"
        ref="swipe"
    >
      <van-swipe-item>{{ notice_messgae }}，此结果仅用于核验该记录是否有效。</van-swipe-item>
      <van-swipe-item v-if="!this.show_sign && !this.signed">如遇特殊情况无法签到，可把截图发给管理员申请补签。</van-swipe-item>
    </van-swipe>
  </van-notice-bar>

  <br v-if="!show_sign && !isLoading"/>
  <br v-if="!show_sign && !isLoading"/>
  <div v-if="isLoading">
    <van-empty image="search" description="加载中…" />
  </div>
  <br/>
  <div v-if="!isLoading">
    <van-cell-group inset>
      <van-row justify="center" style="margin: 0px 0px 0px 0px;">
        <h4>{{actionInf.title}}&nbsp;</h4>
      </van-row>
      <van-row justify="center" style="margin: -22px 0px 0px 0px; font-size: 10pt; color: gray">
        <vue-qrcode :value="sign_code" :width="180"/>
      </van-row>
      <van-row justify="center" style="margin: 0px 0px 20px 0px; font-size: 8pt; font-weight: bold; color: gray">
        {{sign_code}}
      </van-row>
      <van-cell title="场地">{{actionInf.place}}</van-cell>
      <van-cell title="日期">{{actionInf.date}}</van-cell>
      <van-cell title="时间">{{actionInf.time_range}}</van-cell>
      <van-cell title="球拍">{{borrow ? 'Need' : '不需要'}}</van-cell>
      <van-cell title="状态" v-if="!this.show_sign">{{signed ? '已签到' : 'Unsigned'}}</van-cell>
      <van-cell v-if="!this.show_sign && !this.signed"></van-cell>
    </van-cell-group>
    <br/>
    <van-cell-group inset>
      <van-cell title="参与者信息"/>
      <van-cell title="姓名">{{memInf.name}}</van-cell>
      <van-cell title="学号">{{memInf.student_id}}</van-cell>
      <van-cell title="手机号">{{memInf.phone}}</van-cell>
      <van-cell title="邮箱" v-if="memInf.email !== ''">{{memInf.email}}</van-cell>
      <van-cell title="微信号">{{memInf.wechat_id}}</van-cell>
    </van-cell-group>
    <van-submit-bar
        v-if="show_sign"
        tip="Please check the information carefully to make sure it is correct, and then finish signing in!"
        tip-icon="info-o"
        placeholder>
      <template #button>
        <van-button icon="sign" round type="warning" @click="onSignClick">签到</van-button>
      </template>
    </van-submit-bar>
  </div>
  <br/>
</template>

<script>
import QrScanner from '@/components/QrScanner';
import VueQrcode from "@/main";
import Cookies from "js-cookie";
import {showFailToast, showSuccessToast, showToast, showDialog} from "vant";

export default {
  data(){
    return {
      isLoading: true,
      showQrCodeReader: false,
      sign_code: '',
      notice_messgae: '',
      memInf: {
        name: '加载中…',
        username: '加载中…',
        student_id: '加载中…',
        phone: '加载中…',
        email: '加载中…',
        wechat_id: '加载中…',
        state: 3
      },
      borrow: false,
      signed: false,
      loading: false,
      actionInf: {
        title: '加载中…',
        place:'加载中…',
        date: '加载中…',
        time_range: '加载中…'
      },
      show_sign: false
    };
  },
  components:{
    VueQrcode,
    QrScanner
  },
  created() {
    this.$staffVerify();
    this.showQrCodeReader = true;
  },
  methods:{
    qrReaderClose(){
      this.showQrCodeReader = false;
      this.$router.push({path:'/staff'});
    },
    onDecodeHandler(data){
      this.sign_code = data;
      this.showQrCodeReader = false;
      this.$http.post(`/staff/querySign?token=${Cookies.get('token')}&sign_code=${this.sign_code}`)
          .then(response => {
            if(response.status !== 200){
              this.$router.push({path:'/staff'});
              showFailToast("系统错误");
            }
            if(response.data.status < 0)
              this.$staffVerify();
            if(response.data.status === 0){
              this.$router.push({path:'/staff'});
              showFailToast("二维码信息无效");
            }
            else{
              this.actionInf = response.data.data.act_inf;
              this.memInf = response.data.data.mem_inf;
              this.borrow = response.data.data.borrow;
              this.signed = response.data.data.signed;
              if(response.data.status === 1){
                this.notice_messgae = "该二维码已完成签到";
                showDialog({
                  message: '该二维码已完成签到，本次扫码仅用于核验记录',
                  confirmButtonText: '确定'
                }).then(() => {
                  // on close
                });
              }
              if(response.data.status === 2){
                this.notice_messgae = "此活动由其他值班人员负责，你无权签到";
                showDialog({
                  message: '此活动由其他值班人员负责，你无权签到。本次扫码仅用于核验记录。',
                  confirmButtonText: '确定'
                }).then(() => {
                  // on close
                });
              }
              if(response.data.status === 3){
                this.notice_messgae = "该活动尚未开放签到。";
                showDialog({
                  message: '该活动尚未开放签到。本次扫码仅用于核验记录。',
                  confirmButtonText: '确定'
                }).then(() => {
                  // on close
                });
              }
              if(response.data.status === 4){
                this.notice_messgae = "活动已结束，无法签到";
                showDialog({
                  message: '活动已结束，无法签到。本次扫码仅用于核验记录。',
                  confirmButtonText: '确定'
                }).then(() => {
                  // on close
                });
              }
              if(response.data.status === 5){
                this.show_sign = true;
                showToast("请核对信息，确认无误后再签到。");
              }
              this.isLoading = false;
            }
          })
          .catch(error =>{
            console.log(error);
            this.$router.push({path:'/staff'});
            showFailToast("网络连接失败");
          });
      this.isLoading = false;
    },
    onClickLeft(){
      this.$router.push({path:'/staff'});
    },
    onSignClick(){
      this.loading = true;
      this.$http.post(`/staff/finishSign?token=${Cookies.get('token')}&sign_code=${this.sign_code}`)
          .then(response => {
            this.loading = false;
            if(response.status !== 200){
              this.$router.push({path:'/staff'});
              showFailToast("系统错误");
            }
            if(response.data.status < 0)
              this.$staffVerify();
            if(response.data.status === 0){
              this.$router.push({path:'/staff'});
              showFailToast("信息无效");
            }
            if(response.data.status === 1){
              this.$router.push({path:'/staff'});
              showFailToast("该二维码已完成签到。");
            }
            if(response.data.status === 2){
              this.$router.push({path:'/staff'});
              showFailToast("该二维码不属于当前活动。");
            }
            if(response.data.status === 3){
              this.$router.push({path:'/staff'});
              showFailToast("活动尚未开放签到。");
            }
            if(response.data.status === 4){
              this.$router.push({path:'/staff'});
              showFailToast("活动已结束，无法签到。");
            }
            if(response.data.status === 5){
              this.$router.push({path:'/staff'});
              showSuccessToast("签到成功");
            }
          })
          .catch(error => {
            this.loading = false;
            console.log(error);
            this.$router.push({path:'/staff'});
            showFailToast("网络连接失败");
          });
    }
  }
};
</script>
<style scoped>
.notice-swipe {
  height: 40px;
  line-height: 40px;
}
</style>


