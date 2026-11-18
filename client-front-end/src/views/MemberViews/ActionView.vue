<template>
  <van-toast v-model:show="loading" type="loading" overlay="true" duration="0"
             forbid_click="true" message="加载中…"></van-toast>
  <Vcode :show="isShow"
         slider-text="拖动滑块完成验证"
         fail-text="验证失败，请重试"
         success-text="验证通过"
         :range="5"
         @success="onSubmit"
         @close="close"
  />
  <h1 class="club-page-title">可报名活动</h1>
  <van-pull-refresh
      pulling-text="下拉刷新…"
      loosing-text="松开刷新…"
      loading-text="加载中…"
      :success-text="loadError ? '' : '刷新成功'"
      v-model="isLoading"
      @refresh="onRefresh"
  >
    <van-empty v-if="loadError" description="活动加载失败，请重试">
      <van-button size="small" type="primary" :disabled="isLoading" @click="onRefresh">重试</van-button>
    </van-empty>
    <van-empty v-else-if="!isLoading && actionList.length === 0" description="暂无可报名的活动" />
    <div class="club-card-grid">
      <article v-for="item in actionList" :key="item.id" class="club-activity">
        <header class="club-activity__header">
          <h2 class="club-activity__name">{{ item.title }}</h2>
          <span
            class="club-activity__availability"
            :class="{ 'club-activity__availability--full': item.remaining_slots === 0 }"
          >
            {{ item.remaining_slots === 0 ? '已满员' : '剩余 ' + item.remaining_slots + ' 个名额' }}
          </span>
        </header>
        <ul class="club-activity__details">
          <li><van-icon name="clock-o" aria-hidden="true" /> <span>{{ item.date }} · {{ item.time_range }}</span></li>
          <li><van-icon name="location-o" aria-hidden="true" /> <span>{{ item.place }}</span></li>
        </ul>
        <div class="club-activity__capacity">
          <span>已报名 {{ item.registered_count }} / {{ item.max_num }} 人</span>
          <progress v-if="item.max_num > 0" :max="item.max_num" :value="item.registered_count" aria-label="报名进度" />
        </div>
        <footer class="club-activity__footer">
          <div class="club-activity__borrow">
            借用球拍
            <van-switch v-model="borrow" size="20px" aria-label="借用球拍" />
          </div>
          <van-button
            class="club-activity__action"
            :class="{ 'club-activity__action--wait': item.remaining_slots === 0 }"
            :disabled="buttonDisabled || isLoading"
            type="primary"
            size="small"
            @click="onClick(item)"
          >
            {{ item.remaining_slots === 0 ? '加入候补' : '报名' }}
          </van-button>
        </footer>
      </article>
    </div>
  </van-pull-refresh>
</template>

<script>
import Cookies from "js-cookie";
import { showConfirmDialog, showFailToast, showSuccessToast } from "vant";

export default {
  created(){
    this.$memberVerify();
    this.onRefresh();
  },
  data(){
    return{
      borrow: false,
      isLoading: false,
      refreshing: false,
      loadError: false,
      isShow: false,
      buttonDisabled: false,
      loading: false,
      currentId: -1,
      joinWaitlist: false,
      actionList: []
    };
  },
  methods: {
    async onRefresh() {
      if (this.refreshing) return;
      this.refreshing = true;
      this.isLoading = true;
      this.loadError = false;
      try {
        const { data } = await this.$http.post('/action/queryAction', null, {
          params: { token: Cookies.get('token') }
        });
        if (data.status === 1 && Array.isArray(data.data)) {
          this.actionList = data.data;
        } else {
          this.loadError = true;
        }
      } catch {
        this.loadError = true;
      } finally {
        this.refreshing = false;
        this.isLoading = false;
      }
    },
    onClick(item) {
      this.currentId = item.id;
      this.joinWaitlist = item.remaining_slots === 0;
      this.isShow = true;
    },
    close() {
      this.isShow = false;
    },
    async onSubmit() {
      if (this.buttonDisabled) return;
      this.isShow = false;
      this.buttonDisabled = true;
      const params = {
        token: Cookies.get('token'),
        action_id: this.currentId,
        borrow: this.borrow
      };

      try {
        if (this.joinWaitlist) {
          await this.confirmWaitlist(params);
          return;
        }

        this.loading = true;
        const { data } = await this.$http.post('/action/attendAction', null, { params, retry: 0 });
        this.loading = false;
        switch (data.status) {
          case -2:
            this.$memberVerify();
            break;
          case -1:
            showFailToast("当前账号无法直接报名活动。");
            break;
          case 0:
            showFailToast("活动报名已截止。");
            await this.onRefresh();
            break;
          case 1:
            showFailToast("你已报名或已加入候补，请勿重复操作。");
            break;
          case 2:
            await this.onRefresh();
            await this.confirmWaitlist(params);
            break;
          case 3:
            showSuccessToast("报名成功，请在「报名记录」中查看详情，并准时参加。");
            await this.onRefresh();
            break;
          default:
            showFailToast("报名失败，请重试。");
        }
      } catch {
        showFailToast("网络连接失败，请刷新后重试。");
      } finally {
        this.loading = false;
        this.buttonDisabled = false;
      }
    },
    async confirmWaitlist(params) {
      try {
        await showConfirmDialog({
          message: '活动名额已满，是否加入候补？报名期间，如有人取消，空缺名额将按候补顺序分配。报名截止后，可在「报名记录」中查看获得的名额。',
          confirmButtonText: '加入候补',
          cancelButtonText: '取消'
        });
      } catch {
        return;
      }

      this.loading = true;
      const { data } = await this.$http.post('/waiting/waitCreate', null, { params, retry: 0 });
      this.loading = false;
      switch (data.status) {
        case -2:
          this.$memberVerify();
          break;
        case -1:
          showFailToast("当前账号无法加入候补。");
          break;
        case 0:
          showFailToast("活动报名已截止。");
          await this.onRefresh();
          break;
        case 1:
          showFailToast("活动已有空缺名额，可以重新报名。");
          await this.onRefresh();
          break;
        case 2:
          showFailToast("你已报名或已加入候补，请勿重复操作。");
          break;
        case 3:
          showSuccessToast("已加入候补，请在「转让与候补」中查看记录。");
          break;
        default:
          showFailToast("加入候补失败，请重试。");
      }
    }
  }
}
</script>