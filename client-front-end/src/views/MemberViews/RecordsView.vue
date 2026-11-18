<template>
  <van-toast v-model:show="loading" type="loading" overlay="true" duration="0"
             forbid_click="true" message="加载中…"></van-toast>
  <Vcode :show="isShow"
         slider-text="拖动滑块完成验证"
         fail-text="验证失败，请重试"
         success-text="验证通过"
         :range="5"
         @success="send_transfor"
         @close="close"
  />
  <van-action-sheet v-model:show="transfor_show" title="发起转让" z-index="100">
    <van-cell-group>
      <van-cell title="转让说明" label="报名截止后，如果无法参加活动，可以转让名额。发起后无法撤回，对方接受后，名额会从你的账号转到对方账号。填写接收者的完整用户名，对方可以在「转让与候补」中查看。留空时，任何未被封禁的用户（包括你本人）都可以接受。"/>
      <van-field
          v-model="username"
          name="username"
          label="用户名"
          placeholder="接收人账号"
      />
      <br/>
      <van-row justify="center">
        <van-button round block type="success" @click="send_transfor_first" icon="guide-o" style="width: 200px">
          发起转让
        </van-button>
      </van-row>
      <br/>
    </van-cell-group>
  </van-action-sheet>
  <van-action-sheet v-model:show="wechat_show" title="加入微信群" z-index="100">
    <van-cell-group>
      <van-cell title="提示">
        <template #label>
          请使用登记的微信号 {{ wechat_id }} 扫描二维码入群。微信号变更后，请在「我的账号」更新联系方式。
        </template>
      </van-cell>
      <van-row justify="center" style="margin: 0px 0px 0px 0px; font-size: 10pt; color: gray">
        <vue-qrcode :value="wechat_url" :width="300"/>
      </van-row>
      <van-row justify="center" style="margin: 0px 0px 0px 0px; font-size: 8pt; color: gray">
        长按二维码加入群聊，仅限账号本人使用。
      </van-row>
      <br/>
    </van-cell-group>
  </van-action-sheet>
  <h1 class="club-page-title">报名记录</h1>
  <van-pull-refresh
      pulling-text="下拉刷新…"
      loosing-text="松开刷新…"
      loading-text="加载中…"
      success-text="刷新成功"
      v-model="isLoading"
      @refresh="onRefresh"
  >
    <div v-if="recordList.length === 0">
      <van-empty description="暂无参与记录" />
    </div>
    <div class="club-card-grid">
      <div v-for="item in recordList" :key="item.id">
        <van-cell-group inset class="club-detail-card">
          <van-row justify="center" style="margin: 10px 0px 0px 0px;">
            <van-image
                width="90"
                height="90"
                :src="require('@/assets/badminton.png')"
            />
          </van-row>
          <van-row justify="center" style="margin: 5px 0px 5px 0px; font-size: 12pt">
            {{item.action_title}}
          </van-row>
          <van-row justify="center" style="margin: 0px 0px 0px 0px; font-size: 9pt; color: gray">
            时间： {{item.action_time_range}} &nbsp; {{item.action_date}}
          </van-row>
          <van-row justify="center" style="margin: 0px 0px 0px 0px; font-size: 9pt; color: gray">
            场地： {{item.action_place}} &nbsp; &nbsp; 球拍： {{item.borrow ? 'Borrowed' : 'Unborrowed'}}
          </van-row>
          <van-row justify="center" style="margin: 0px 0px 0px 0px; font-size: 9pt; color: gray">
            {{item.account_name}}({{item.account_student_id}})
          </van-row>
          <van-divider/>
          <van-row justify="center" style="margin: 10px 0px 0px 0px; font-size: 8pt;">
            {{item.sign_code}}
          </van-row>
          <van-row justify="center" style="margin: 0px 0px 0px 0px; font-size: 10pt; font-weight: bold; color: gray">
            <vue-qrcode :value="item.sign_code" :width="240"/>
          </van-row>
          <van-row justify="center" style="margin: 0px 0px 10px 0px; font-size: 8pt; color: gray">
            请出示此码签到，仅限账号本人使用。
          </van-row>

          <van-divider/>
          &nbsp&nbsp
          <van-cell style="margin: -38px 0px 10px 0px;">
            <template #title>
              <div style="font-size: 9pt; margin: 6px 0px 0px 10px; font-weight: bold;">
                {{item.state == 1 ? "已签到" : "Unsigned"}}
              </div>
            </template>
            <div v-if="item.action_state < 4">
              <van-button v-if="item.action_state === 3" @click="onTransforClick(item.id)" type="warning" size="mini" icon="share-o">转让</van-button>&nbsp
              <van-button v-if="item.action_state === 3" @click="onWechatClick(item.id)" type="success" size="mini" icon="chat-o">微信</van-button>
              <van-button v-if="item.action_state < 3" @click="onCanclClick(item.id)" type="danger" size="mini" icon="cross" :disabled="buttonDisabled">取消报名</van-button>
            </div>
            <div v-else-if="item.action_state == 4" style="font-size: 8pt; color: red; font-weight: bold; margin: 7px 0px 0px 0px;">
              进行中
            </div>
            <div v-else style="font-size: 8pt; color: black; margin: 7px 0px 0px 0px;">
              已结束
            </div>
          </van-cell>
        </van-cell-group>
      </div>
    </div>
    <br/>
    <br/>
  </van-pull-refresh>
</template>

<script>
import VueQrcode from "@/main";
import {showConfirmDialog, showFailToast, showSuccessToast} from 'vant';
import Cookies from "js-cookie";

