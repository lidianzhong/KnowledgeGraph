<template>
  <div>
    <nav-bar></nav-bar>
    <div class="main">
      <keep-alive>
        <router-view></router-view>
      </keep-alive>
      <!-- <router-view></router-view> -->
    </div>
  </div>
</template>
<script>
import NavBar from "components/NavBar.vue";
export default {
  name: "Index",
  components: {
    NavBar,
  },
  data() {
    return {};
  },
  methods: {},
};
</script>
<style scoped>
.main {
  /* 上，右，下，左 */
  margin: 80px 100px 0px 200px;
  margin-top: 80px;
  margin-left: 230px;
  height: 665px;
  /* overflow-y: scroll; */
}
</style>
