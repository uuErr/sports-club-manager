<template>
  <div class="club-shell">
    <van-nav-bar title="值班管理" fixed placeholder />
    <main class="club-shell__content">
      <router-view />
    </main>
    <van-tabbar v-model="active" @change="onChange" class="club-shell__nav" fixed placeholder>
      <van-tabbar-item icon="calendar-o">值班安排</van-tabbar-item>
      <van-tabbar-item icon="scan">核验并签到</van-tabbar-item>
      <van-tabbar-item icon="user-circle-o">账号</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script>
export default {
  data(){
    return {
      active: 0
    };
  },
  created(){
    this.$staffVerify();
    switch (this.$route.path){
      case '/staff/work':
        this.active = 0;
        break;
      case '/staff/membership':
        this.active = 2;
    }
  },
  methods: {
    onChange(){
      switch(this.active){
        case 0:
          this.$router.push('/staff/work');
          break;
        case 1:
          this.active = 0;
          this.$router.push('/staff/scan');
          break;
        case 2:
          this.$router.push('/staff/membership');
          break;
      };
    }
  }
};
</script>

<style scoped lang="scss">

</style>