export default {
  components: {VueQrcode},
  created(){
    this.loading = true;
    this.onRefresh();
  },
  data(){
    return{
      buttonDisabled: false,
      isLoading: false,
      isShow: false,
      currentId: -1,
      recordList: [ ],
      wechat_id: '',
      wechat_url: '',
      wechat_show: false,
      transfor_show: false,
      transfor_account: '',
      loading: false,
      username: ''
    };
  },
  methods: {
    onRefresh() {
      this.isLoading = true;
      this.$http.post('/action/queryRecord?token='+Cookies.get('token'))
          .then(response => {
            this.loading = false;
            this.isLoading = false;
            if(response.status === 200){
              if(response.data.status <= 0){
                this.$memberVerify();
                return;
              }
              this.recordList = response.data.data;
            }
          })
          .catch(error =>{
            this.loading = false;
            this.isLoading = false;
            console.log(error);
          });
      /*this.recordList = [
        {id:0, action_title: '8月13日打球活動（前半場）', action_place:'東亞運體育館', action_date: '2024年8月13日', action_time_range: '14:00~15:00', account_student_id: '122003047', account_name: '費才軒', sign_code: 'd66067b8-122e-4e3f-9d7e-fa7abe3bbda0', borrow: false, action_state: 3, state: 0},
        {id:1, action_title: '8月22日打球活動（后半場）', action_place:'科大體育館J座', action_date: '2024年8月22日', action_time_range: '15:00~16:00', account_student_id: '122003047', account_name: '費才軒', sign_code: '4d93f326-3f48-4a43-929d-b6489f4754b5', borrow: true, action_state: 2, state: 0},
        {id:2, action_title: '7月12日打球活動（后半場）', action_place:'科大體育館J座', action_date: '2024年7月12日', action_time_range: '15:00~16:00', account_student_id: '122003047', account_name: '費才軒', sign_code: 'a98f184e-976c-25a7-5258-57570a66d6d7', borrow: true, action_state: 4, state: 1},
        {id:3, action_title: '7月5日打球活動（后半場）', action_place:'科大體育館J座', action_date: '2024年7月5日', action_time_range: '15:00~16:00', account_student_id: '122003047', account_name: '費才軒', sign_code: 'b98f184e-976c-25a7-5258-57570a66d6d7', borrow: true, action_state: 5, state: 1}
      ]*/
    },
    onTransforClick(id) {
      this.currentId = id;
      this.username = '';
      this.transfor_show = true;
    },
    onCanclClick(id) {
      this.currentId = id;
      showConfirmDialog({
        title: '提示',
        confirmButtonText: '继续',
        cancelButtonText: '取消',
        message:
            '退出报名后，空缺名额将优先按顺序分给候补成员，你可能无法再次报名。确认退出吗？',
      }).then(() => {
            this.buttonDisabled = true;
            this.loading = true;
            this.$http.post('/action/cancelAction?token='+Cookies.get('token')
                +`&record_id=${this.currentId}`)
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
                    showFailToast("记录不存在，请刷新页面");
                    this.buttonDisabled = false;
                  }
                  if(response.data.status === 0){
                    showFailToast("活动报名已截止，无法取消");
                    this.buttonDisabled = false;
                  }
                  if(response.data.status === 1){
                    showFailToast("用户信息与报名记录不符");
                    this.buttonDisabled = false;
                  }
                  if(response.data.status === 2){
                    showSuccessToast("已取消报名");
                    this.onRefresh();
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
    onWechatClick(id){
      this.loading = true;
      this.currentId = id;
      this.buttonDisabled = true;
      this.$http.post('/action/queryWechatGroup?token='+Cookies.get('token')
          +`&record_id=${this.currentId}`)
          .then(response => {
            this.loading = false;
            if(response.status !== 200){
              showFailToast("系统错误");
              this.buttonDisabled = false;
            }
            if(response.data.status <= 0){
              showFailToast("请刷新页面后重试");
              this.buttonDisabled = false;
            }
            if(response.data.status > 0){
              this.wechat_id = response.data.data.wechat_id;
              this.wechat_url = response.data.data.wechat_url;
              this.wechat_show = true;
            }
          })
          .catch(error => {
            this.loading = false;
            showFailToast("网络连接失败");
            this.buttonDisabled = false;
          })

    },
    close(){
      this.isShow = false;
    },
    send_transfor_first(){
      this.isShow = true;
    },
    send_transfor(){
      this.loading = true;
      this.isShow = false;
      this.buttonDisabled = true;
      this.$http.post(`transfer/transferRecord?token=${Cookies.get('token')}&record_id=${this.currentId}
                           &receive_user=${encodeURIComponent(this.username)}`)
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
              showFailToast("请刷新页面后重试");
              this.buttonDisabled = false;
              this.transfor_show = false;
            }
            if(response.data.status === 0){
              showFailToast("活动正在进行或已结束，无法转让名额。");
              this.buttonDisabled = false;
              this.transfor_show = false;
              this.onRefresh();
            }
            if(response.data.status === 1){
              showFailToast("账号不匹配，请刷新页面后重试");
              this.buttonDisabled = false;
              this.transfor_show = false;
            }
            if(response.data.status === 2){
              showFailToast("已发起转让，请等待对方确认。");
              this.buttonDisabled = false;
              this.transfor_show = false;
            }
            if(response.data.status === 3){
              showFailToast("找不到接收账号，请核对用户名是否完整、正确。");
              this.buttonDisabled = false;
            }
            if(response.data.status === 4){
              showSuccessToast("已发起转让，对方将收到通知");
              this.buttonDisabled = false;
              this.transfor_show = false;
            }
          })
          .catch(error => {
            this.loading = false;
            showFailToast("网络连接失败");
            this.buttonDisabled = false;
          });
    }
  }
}
</script>