<template>
  <lay-layer v-model="loading" type="3" shade-close="false"/>
  <main class="admin-dashboard">
    <header class="admin-dashboard__hero">
      <h1>管理概览</h1>
      <div class="admin-dashboard__actions">
        <router-link class="admin-dashboard__create" to="/main/action/create">
          <lay-icon type="layui-icon-release"/> 创建活动
        </router-link>
        <button class="admin-dashboard__refresh" type="button" :disabled="loading" @click="loadDashboard">
          <lay-icon type="layui-icon-refresh"/> 刷新
        </button>
      </div>
    </header>

    <p v-if="loadError" class="admin-dashboard__error" role="alert">统计加载失败，请点「刷新」重试。</p>

    <section v-if="hasLoaded" class="admin-dashboard__metrics" aria-label="统计数据">
      <article
        v-for="metric in [
          { label: '会员总数', value: totalMembers, unit: ' 人', icon: 'layui-icon-user' },
          { label: '值班人员', value: totalStuffs, unit: ' 人', icon: 'layui-icon-log' },
          { label: '活动总数', value: totalActions, unit: ' 次', icon: 'layui-icon-template' },
          { label: '参与次数', value: totalRecords, unit: ' 次', icon: 'layui-icon-form' },
          { label: '平均值班次数', value: avaregeWorkTimes, unit: ' 次', icon: 'layui-icon-chart', decimals: 2 },
          { label: '失信记录', value: totalUnsignedRecords, unit: ' 条', icon: 'layui-icon-face-cry' }
        ]"
        :key="metric.label"
        class="admin-dashboard__tile"
      >
        <span class="admin-dashboard__metric-icon"><lay-icon :type="metric.icon" /></span>
        <h2>{{ metric.label }}</h2>
        <p><lay-count-up :startVal="0" :endVal="metric.value" :suffix="metric.unit" :duration="600" :decimalPlaces="metric.decimals || 0" /></p>
      </article>
    </section>

    <div v-if="hasLoaded" class="admin-dashboard__details">
      <section class="admin-dashboard__tile">
        <h2>当前账号</h2>
        <dl v-if="userInf" class="admin-dashboard__profile">
          <div><dt>用户名</dt><dd>{{ userInf.username }}</dd></div>
          <div><dt>姓名</dt><dd>{{ userInf.name }}</dd></div>
          <div><dt>学号</dt><dd>{{ userInf.student_id }}</dd></div>
          <div><dt>手机号</dt><dd>{{ userInf.phone }}</dd></div>
          <div><dt>微信号</dt><dd>{{ userInf.wechat_id }}</dd></div>
          <div><dt>邮箱</dt><dd>{{ userInf.email || '未注册' }}</dd></div>
        </dl>
      </section>

      <section class="admin-dashboard__tile">
        <h2>失信积分前五名</h2>
        <ol v-if="unsignMemberList.length" class="admin-dashboard__ranking">
          <li v-for="(item, index) in unsignMemberList" :key="index">
            <span>{{ item.name }}</span><strong>{{ item.unsigned_num }} 分</strong>
          </li>
        </ol>
        <p v-else class="admin-dashboard__empty">暂无记录</p>
      </section>

      <section class="admin-dashboard__tile">
        <h2>值班次数前五名</h2>
        <ol v-if="stuffMemberList.length" class="admin-dashboard__ranking">
          <li v-for="(item, index) in stuffMemberList" :key="index">
            <span>{{ item.name }}</span><strong>{{ item.unsigned_num }} 次</strong>
          </li>
        </ol>
        <p v-else class="admin-dashboard__empty">暂无记录</p>
      </section>
    </div>
  </main>
</template>

<script>
import Cookies from "js-cookie";

