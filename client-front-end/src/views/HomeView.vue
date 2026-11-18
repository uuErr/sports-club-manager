<template>
  <div class="club-shell">
    <van-nav-bar title="体育俱乐部" fixed placeholder />
    <main class="club-shell__content">
      <router-view />
    </main>
    <van-tabbar v-model="active" @change="onChange" class="club-shell__nav" fixed placeholder>
      <van-tabbar-item icon="list-switch">活动</van-tabbar-item>
      <van-tabbar-item icon="records-o">报名记录</van-tabbar-item>
      <van-tabbar-item icon="tosend">转让与候补</van-tabbar-item>
      <van-tabbar-item icon="user-circle-o">我的账号</van-tabbar-item>
    </van-tabbar>
  </div>
</template>

<script>
export default {
  data(){
    return{
      active: 0
    };
  },
  created(){
    this.$memberVerify();
    switch (this.$route.path){
      case '/main/action':
        this.active = 0;
        break;
      case '/main/records':
        this.active = 1;
        break;
      case '/main/others':
        this.active = 2;
        break;
      case '/main/membership':
        this.active = 3;
    }
  },
  methods:{
    onChange(){
      switch(this.active){
        case 0:
          this.$router.push('/main/action');
          break;
        case 1:
          this.$router.push('/main/records');
          break;
        case 2:
          this.$router.push('/main/others');
          break;
        case 3:
          this.$router.push('/main/membership');
          break;
      }
    }
  }
}
</script>