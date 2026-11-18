<template>
  <lay-layer v-model="loading" type="3" shade-close="false"/>
  <lay-layer v-model="disabled" type="3" shade-close="false"/>
  <lay-layer v-model="editUserShow" title="编辑账号" :area="['600px', '620px']" z-index="1000">
    <lay-form :model="editUserInf">
      <lay-quote>账号信息</lay-quote>
      <lay-row space="10" style="margin-top: 10pt; width: 590px">
        <lay-col md="14">
          <lay-form-item label="用户名" prop="text" style="text-align: left"  label-width="100px" required>
            <lay-input v-model="editUserInf.username" type="test" style="width: 222px"></lay-input>
          </lay-form-item>
        </lay-col>
        <lay-col md="10">
          <lay-form-item label="状态" prop="text">
            <lay-select v-model="editUserInf.state" placeholder="请选择" style="width: 150px">
              <lay-select-option :value="0" label="已封禁"></lay-select-option>
              <lay-select-option :value="1" label="失信"></lay-select-option>
              <lay-select-option :value="2" label="正常"></lay-select-option>
            </lay-select>
          </lay-form-item>
        </lay-col>
      </lay-row>
      <lay-quote>个人信息</lay-quote>
      <lay-row space="4" style="margin-top: 10pt; width: 590px">
        <lay-col md="12">
          <lay-form-item label="姓名" prop="text" style="text-align: left" required>
            <lay-input v-model="editUserInf.name" type="text" style="width: 200px"></lay-input>
          </lay-form-item>
        </lay-col>
        <lay-col md="12">
          <lay-form-item label="会员卡号" prop="text" style="text-align: left" required>
            <lay-input v-model="editUserInf.card_id" type="text" style="width: 200px"></lay-input>
          </lay-form-item>
        </lay-col>
        <lay-col md="24">
          <lay-form-item label="学号" prop="text" style="text-align: left;" label-width="104px" required>
            <lay-input v-model="editUserInf.student_id" type="text" style="width: 466px"></lay-input>
          </lay-form-item>
        </lay-col>
      </lay-row>
      <lay-quote>联系方式</lay-quote>
      <lay-row space="4" style="margin-top: 10pt; width: 590px">
        <lay-col md="12">
          <lay-form-item label="手机号" prop="text" style="text-align: left" required>
            <lay-input v-model="editUserInf.phone" type="text" style="width: 200px"></lay-input>
          </lay-form-item>
        </lay-col>
        <lay-col md="12">
          <lay-form-item label="微信号" prop="text" style="text-align: left" required>
            <lay-input v-model="editUserInf.wechat_id" type="text" style="width: 200px"></lay-input>
          </lay-form-item>
        </lay-col>
        <lay-col md="24">
          <lay-form-item label="邮箱" prop="text" style="text-align: left">
            <lay-input v-model="editUserInf.email" type="text" style="width: 496px"></lay-input>
          </lay-form-item>
        </lay-col>
      </lay-row>
      <div style="text-align: right; margin-top: -3px;">
        <lay-button @click="this.editUserShow = false"><lay-icon type="layui-icon-close"/> 取消</lay-button>
        <lay-button type="primary" style="margin-right: 20px" @click="onEditSubmit" :disabled="disabled"><lay-icon type="layui-icon-release"/> 提交</lay-button>
      </div>
    </lay-form>
  </lay-layer>

  <lay-table
      :page="page"
      :columns="columns"
      :data-source="dataSource"
      style="margin: 10pt; height: calc(100vh - 70pt);"
      :default-toolbar="true"
      @change="change">
    <template #toolbar>
      <lay-row>
        <lay-col md="24">
          <lay-breadcrumb style="margin-left: 6pt">
            <lay-breadcrumb-item title="账号管理"></lay-breadcrumb-item>
            <lay-breadcrumb-item title="失信管理"></lay-breadcrumb-item>
          </lay-breadcrumb>
          <lay-col md="24" style="margin-top: 4pt">
            <lay-input v-model="preQuery.name" size="sm" type="text" style="width: 120pt" placeholder="姓名" prefix-icon="layui-icon-user"></lay-input>
            <lay-input v-model="preQuery.student_id" size="sm" type="text" style="width: 180pt; margin-left: 10pt" placeholder="学号" prefix-icon="layui-icon-read"></lay-input>
            <lay-button type="primary" size="sm" style="margin-left: 10pt" prefix-icon="layui-icon-search" @click="queryData(-1)" :disabled="loading">查询</lay-button>
          </lay-col>
        </lay-col>
      </lay-row>
    </template>
    <template #empty>
      <lay-empty description="暂无记录"></lay-empty>
    </template>
    <template v-slot:operator="{ rowIndex }">
      <lay-button size="xs" type="normal" :disabled="this.loading" @click="onEditShow(rowIndex)"><lay-icon type="layui-icon-tabs"/> 编辑</lay-button>
      <lay-button size="xs" type="primary" :disabled="this.loading" @click="onClearSubmit(rowIndex)"><lay-icon type="layui-icon-fonts-clear"/>清空失信积分</lay-button>
      <lay-button size="xs" type="warm" :disabled="this.loading" @click="onResetSubmit(rowIndex)"><lay-icon type="layui-icon-refresh"/>重置失信积分</lay-button>
    </template>
  </lay-table>
