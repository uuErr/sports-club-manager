<template>
  <van-toast v-model:show="loading" type="loading" overlay="true" duration="0"
             forbid_click="true" message="加载中…"></van-toast>
  <h1 class="club-page-title">转让与候补</h1>
  <van-tabs v-model:active="active" sticky offset-top="56" @change="onClickTab(name)" type="card" swipeable>
    <van-tab title="候补名单" name="1">
      <van-pull-refresh
          pulling-text="下拉刷新…"
          loosing-text="松开刷新…"
          loading-text="加载中…"
          success-text="刷新成功"
          v-model="waitingRefresh"
          @refresh="onWaitingRefresh">
        <br/>
      <div v-if="waitingList.length === 0">
        <van-empty description="暂无候补记录" />
      </div>
      <div class="club-card-grid">
      <div v-for="item in waitingList" :key="item.id">
        <van-cell-group inset class="club-detail-card">
          <van-cell title="活动">{{item.action_title}}</van-cell>
          <van-cell title="候补中">{{item.action_user}}</van-cell>
          <van-cell title="候补顺位">{{item.wait_rank}}</van-cell>
          <van-cell><van-button @click="onCancelClick(item.id)" type="danger" size="small" icon="cross" :disabled="buttonDisabled">退出候补</van-button></van-cell>
        </van-cell-group>
      </div>
      </div>
      </van-pull-refresh>
      <br/>
      <br/>
    </van-tab>
    <van-tab title="接收转让" name="2">
      <van-pull-refresh
          pulling-text="下拉刷新…"
          loosing-text="松开刷新…"
          loading-text="加载中…"
          success-text="刷新成功"
          v-model="transferRefresh"
          @refresh="onTransferRefresh">
      <br/>
        <div v-if="presentList.length === 0">
          <van-empty description="暂无可接收的转让" />
        </div>
      <div class="club-card-grid">
      <div v-for="item in presentList" :key="item.id">
        <van-cell-group inset class="club-detail-card">
          <van-cell title="活动名称">{{item.action_title}}</van-cell>
          <van-cell title="发起人">{{item.send_user}}</van-cell>
          <van-cell title="接收人">{{item.receive_user == '' ? '不限' : item.receive_user}}</van-cell>
          <van-cell>
            <van-button @click="onRefuseClick(item.id)" v-if="item.receive_user != ''" type="danger" size="small" icon="cross">拒绝</van-button>&nbsp
            <van-button @click="onAcceptClick(item.id)" type="success" size="small" icon="success">接受</van-button>
          </van-cell>
        </van-cell-group>
      </div>
      </div>
      </van-pull-refresh>
    </van-tab>
  </van-tabs>
</template>

<script>
import Cookies from "js-cookie";
import {showConfirmDialog, showFailToast, showSuccessToast} from "vant";

