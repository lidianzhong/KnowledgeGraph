<template>
  <div>
    <div>
      <div class="content">
        <el-input type="textarea" v-model="fileDetail.content"> </el-input>
      </div>
      <div class="footer">
        <div class="text">
          <p>上传者: {{ fileDetail.user_name }}</p>
          <p>最后更新时间: {{ fileDetail.update_time }}</p>
        </div>
        <div class="save">
          <el-button type="primary" @click="save">保存</el-button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { getFileDetail, updateFile } from "api/file";
export default {
  name: "ChangeFile",
  components: {},
  data() {
    return {
      fileDetail: {},
    };
  },
  computed: {},
  methods: {
    changeFile() {
      updateFile({
        document_id: this.fileDetail.document_id,
        content: this.fileDetail.content,
      }).then((res) => {
        if (res.status == 200) {
          this.$message.success("修改成功");
          this.getFileDetail();
        }
      });
    },
    getFileDetail() {
      getFileDetail({ document_id: this.$route.query.id }).then((res) => {
        this.fileDetail = res.data.data;
      });
    },
    save() {
      this.changeFile();
    },
  },
  created() {
    this.getFileDetail();
  },
};
</script>
<style scoped>
.content {
  margin: 0 auto;
  margin-top: 50px;
  width: 60%;
  /* height: 800px;; */
}
.el-textarea {
  height: 610px;
}
.el-textarea :deep(.el-textarea__inner) {
  height: 610px;
}
.el-textarea {
  font-size: 18px;
}
.footer {
  display: flex;
}
.text {
  margin-left: 295px;
  margin-top: 10px;
  font-size: 14px;
}
.save{
  margin-left: 570px;
  margin-top: 15px;
  background-color: #5aa4ae;
  border-radius: 5px;
}
.save :deep(.el-button--primary) {
  background-color: #5aa4ae;
  border-radius: 5px;
}
</style>
