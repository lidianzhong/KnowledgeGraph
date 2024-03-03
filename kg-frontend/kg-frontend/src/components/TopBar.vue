<template>
  <div class="top-container">
    <el-dropdown class="avatar">
      <!-- <img src="https://github.githubassets.com/favicons/favicon.svg" /> -->
      <span>{{ this.$store.getters.getUser }} ({{ identity }})</span>
      <el-dropdown-menu slot="dropdown" class="menu">
        <el-dropdown-item @click.native="layout" icon="el-icon-circle-close">
          退出登录</el-dropdown-item
        >
        <el-dropdown-item @click.native="layoff" icon="el-icon-delete"
          >&nbsp;注销账号</el-dropdown-item
        >
      </el-dropdown-menu>
    </el-dropdown>

    <div class="username">HZAU知识工程与元学习团队</div>
  </div>
</template>
<script>
import { layoff, layout } from "api/user";
export default {
  name: "TopBar",
  components: {},
  data() {
    return {
      search: "",
      avatarUrl: "",
      show: false,
    };
  },
  computed: {
    identity() {
      return this.$store.getters.getIdentity ? "管理员" : "普通用户";
    },
  },
  methods: {
    layout() {
      this.$store.commit("clearUser");
      this.$message.success("退出成功");
      this.$router.replace("/login");
    },
    layoff() {
      this.$alert("确定要注销您的账号吗？", "提示", {
        confirmButtonText: "确定",
        callback: (action) => {
          if (action == "confirm") {
            layout().then((res) => {
              if (res.status == 200) {
                this.$store.commit("clearUser");
                this.$message.success("注销成功");
                this.$router.replace("/login");
              }
            });
          }
        },
      });
    },
  },
};
</script>
  <style scoped>
.top-container {
  width: 100%;
  height: 60px;
  background-color: #5AA4AE;
  color:#181818
;
}
.avatar {
  position: absolute;
  top: 5px;
  right: 100px;
  cursor: pointer;
  width: 120px;
  height: 50px;
  line-height: 50px;
  color: #fff;
  /* background-color: #fff; */
}
.avatar img {
  width: 50px;
  height: 50px;
}
.username {
  float: left;
  margin: 20px 0 0 30px;
  color: #fff;
}
.layout {
  float: right;
  margin: 13px 20px 0 0;
  cursor: pointer;
  color: #5e85bf;
  border-radius: 20px;
  width: 80px;
  text-align: center;
  font-size: 14px;
}
</style>
  