export default {
  data(){
    return {
      buttonDisabled: false,
      currentId: 0,
      active: 0,
      waitingRefresh: false,
      transferRefresh: false,
      loading: false,
      waitingList: [],
      presentList: []
    };
  },
  created(){
    this.loading = true;
    this.$memberVerify();
    this.onWaitingRefresh();
  },
  methods: {
    onClickTab(name){
      if(name === 1){
        this.loading = true;
        this.$memberVerify();
        this.onWaitingRefresh();
      }else{
        this.loading = true;
        this.$memberVerify();
        this.onTransferRefresh();
      }
    },
    onCancelClick(id){
      this.currentId = id;
      showConfirmDialog({
        title: '提示',
        confirmButtonText: '退出候补',
        cancelButtonText: '取消',
        message:
            '退出候补后，再次加入需要重新排队。确认退出吗？',
      }).then(() => {
        this.loading = true;
        this.buttonDisabled = true;
        this.$http.post('/waiting/waitDelete?token='+Cookies.get('token')
            +`&waiting_id=${this.currentId}`)
            .then(response => {
              this.loading = false;
              if(response.status !== 200){
                showFailToast("系统错误");
                this.buttonDisabled = false;
              }
              if(response.data.status === -2){
                this.$memberVerify();
              }
              if(response.data.status === -1){
                showFailToast("可能已加入候补，或活动已结束，请刷新页面查看。");
                this.onWaitingRefresh();
                this.buttonDisabled = false;
              }
              if(response.data.status === 0){
                showFailToast("用户信息与候补记录不符");
                this.onWaitingRefresh();
                this.buttonDisabled = false;
              }
              if(response.data.status === 1){
                showSuccessToast("已退出候补");
                this.onWaitingRefresh();
                this.buttonDisabled = false;
              }
            })
            .catch(error => {
              this.loading = false;
              console.log(error);
              showFailToast("网络连接失败");
              this.buttonDisabled = false;
            });
      }).catch(() => {});
    },
    onRefuseClick(id){
      this.currentId = id;
      showConfirmDialog({
        title: '提示',
        confirmButtonText: '拒绝',
        cancelButtonText: '取消',
        message:
            '拒绝后，对方需要重新发起转让。确认拒绝吗？',
      }).then(() => {
        this.loading = true;
        this.$http.post(`transfer/refuseTransfer?token=${Cookies.get('token')}&transfer_id=${this.currentId}`)
            .then(response => {
              this.loading = false;
              if(response.status !== 200){
                showFailToast("系统错误");
                this.buttonDisabled = false;
              }
              if(response.data.status === -2){
                this.$memberVerify();
              }
              if(response.data.status === -1){
                showFailToast("活动已开始或名额已被领取，转让已失效。页面将自动刷新。");
                this.onTransferRefresh();
                this.buttonDisabled = false;
              }
              if(response.data.status === 0){
                showFailToast("用户信息不匹配，请稍后再试。\n");
                this.buttonDisabled = false;
                this.onWaitingRefresh();
              }
              if(response.data.status === 1){
                showFailToast("已拒绝该名额转让");
                this.onTransferRefresh();
                this.buttonDisabled = false;
              }
            })
            .catch(error => {
              showFailToast("网络连接失败");
              this.loading = false;
              this.buttonDisabled = false;
            });
      }).catch(() => {});
    },
    onAcceptClick(id){
      this.loading = true;
      this.currentId = id;
      this.$http.post(`transfer/acceptTransfer?token=${Cookies.get('token')}&transfer_id=${this.currentId}`)
          .then(response => {
            this.loading = false;
            if(response.status !== 200){
              showFailToast("系统错误");
              this.buttonDisabled = false;
            }
            if(response.data.status === -2){
              this.$memberVerify();
            }
            if(response.data.status === -1){
              showFailToast("活动已开始或名额已被其他成员领取，转让已失效。\n");
              this.onTransferRefresh();
              this.buttonDisabled = false;
            }
            if(response.data.status === 0){
              showFailToast("当前账号受限，无法领取非指定转让名额。\n");
              this.onTransferRefresh();
              this.buttonDisabled = false;
            }
            if(response.data.status === 1){
              showFailToast("你已报名，不能通过领取转让名额重复报名。\n");
              this.buttonDisabled = false;
            }
            if(response.data.status === 2){
              showSuccessToast("名额领取成功，请在「报名记录」中查看，并准时参加活动。\n");
              this.onTransferRefresh();
              this.buttonDisabled = false;
            }
          })
          .catch(error => {
            showFailToast("网络连接失败");
            this.buttonDisabled = false;
          });
    },
    onWaitingRefresh(){
      this.waitingRefresh = true;
      this.$http.post('/waiting/queryWaiting?token='+Cookies.get('token'))
          .then(response => {
            this.loading = false;
            console.log(response);
            if(response.status === 200 && response.data.status > 0){}
              this.waitingList = response.data.data;
            this.waitingRefresh = false;
          })
          .catch(error =>{
            console.log(error);
            this.waitingRefresh = false;
          });
    },
    onTransferRefresh(){
      this.transferRefresh = true;
      this.$http.post('/transfer/queryTransfer?token='+Cookies.get('token'))
          .then(response => {
            this.loading = false;
            if(response.status === 200 && response.data.status > 0)
              this.presentList = response.data.data;
            this.transferRefresh = false;
          })
          .catch(error =>{
            console.log(error);
            this.loading = false;
            this.transferRefresh = false;
          });
    }
  }
}
</script>


<style scoped lang="scss">

</style>