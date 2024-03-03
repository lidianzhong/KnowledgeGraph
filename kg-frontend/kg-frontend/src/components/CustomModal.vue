<template>
  <div v-if="visible" class="modal">
    <div class="modal-mask"></div>
    <div class="modal-container">
      <div class="el-icon-close close-detail" @click="close"></div>
      <div class="modal-body">
        <span class="title">文献名：{{ this.data.title }}</span>
        <span class="author">上传者：{{ this.data.user_name }}</span>
        <span class="create_time">上传时间：{{ this.data.create_time }}</span>
        <span class="update_time"
          >最后更新时间：{{ this.data.update_time }}</span
        >

        <div
          v-if="keywords"
          contenteditable="true"
          placeholder=""
          v-html="highlightText(this.data.content)"
          class="content"
        ></div>
        <el-input
          v-else
          type="textarea"
          :only-read="true"
          :readonly="true"
          class="content"
          v-model="this.data.content"
        >
        </el-input>
      </div>
      <div class="modal-footer">
        <button class="modal-btn" @click="change">修改</button>
      </div>
    </div>
  </div>
</template>
  
  <script>
export default {
  name: "CustomModal",
  props: {
    visible: Boolean,
    data: Object,
    keywords: Array,
  },
  data() {
    return {};
  },
  methods: {
    close() {
      this.$emit("close");
    },
    change() {
      this.$router.push({
        path: "/changeFile",
        query: {
          id: this.data.document_id,
        },
      });
    },
    highlightText(text) {
      // 将关键词用 <span> 标签包裹并添加样式
      const regex = new RegExp(this.keywords.join("|"), "gi");
      const highlightedText = text.replace(
        regex,
        `<span style="color: red;">$&</span>`
      );
      return `<div style="white-space: pre-line;">${highlightedText}</div>`;
    },
  },
  watch: {},
};
</script>
  
  <style scoped>
.modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-mask {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
}

.modal-container {
  width: 80%;
  height: 70%;
  max-width: 800px;
  background-color: #fff;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.3);
  padding: 20px;
  z-index: 999;
}

.modal-title {
  margin: 0;
}

.modal-close-btn {
  border: none;
  background-color: transparent;
  font-size: 20px;
  cursor: pointer;
  outline: none;
}

.modal-body {
  margin-top: 20px;
  margin-bottom: 20px;
  position: relative;
}

.modal-footer {
  position: relative;
  margin-top: 430px;
  margin-left: 50px;
}

.modal-footer button {
  border-radius: 10px;
  background-color: #5aa4ae;
  float: right;
  right: 100px;
}
.modal-btn {
  margin-left: 10px;
  padding: 5px 10px;
  border-radius: 3px;
  border: none;
  color: #fff;
  background-color: #5aa4ae;
  cursor: pointer;
  outline: none;
}

.modal-btn:hover {
  background-color: #5aa4ae;
}

.close-detail {
  position: absolute;
  right: 24%;
  top: 125px;
  font-size: 20px;
  cursor: pointer;
}
.title {
  position: absolute;
  top: -10px;
  left: 20px;
}
.author {
  position: absolute;
  top: 20px;
  left: 20px;
}
.field {
  position: absolute;
  top: 50px;
  left: 20px;
}
.content {
  position: absolute;
  overflow-y: scroll;
  top: 70px;
  width: 94%;
  height: 315px;
  left: 3%;
}
.el-textarea {
  height: 320px;
}
.el-textarea :deep(.el-textarea__inner) {
  height: 300px;
}
.create_time {
  position: absolute;
  top: 410px;
  left: 20px;
  font-size: 12px;
}
.update_time {
  position: absolute;
  top: 425px;
  left: 20px;
  font-size: 12px;
}
.el-textarea {
  font-size: 16px;
}
</style>
  