</template>

<script>
import {layer} from "@layui/layui-vue";
import Cookies from "js-cookie";

export default {
  beforeRouteLeave (to, from, next) {
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
    next();
  },
  created() {
    this.loading = true;
    this.queryData();
    this.intervalId = setInterval(this.queryData, 10000);
  },
  beforeDestroy() {
    // 销毁计时器
    if (this.intervalId) {
      clearInterval(this.intervalId);
    }
  },
  data(){
    return{
      preQuery:{
        name: '',
        student_id: ''
      },
      query:{
        name: '',
        student_id: ''
      },
      loading: false,
      page:{
        current: 1,
        limit: 10,
        total: 0
      },
      columns:[
        { title:"用户名", width:"160px", resize:true, key:"username"},
        { title:"姓名", width:"160px", resize:true, key:"name" },
        { title:"学号", width:"200px", resize:true, key:"student_id" },
        { title:"微信号", width:"160px", resize:true, key:"wechat_id"},
        { title:"手机号", width:"160px", resize:true, key:"phone" },
        { title:"失信积分", width:"160px", resize:true, key:"unsigned_num" },
        { title:"状态", width:"150px", resize:true, key:"status_name" },
        { title:"操作" , width: "320px" , fixed: "right", customSlot:"operator", key:"operator", ignoreExport: true }
      ],
      dataSource:[],
      editUserInf:{
        id: -1,
        username: '',
        name: '',
        phone: '',
        state: 0,
        student_id: '',
        wechat_id: '',
        email: '',
        card_id: '',
      },
      editUserShow: false,
      disabled: false,
      currentIndex: -1
    };
  },
  methods: {
    change() {
      this.queryData();
    },
    queryData(val){
      if(val != null){
        this.query.name = this.preQuery.name;
        this.query.student_id = this.preQuery.student_id;
        this.loading = true;
      }
      this.$http.post(`/member/queryUnsignedMembers?token=${Cookies.get('token')}&name=${encodeURIComponent(this.query.name)}
&student_id=${encodeURIComponent(this.query.student_id)}&page_size=${this.page.limit}&page_number=${this.page.current}`)
          .then(res => {
            if(res.status !== 200){
              layer.msg('系统错误', {icon: 2, time: 1500});
              this.loading = false;
              return;
            }
            // console.log(res.data.data);
            if(res.data.status < 0){
              if (this.intervalId) {
                clearInterval(this.intervalId);
              }
              this.$clear();
              this.loading = false;
              return;
            }
            for(var i in res.data.data)
              this.computedStatusName(res.data.data[i]);
            this.dataSource = res.data.data;
            this.page.total = res.data.status;
            if(this.dataSource.length === 0 && this.page.current > 1){
              this.page.current = this.page.current - 1;
              this.queryData();
            }
            this.loading = false;
          })
          .catch(error => {
            layer.msg('网络连接失败', {icon: 2, time: 1500});
            this.loading = false;
          })
    },
    computedStatusName(obj){
      obj.status_name = '';
      switch(obj.state){
        case 0:
          obj.status_name = '已封禁'; break;
        case 1:
          obj.status_name = '失信'; break;
        case 2:
          obj.status_name = '正常'; break;
      }
    },
    onEditShow(id){
      this.currentIndex = id;
      this.editUserInf = JSON.parse(JSON.stringify(this.dataSource[id]));
      this.editUserShow = true;
    },
    onEditSubmit(){
      if(this.editUserInf.username === '' || this.editUserInf.name === '' || this.editUserInf.card_id === '' ||
      this.editUserInf.phone === '' || this.editUserInf.wechat_id === '' || this.editUserInf.student_id === ''){
        layer.msg('请填写必填信息', {icon: 7, time: 1500});
        return;
      }
      this.disabled = true;
      this.$http.post(`/member/updateUserInf?token=${Cookies.get('token')}&id=${this.editUserInf.id}&username=${encodeURIComponent(this.editUserInf.username)}&name=${encodeURIComponent(this.editUserInf.name)}\
&card_id=${encodeURIComponent(this.editUserInf.card_id)}&phone=${encodeURIComponent(this.editUserInf.phone)}&state=${encodeURIComponent(this.editUserInf.state)}&wechat_id=${encodeURIComponent(this.editUserInf.wechat_id)}\
&email=${encodeURIComponent(this.editUserInf.email)}&student_id=${encodeURIComponent(this.editUserInf.student_id)}`)
          .then(res => {
            if(res.status === 200){
              if(res.data.status === -2) {
                this.$clear();
                return;
              }
              if(res.data.status === -1){
                this.disabled = false;
                layer.msg('无法修改当前登录账号的管理员权限。',{icon: 7, time: 1500});
                return;
              }
              if(res.data.status === 0){
                this.disabled = false;
                layer.msg('该用户名已被其他账号使用。',{icon: 7, time: 1500});
                return;
              }
              if(res.data.status === 1){
                this.disabled = false;
                this.editUserShow = false;
                layer.msg('该账号已删除，请刷新页面后重试。',{icon: 7, time: 1500});
                return;
              }
              if(res.data.status === 2){
                this.disabled = false;
                this.editUserShow = false;
                layer.msg('该账号仍有值班安排，请重新分配值班人员或等活动结束后再修改。',{icon: 7, time: 1500});
                return;
              }
              this.dataSource[this.currentIndex] = JSON.parse(JSON.stringify(this.editUserInf));
              this.computedStatusName(this.dataSource[this.currentIndex]);
              this.disabled = false;
              this.editUserShow = false;
              layer.msg('更新成功',{icon: 1, time: 1500});
            }else{
              layer.msg('系统错误',{icon: 1, time: 1500});
            }
          })
          .catch(res => {
            layer.msg('网络连接失败', {icon: 2, time: 1500})
          });
    },
    onClearSubmit(index){
      layer.confirm(`确认清空「${this.dataSource[index].username}」的失信积分吗？相关记录会保留。`,
          {
            title:"查询",
            icon: 3,
            btn: [
              {text:'确认', callback: (id) => {
                  layer.close(id);
                  this.disabled = true;
                  this.$http.post(`/member/clearUserUnsigned?token=${Cookies.get('token')}&user_id=${this.dataSource[index].id}`)
                      .then(res => {
                        if(res.status === 200){
                          if(res.data.status === -2) {
                            this.$clear();
                            return;
                          }
                          if(res.data.status === 0){
                            this.disabled = false;
                            this.changePasswordShow = false;
                            layer.msg('该账号已删除，请刷新页面后重试。',{icon: 7, time: 1500});
                            return;
                          }
                          if(res.data.status === 1){
                            this.disabled = false;
                            this.changePasswordShow = false;
                            layer.msg('该账号信息已更新，请刷新页面后重试。',{icon: 7, time: 1500});
                            return;
                          }
                          this.dataSource[this.currentIndex] = JSON.parse(JSON.stringify(this.editUserInf));
                          this.computedStatusName(this.dataSource[this.currentIndex]);
                          this.disabled = false;
                          this.changePasswordShow = false;
                          layer.msg('该账号的失信积分已清空，可通过「重置失信积分」恢复。',{icon: 1, time: 1500});
                          if(this.dataSource.length === 1 && this.page.current > 1){
                            this.page.current = this.page.current - 1;
                          }
                          this.queryData();
                        }else{
                          layer.msg('系统错误',{icon: 1, time: 1500});
                        }
                      })
                      .catch(res => {
                        layer.msg('网络连接失败', {icon: 2, time: 1500})
                      })

                }
              },
              {text:'取消', callback: (id) => {
                  layer.close(id);
              }
              }
            ]
          }
      );
    },
    onResetSubmit(index){
      layer.confirm(`确认根据相关记录重新计算「${this.dataSource[index].username}」的失信积分吗？`,
          {
            title:"查询",
            icon: 3,
            btn: [
              {text:'确认', callback: (id) => {
                  layer.close(id);
                  this.disabled = true;
                  this.$http.post(`/member/resetUserUnsigned?token=${Cookies.get('token')}&user_id=${this.dataSource[index].id}`)
                      .then(res => {
                        if(res.status === 200){
                          if(res.data.status === -2) {
                            this.$clear();
                            return;
                          }
                          if(res.data.status === 0){
                            this.disabled = false;
                            this.changePasswordShow = false;
                            layer.msg('该账号已删除，请刷新页面后重试。',{icon: 7, time: 1500});
                            return;
                          }
                          if(res.data.status === 1){
                            this.disabled = false;
                            this.changePasswordShow = false;
                            layer.msg('该账号信息已更新，请刷新页面后重试。',{icon: 7, time: 1500});
                            return;
                          }
                          this.dataSource[this.currentIndex] = JSON.parse(JSON.stringify(this.editUserInf));
                          this.computedStatusName(this.dataSource[this.currentIndex]);
                          this.disabled = false;
                          this.changePasswordShow = false;
                          layer.msg('该账号已重置',{icon: 1, time: 1500});
                          this.queryData();
                        }else{
                          layer.msg('系统错误',{icon: 1, time: 1500});
                        }
                      })
                      .catch(res => {
                        layer.msg('网络连接失败', {icon: 2, time: 1500})
                      })

                }
              },
              {text:'取消', callback: (id) => {
                  layer.close(id);
                }
              }
            ]
          }
      );
    }
  }
}

</script>

<style>

</style>
