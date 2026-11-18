<template>
  <van-toast v-model:show="loading" type="loading" overlay="true" duration="0"
             forbid_click="true" message="加载中…"></van-toast>
  <van-action-sheet v-model:show="setPasswordShow" :z-index="100" title="密码设置">
    <Vcode :show="isChangePassVerifyShow"
           slider-text="拖动滑块完成验证"
           fail-text="验证失败，请重试"
           success-text="验证通过"
           :range="5"
           @success="onChangePassClick"
           @close="close"
    />
    <van-cell-group>
      <van-field
          label-width="9em"
          v-model="changeInf.originPass"
          type="password"
          name="原密碼"
          label="原密码"
          placeholder=""
      />
      <van-field
          label-width="8em"
          v-model="changeInf.newPass"
          type="password"
          name="新密碼"
          label="新密码"
          placeholder=""
      />
      <van-field
          label-width="9em"
          v-model="changeInf.confirmPass"
          type="password"
          name="密碼確認"
          label="确认密码"
          placeholder=""
      />
      <br/>
      <van-row justify="center">
        <van-button round block type="primary" @click="changePassPre" icon="guide-o" style="width: 200px">
          修改密码
        </van-button>
      </van-row>
      <br/>
    </van-cell-group>
  </van-action-sheet>
  <van-action-sheet v-model:show="setContactShow" :z-index="100" title="更新联系方式">
    <Vcode :show="isChangeContactVerifyShow"
           slider-text="拖动滑块完成验证"
           fail-text="验证失败，请重试"
           success-text="验证通过"
           :range="5"
           @success="onChangeContactClick"
           @close="close"
    />
    <p style="font-size: 8pt; color: gray; margin-left: 10pt"> 如需修改会员个人信息，请提供身份证件复印件并联系客服。</p>
    <van-cell-group>
      <van-field
          v-model="changeInf.originPass"
          type="password"
          name="密碼"
          label="密码"
          placeholder="需要验证密码"
      />
      <van-field
          v-model="changeInf.phone"
          type="tel"
          name="手機號碼"
          label="手机号"
          placeholder="设置手机号"
      />
      <van-field
          v-model="changeInf.email"
          type="text"
          name="郵箱"
          label="邮箱"
          placeholder="设置邮箱"
      />
      <van-field
          v-model="changeInf.wechat_id"
          name="微信號"
          label="微信号"
          placeholder="用于日常活动联系"
      />
      <br/>
      <van-row justify="center">
        <van-button round block type="primary" @click="changeContactPre" icon="guide-o" style="width: 200px">
          更新
        </van-button>
      </van-row>
      <br/>
    </van-cell-group>
  </van-action-sheet>
  <van-dialog v-model:show="isAddMyEquipmentShow" title="在此设备上启用一键登录" @cancel="this.isAddMyEquipmentShow = false"
              show-cancel-button cancel-button-text="取消" confirm-button-text="确认" @confirm="submitEquipment">
    <div style="width: 85%; margin-right: auto; margin-left: auto; margin-top: 5pt; margin-bottom: 0pt; font-size: 10pt; color: #666666">
      启用后，可在此设备上免密码登录。
      <b>请勿在不信任的设备上启用此功能。</b>。请在下方为该设备设置名称，最多 12 个字符。
    </div>
    <van-field v-model="name" placeholder="设备名称" left-icon="graphic" style="font-size: 12pt; width: 95%; margin-right: auto; margin-left: auto;"/>
    <div style="width: 85%; margin-right: auto; margin-left: auto; margin-top: 5pt; margin-bottom: 0pt; font-size: 10pt; color: #666666">
      <van-icon name="warn-o" /> 这项操作需要验证密码。
    </div>
    <van-field v-model="password" placeholder="密码" left-icon="lock" style="font-size: 12pt; width: 95%; margin-right: auto; margin-left: auto;" type="password"/>
  </van-dialog>
  <van-action-sheet v-model:show="setFastLoginShow" :z-index="100" title="一键登录管理" style="height: 75%;">
    <van-empty
        v-show="equipments.length === 0"
        style="margin-top: 15pt"
        image="https://fastly.jsdelivr.net/npm/@vant/assets/custom-empty-image.png"
        image-size="80"
        description="暂无一键登录设备"
    />
    <div class="device-card" v-for="equip in equipments" :style="{ border: equip.is_local ? '4px solid #ccc' : ''}">
      <div class="device-icon">
        <i class="fas fa-device"></i>
      </div>
      <div class="device-info">
        <div class="device-name">姓名： {{equip.name}}</div>
        <div class="device-id">设备编号： {{equip.equip_id}}</div>
        <van-button type="danger" size="mini" icon="delete-o" class="delete-button" @click="deleteEquipment(equip.id, equip.name)">取消一键登录授权</van-button>
        <p style="font-size: 9pt; margin-top: 3pt; margin-bottom: -6pt; color: #666666" v-if="equip.is_local">当前设备</p>
      </div>
    </div>
    <van-button round block icon="link-o" :disabled="disabled" type="primary" size="small" @click="onAddManageClick"
                style="width: 75%; max-width: 300px; height: 40px; margin-top: 15pt; margin-left: auto; margin-right: auto" v-show="canAddMyEquipment">在此设备上启用一键登录</van-button>
    <center style="font-size: 9pt; margin-top: 5pt">最多可以添加 5 台设备。<br/><br/></center>
  </van-action-sheet>
  <h1 class="club-page-title">我的账号</h1>
  <div class="club-account">
    <van-cell-group inset class="club-detail-card">
      <h2 class="club-card-heading">{{ memInf.name || '个人资料' }}</h2>
      <van-cell title="用户名" size="small">{{memInf.username}}</van-cell>
      <van-cell title="学号">{{memInf.student_id}}</van-cell>
      <van-cell title="手机号">{{memInf.phone}}</van-cell>
      <van-cell title="邮箱" v-if="memInf.email !== ''">{{memInf.email}}</van-cell>
      <van-cell title="微信号">{{memInf.wechat_id}}</van-cell>
      <van-cell title="状态">{{memberStatus}}</van-cell>
      <van-cell title="失信积分" v-if="memInf.state >= 0 && memInf.state <= 2">{{memInf.unsigned_num}}</van-cell>
      <van-cell title="值班次数" v-if="memInf.state === 3">{{memInf.unsigned_num}}</van-cell>
    </van-cell-group>
    <van-cell-group inset class="club-detail-card">
      <h2 class="club-card-heading">账号设置</h2>
      <van-cell title="密码设置"  is-link @click="onChangePassShow"/>
      <van-cell title="更新联系方式"  is-link @click="onChangeContactShow"/>
      <van-cell title="一键登录管理"  is-link @click="onEquipManageShow"/>
      <van-cell title="退出登录" is-link @click="signout"/>
    </van-cell-group>
  </div>