export default {
  created() {
    this.loadDashboard();
  },
  methods: {
    async loadDashboard() {
      if (this.loading) return;
      this.loading = true;
      this.loadError = false;
      try {
        const { data } = await this.$http.post('/member/queryInboxData', null, {
          params: { token: Cookies.get('token') }
        });
        if (data.status === -1) {
          this.$clear();
          return;
        }
        if (data.status !== 1 || !data.data) {
          this.loadError = true;
          return;
        }

        const dashboard = data.data;
        this.totalActions = dashboard.totalActions;
        this.avaregeWorkTimes = dashboard.avarageWorkTimes;
        this.totalUnsignedRecords = dashboard.totalUnsignedRecords;
        this.totalStuffs = dashboard.totalStuffs;
        this.totalMembers = dashboard.totalMembers;
        this.totalRecords = dashboard.totalRecords;
        this.userInf = dashboard.user_inf;
        this.stuffMemberList = Array.isArray(dashboard.StuffMemberList) ? dashboard.StuffMemberList : [];
        this.unsignMemberList = Array.isArray(dashboard.UnsignMemberList) ? dashboard.UnsignMemberList : [];
        this.hasLoaded = true;
      } catch {
        this.loadError = true;
      } finally {
        this.loading = false;
      }
    }
  },
  data(){
    return{
      loading: false,
      loadError: false,
      hasLoaded: false,
      userInf: null,
      totalActions: 0,
      totalRecords: 0,
      totalMembers: 0,
      totalStuffs: 0,
      totalUnsignedRecords: 0,
      avaregeWorkTimes: 0.0,
      stuffMemberList:[],
      unsignMemberList:[]
    };
  }
}
</script>

<style scoped>
.admin-dashboard {
  box-sizing: border-box;
  width: min(100%, 1400px);
  height: fit-content;
  margin: 0 auto;
  padding: clamp(16px, 3.4vw, 38px);
}

.admin-dashboard__hero {
  display: flex;
  justify-content: space-between;
  align-items: flex-end;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 20px;
  padding: clamp(22px, 4vw, 44px);
  border-radius: 18px;
  color: #fff;
  background: linear-gradient(105deg, #102e25 36%, #102e258c),
    #102e25 url("../assets/courts-login.webp") center 62% / cover no-repeat;
}

.admin-dashboard__hero h1 {
  margin: 0;
  font-size: clamp(26px, 4vw, 42px);
  font-weight: 750;
  letter-spacing: -0.04em;
}

.admin-dashboard__actions {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.admin-dashboard__create, .admin-dashboard__refresh {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 9px 14px;
  border: 1px solid #ffffff64;
  border-radius: 8px;
  background: #102e2580;
  color: #fff;
  font: inherit;
  font-weight: 650;
  cursor: pointer;
}

.admin-dashboard__create {
  border-color: #d5eea5;
  background: #d5eea5;
  color: #193a2b;
}

.admin-dashboard__create:hover {
  background: #e7f7c9;
  color: #193a2b;
}

.admin-dashboard__refresh:hover {
  background: #ffffff24;
}

.admin-dashboard__metrics, .admin-dashboard__details {
  display: grid;
  gap: 14px;
}

.admin-dashboard__metrics {
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 140px), 1fr));
  margin-bottom: 18px;
}

.admin-dashboard__details {
  grid-template-columns: repeat(auto-fit, minmax(min(100%, 238px), 1fr));
  align-items: stretch;
}

.admin-dashboard__tile {
  min-width: 0;
  padding: 18px;
  border: 1px solid #dce7df;
  border-radius: 14px;
  background: #fff;
  box-shadow: 0 4px 20px #183c2308;
}

.admin-dashboard__metric-icon {
  display: grid;
  place-items: center;
  width: 32px;
  height: 32px;
  margin-bottom: 12px;
  border-radius: 8px;
  background: #e8f4eb;
  color: #11684f;
}

.admin-dashboard__tile h2 {
  margin: 0 0 6px;
  color: #486255;
  font-size: 14px;
  font-weight: 650;
}

.admin-dashboard__metrics p {
  margin: 0;
  color: #132b24;
  font-size: 24px;
  font-weight: 750;
  font-variant-numeric: tabular-nums;
}

.admin-dashboard__profile,
.admin-dashboard__ranking {
  margin: 12px 0 0;
  padding: 0;
}

.admin-dashboard__profile div,
.admin-dashboard__ranking li {
  display: flex;
  justify-content: space-between;
  gap: 10px;
  padding: 8px 0;
  border-bottom: 1px solid #edf2ee;
  font-size: 13px;
}

.admin-dashboard__profile dd,
.admin-dashboard__ranking span {
  min-width: 0;
  margin: 0;
  overflow-wrap: anywhere;
}

.admin-dashboard__profile dt,
.admin-dashboard__ranking strong {
  flex-shrink: 0;
  color: #486255;
}

.admin-dashboard__error {
  margin: 0 0 18px;
  padding: 12px 16px;
  border: 1px solid #efd6b0;
  border-radius: 10px;
  background: #fff7e9;
  color: #784b24;
}

.admin-dashboard__refresh:disabled {
  opacity: .65;
  cursor: wait;
}

.admin-dashboard__empty {
  margin: 16px 0 0;
  color: #54665d;
}
</style>