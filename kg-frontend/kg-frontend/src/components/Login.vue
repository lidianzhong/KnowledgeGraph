<template>
  <div class="body">
    <div class="fixed">
      <div class="form-demo">
        <input
          type="checkbox"
          style="display: none"
          id="change"
          @click="_switch"
        />
        <label for="change">&lt;&lt;</label>

        <div class="turn">
          <div class="over">
            <form action="" class="login">
              <h1>欢迎回来</h1>
              <input
                type="text"
                v-model="email"
                placeholder="请输入邮箱"
                class="input"
              />
              <input
                type="password"
                v-model="password"
                placeholder="请输入密码"
                class="input"
              />
              <div class="btn input" @click="login">登录</div>
            </form>
            <form action="" class="sign">
              <div class="empty"></div>
              <h1>加入我们</h1>
              <input
                type="text"
                v-model="email"
                placeholder="请输入邮箱"
                class="input first"
              />
              <input
                type="text"
                v-model="username"
                placeholder="请输入用户名"
                class="input"
              />
              <input
                type="password"
                v-model="password"
                placeholder="请输入密码"
                class="input"
              />
              <input
                type="text"
                v-model="code"
                placeholder="请输入验证码"
                class="input verify"
              />
              <div class="btn input" @click="register">注册</div>
              <div
                class="code el-icon-message"
                v-if="showTime === null"
                @click="sendCode"
              ></div>
              <div class="code data" v-else>{{ showTime }}</div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { login, register, sendCode } from "api/user";
export default {
  name: "Login",
  components: {},
  data() {
    return {
      email: "",
      password: "",
      username: "",
      code: "",
      timeCounter: null, //计时器
      showTime: null, //剩余时间
    };
  },
  methods: {
    async login() {
      const res = await login({ email: this.email, password: this.password });
      this.$store.commit("updateUser", res.data.data);
      this.$message.success("登录成功");
      this.$router.push("/main/upload");
    },
    async register() {
      const res = await register({
        email: this.email,
        password: this.password,
        username: this.username,
        verificationCode: this.code,
      });
      if (res.status == 200) {
        this.login();
      }
    },
    _switch() {
      this.email = "";
      this.password = "";
      this.username = "";
    },
    sendCode() {
      if (this.showTime != null) {
        return;
      }
      if (this.email == "") {
        this.$message.error("请输入邮箱");
        return;
      }
      sendCode({ email: this.email }).then((res) => {
        this.$message.success("验证码已发送");
        this.countDown(300);
      });
    },
    // 倒计时显示处理
    countDownText(s) {
      this.showTime = `${s}s`;
    },
    // 倒计时60秒
    countDown(times) {
      const self = this;
      // 时间间隔 1秒
      const interval = 1000;
      let count = 0;
      self.timeCounter = setTimeout(countDownStart, interval);
      function countDownStart() {
        if (self.timeCounter == null) {
          return false;
        }
        count++;
        self.countDownText(times - count + 1);
        if (count > times) {
          clearTimeout(self.timeCounter);
          self.showTime = null;
        } else {
          self.timeCounter = setTimeout(countDownStart, interval);
        }
      }
    },
  },
};
</script>
<style scoped>
.body {
  background-color: #abdde8;

  overflow: hidden;
  margin: 0;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  background: url(assets/img/background7.jpg) no-repeat center center;
  background-size: cover;
}
.code {
  position: absolute;
  top: 280px;
  left: 300px;
  color: #4aa4ad;
  font-size: 40px;
  transform: translate(-50%);
  cursor: pointer;
}

.fixed {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  opacity: 0.8;
}

.form-demo {
  position: relative;
  width: 400px;
  height: 600px;
  opacity: 0.8;
}

/* 切换按钮 */
#change:checked+label,
/* +用来选择同级后面最近的元素  */
#change:not(:checked)+label {
  color: white;
  width: 10px;
  padding: 8px 0;
  font-size: 40px;
  font-weight: 600;
  position: absolute;
  top: 112px;
  left: -70px;
  transform: translate(-50%);
  /* border-radius: 8px; */
  cursor: pointer;
  /* text-align: center; */
}

/* 旋转体 */
.turn {
  width: 100%;
  height: 400px;
  position: absolute;
  top: 100px;
  perspective: 800px;
  /* 旋转的时候的透视效果 */
}

.over {
  width: 100%;
  height: 100%;
  transform-style: preserve-3d;
  transition: all 1.6s ease;
  /* 旋转持续时间 */
  /* ease是慢快慢 */
}

#change:checked ~ .turn .over {
  transform: rotateY(180deg);
}

form {
  position: absolute;
  background-color: #fcfbfa;
  height: 100%;
  border-radius: 8px;
  transform-style: preserve-3d;
  text-align: center;
}

.sign {
  transform: rotateY(180deg);
  position: relative;
}

h1,
h2 {
  color: #1f2029;
  user-select: none;
}

h1 {
  margin-top: 38px;
  transform-style: preserve-3d;
  transform: translate3d(0, 0, 1px);
}
.input {
  /* background-color: #4E495D; */
  width: 70%;
  height: 48px;
  line-height: 48px;
  /* border-radius: 8px; */
  margin-bottom: 20px;
  margin-top: 12px;
  padding: 0;
  font-size: 22px;
  /* color: #c4c3ca; */
  font-weight: 500;
  outline: none;
  border: none;
  /* box-shadow: 0 4px 8px 0 rgba(78, 73, 79, .5); */
  transform-style: preserve-3d;
  transform: translate3d(0, 0, 1px);
  border: none;
  border-bottom: 2px solid silver;
}
.login .input {
  /* background-color: #4E495D; */
  width: 70%;
  height: 48px;
  /* border-radius: 8px; */
  margin-bottom: 20px;
  margin-top: 12px;
  padding: 0;
  font-size: 22px;
  /* color: #c4c3ca; */
  font-weight: 500;
  outline: none;
  border: none;
  /* box-shadow: 0 4px 8px 0 rgba(78, 73, 79, .5); */
  transform-style: preserve-3d;
  transform: translate3d(0, 0, 1px);
  border: none;
  border-bottom: 2px solid silver;
}

.login .input:nth-child(-n + 2) {
  margin: 20px 0;
}

.sign .input {
  /* background-color: #4E495D; */
  width: 70%;
  height: 40px;
  /* background-color: #59c2c5; */
  /* border-radius: 8px; */
  /* margin-bottom: 20px; */
  margin-top: 1px;
  padding: 0;
  font-size: 22px;
  /* color: #c4c3ca; */
  font-weight: 500;
  outline: none;
  border: none;
  /* box-shadow: 0 4px 8px 0 rgba(78, 73, 79, .5); */
  transform-style: preserve-3d;
  transform: translate3d(0, 0, 1px);
  border: none;
  border-bottom: 2px solid silver;
}
.sign .btn {
  line-height: 40px;
}
.sign h1 {
  margin-top: 20px !important;
}
.login .btn {
  margin-top: 20px;
}
.empty {
  height: 15px;
}
.btn {
  background-color: #59c2c5;
  border: none;
  width: 280px;
  font-size: 24px;
  font-weight: 600;
  padding: 6px 0;
  color: white;
  border-radius: 8px;
  margin-top: 15px;
  margin-left: 60px;
  cursor: pointer;
  text-align: center;
}
.first {
  margin-top: 20px !important;
}
.verify {
  margin-left: -78px !important;
  width: 50% !important;
  /* background-color: #59c2c5; */
}
.data {
  font-size: 20px;
  color: #4aa4ad;
  top: 290px;
}
</style>