</template>

<script>
import Cookies from "js-cookie";
import {showSuccessToast, showFailToast, showToast, showDialog} from "vant";
import { showConfirmDialog } from 'vant';

export default {
  data(){
    return {
      memInf: {
        name: '',
        username: '',
        student_id: '',
        phone: '',
        email: '',
        wechat_id: '',
        state: 0,
        unsigned_num: 0
      },
      changeInf: {
        originPass: '',
        newPass: '',
        confirmPass: '',
        wechat_id: '',
        phone: '',
        email: '',
      },
      loading: false,
      name:'',
      password: '',
      equipments: [],
      setPasswordShow: false,
      setContactShow: false,
      isChangePassVerifyShow: false,
      isChangeContactVerifyShow: false,
      isAddMyEquipmentShow: false,
      setFastLoginShow: false,
      canAddMyEquipment: true
    };
  },
  computed: {
    memberStatus() {
      switch (this.memInf.state) {
        case 0:
          return '已封禁';
        case 1:
          return '失信';
        case 2:
          return '正常';
        case 3:
          return '值班人员'
        case 4:
          return '管理员'
      }
      return '未知';
    }
  },
  created(){
    this.loading = true;
    if(this.$route.name === 'member_membership')
      this.$memberVerify();
    else
      this.$staffVerify();
    this.$http.post('/user/verify?token='+Cookies.get('token'))
        .then(response => {
          console.log(response.data.data);
          this.memInf = response.data.data;
          this.loading = false;
        })
        .catch(error =>{
          this.loading = false;
          console.log(error);
        });
  },
  methods: {
    signout(){
      this.$http.post('/user/logout?token='+Cookies.get('token')).then(function (a){}).catch(function(a){});
      Cookies.remove('token');
      showFailToast('该账号已退出登录。');
      this.$router.push('/inbox');
    },
    onChangePassShow(){
      this.changeInf.confirmPass = '';
      this.changeInf.newPass = '';
      this.changeInf.originPass = '';
      this.setPasswordShow = true;
    },
    changePassPre(){
      if(this.changeInf.originPass === '' || this.changeInf.newPass === '' || this.changeInf.confirmPass === ''){
        showFailToast('请输入密码');
        return;
      }
      if(this.changeInf.newPass !== this.changeInf.confirmPass){
        showFailToast('两次输入的密码不一致');
        return;
      }
      this.isChangePassVerifyShow = true;
    },
    onChangePassClick(){
      this.isChangePassVerifyShow = false;
      this.loading = true;
      const pattern = /^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[$@$!%*?&])[A-Za-z\d$@$!%*?&]{8,}/;
      if(pattern.test(this.changeInf.newPass) === false){
        this.loading = false;
        showToast("密码至少要有 8 个字符，并包含大写字母、小写字母、数字和特殊字符。");
        return;
      }
      const token = Cookies.get('token');
      this.$http.post(`/user/password?token=${token}&origin_pass=${encodeURIComponent(this.changeInf.originPass)}&new_pass=${encodeURIComponent(this.changeInf.newPass)}`)
          .then(response =>{
            this.loading = false;
            if(response.data.status <= 0){
              showFailToast('账号状态异常');
            }
            if(response.data.status === 1){
              showFailToast('原密码错误。');
            }
            if(response.data.status === 2){
              showFailToast('数据库异常');
            }
            if(response.data.status === 3){
              showSuccessToast('修改成功');
              this.setPasswordShow = false;
            }
          })
          .catch(error =>{
            this.loading = false;
            console.log(error);
            showSuccessToast('修改成功');
          });
    },
    deleteEquipment(id, name){
      showConfirmDialog({
        message: `确认解除设备「${name}」的一键登录授权吗？再次使用时需要重新授权。`,
        confirmButtonText: '确认',
        cancelButtonText: '取消'
      }).then(() =>{
        this.loading = true;
        this.$http.post(`/user/deleteEquipment?token=${Cookies.get('token')}&id=${id}`)
            .then(response =>{
              this.loading = false;
              if(response.data.status === -2){
                showFailToast('账号状态异常');
              }
              if(response.data.status === -1){
                showFailToast('设备已解除绑定，请刷新页面。');
              }
              if(response.data.status === 0){
                showFailToast('此设备未绑定到当前账号，请刷新页面。');
              }
              if(response.data.status === 1){
                showSuccessToast('设备已解除绑定');
                this.onEquipManageShow();
              }
            })
            .catch(error =>{
              this.loading = false;
              console.log(error);
              showFailToast('网络连接失败');
            });
      }).catch(() => {});
    },
    async onEquipManageShow(){
      this.loading = true;
      if(this.$route.name === 'member_membership')
        this.$memberVerify();
      else
        this.$staffVerify();
      this.$http.post('/user/queryEquips?token='+Cookies.get('token')+'&local='+await this.$finger())
          .then(response => {
            this.loading = false;
            if(response.status === 200 && response.data.status > 0)
              this.equipments = response.data.data;
            if(response.data.status === 2)
              this.canAddMyEquipment = false;
            else
              this.canAddMyEquipment = true;
            this.setFastLoginShow = true;
          })
          .catch(error =>{
            this.loading = false;
            console.log(error);
            showFailToast('网络连接失败');
          });
    },
    async submitEquipment(){
      if(this.getByteLength(this.password) === 0){
        showFailToast('请输入密码');
        return;
      }
      if(this.getByteLength(this.name) > 12){
        showFailToast('设备名称过长');
        return;
      }
      if(this.getByteLength(this.name) === 0){
        showFailToast('请输入设备名称');
        return;
      }
      this.loading = true;
      this.$http.post('/user/newEquipment?token='+Cookies.get('token')+'&equip_id='+await this.$finger()+'&name='+encodeURIComponent(this.name)+'&password='+encodeURIComponent(this.password))
          .then(response => {
            this.loading = false;
            if(response.status !== 200){
              showFailToast('系统错误');
              return;
            }
            if(response.data.status === -2){
              showFailToast('密码错误，验证失败');
              return;
            }
            if(response.data.status === -1){
              showDialog({
                message: '此设备已绑定其他账号的一键登录。请先在该账号中解除绑定，再重试。',
                confirmButtonText: '确定'
              }).then(() => {});
              return;
            }
            if(response.data.status === 0){
              showDialog({
                message: '账号绑定的设备已达上限。请先解除部分绑定，再添加新设备。',
                confirmButtonText: '确定'
              }).then(() => {
                // on close
              });
              return;
            }
            showSuccessToast('当前设备绑定成功');
            this.onEquipManageShow();
          })
          .catch(error =>{
            this.loading = false;
            showFailToast('网络连接失败');
            console.log(error);
          });
    },
    onAddManageClick(){
      this.name = "";
      this.password = "";
      this.isAddMyEquipmentShow = true;
    },
    onChangeContactShow(){
      this.changeInf.phone = this.memInf.phone;
      this.changeInf.email = this.memInf.email;
      this.changeInf.wechat_id = this.memInf.wechat_id;
      this.changeInf.originPass = '';
      this.setContactShow = true;
    },
    changeContactPre(){
      if(this.changeInf.originPass === ''){
        showFailToast('请输入密码');
        return;
      }
      if(this.changeInf.phone === ''){
        showFailToast('请输入手机号。');
        return;
      }
      if(this.changeInf.wechat_id === ''){
        showFailToast('请输入微信号');
        return;
      }
      this.isChangeContactVerifyShow = true;
    },
    onChangeContactClick(){
      this.loading = true;
      this.isChangeContactVerifyShow = false;
      this.isChangePassVerifyShow = false;
      const token = Cookies.get('token');
      this.$http.post(`/user/contact?token=${token}&origin_pass=${encodeURIComponent(this.changeInf.originPass)}&email=${encodeURIComponent(this.changeInf.email)}&phone=${encodeURIComponent(this.changeInf.phone)}&wechat_id=${encodeURIComponent(this.changeInf.wechat_id)}`)
          .then(response =>{
            this.loading = false;
            if(response.data.status <= 0){
              showFailToast('账号状态异常');
            }
            if(response.data.status === 1){
              showFailToast('密码错误，验证失败');
            }
            if(response.data.status === 2){
              sshowFailToast('数据库异常');
            }
            if(response.data.status === 3){
              showSuccessToast('联系方式已更新');
              this.memInf.wechat_id = this.changeInf.wechat_id;
              this.memInf.phone = this.changeInf.phone;
              this.memInf.email = this.changeInf.email;
              this.setContactShow = false;
            }
          })
          .catch(error =>{
            this.loading = false;
            console.log(error);
            showFailToast('网络连接失败');
          });
    },
    close(){
      this.isChangeContactVerifyShow = false;
      this.isChangePassVerifyShow = false;
    },
    getByteLength(str) {
      let len = 0;
      for (let i = 0; i < str.length; i++) {
        const code = str.charCodeAt(i);
        if (code >= 0 && code <= 128) {
          len += 1;
        } else {
          len += 2;
        }
      }
      return len;
    }
  }
}
</script>

<style scoped lang="scss">
.device-card {
  display: flex;
  align-items: center;
  border: 1px solid #ccc;
  border-radius: 10px;
  padding: 16px;
  width: 80%;
  margin-left: auto;
  margin-right: auto;
  margin-top: 15pt;
  max-width: 350px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.device-icon {
  flex-shrink: 0;
  margin-right: 16px;
  width: 88px;
  height: 88px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-image: url('~@/assets/equipment.png');
  background-size: contain;
  background-repeat: no-repeat;
}

.device-info {
  flex-grow: 1;
  text-align: center;
}

.device-name {
  font-size: 16px;
  font-weight: bold;
  margin-bottom: 8px;
}

.device-id {
  color: #666;
  margin-bottom: 12px;
}

.delete-button {
  background-color: #ff4d4f;
  color: white;
  border: none;
  border-radius: 5px;
  padding: 8px 16px;
  cursor: pointer;
  font-size: 12px;
}

.delete-button:hover {
  background-color: #ff1a1c;
}
</style>