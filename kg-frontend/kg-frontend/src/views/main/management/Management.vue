<template>
  <div class="users">
    <div class="empty"></div>
    <div class="table">
      <el-table
        :data="userList"
        border
        max-height="500px"
        class="tableClass"
        style="width: 100%"
        tooltip-effect="light"
        v-loading="loading"
      >
        <el-table-column
          prop="username"
          label="用户名"
          :show-overflow-tooltip="Boolean('true')"
          width="300px"
        >
        </el-table-column>
        <el-table-column
          prop="email"
          label="邮箱"
          :show-overflow-tooltip="Boolean('true')"
          width="350px"
        ></el-table-column>
        <el-table-column
          prop="role"
          label="身份"
          :show-overflow-tooltip="Boolean('true')"
          width="150px"
        ></el-table-column>
        <el-table-column align="center">
          <template slot-scope="scope">
            <span
              v-show="scope.row.role == '普通用户'"
              class="el-icon-more"
              @click="handle($event, scope.row)"
            ></span>
            &nbsp;&nbsp;&nbsp;
            <span
              v-show="scope.row.role == '普通用户'"
              class="el-icon-key"
              @click="guardAdmin($event, scope.row)"
            >
            </span>
            &nbsp;&nbsp;&nbsp;
            <span
              v-show="scope.row.role == '普通用户'"
              class="el-icon-delete"
              @click="deleteUser($event, scope.row)"
            >
            </span>
          </template>
        </el-table-column>
      </el-table>
    </div>

    <el-pagination
      @size-change="handleSizeChange"
      @current-change="handleCurrentChange"
      :current-page="params.page"
      :page-size="params.pageSize"
      layout="prev, pager, next"
      :total="total"
      class="pagination"
    >
    </el-pagination>
    <div class="modal" v-show="visible">
      <div class="el-icon-close close-settings" @click="close"></div>
      <div class="modal-mask"></div>
      <div class="model-container">
        <h2>权限设置</h2>
        <div class="username">用户:&nbsp;&nbsp;{{ username }}</div>
        <div class="permission" v-loading="loading_permission">
          <div class="switch" v-for="(item, index) in permissions" :key="index">
            <div class="permission_name">
              {{ permission_name[item.permission_id - 1] }}
            </div>
            <el-switch
              v-model="item.is_allowed"
              active-color="#5e85bf"
              inactive-color="#eef0f4"
            >
            </el-switch>
          </div>
        </div>
        <div class="btn">
          <el-button type="primary" class="cancel" @click="close"
            >取消</el-button
          >
          <el-button type="primary" class="confirm" @click="save"
            >确定</el-button
          >
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import {
  getPermission,
  updatePermission,
  guardAdmin,
  deleteUser,
} from "api/permission";
import { getUserList } from "api/user";
export default {
  name: "Management",
  components: {},
  data() {
    return {
      userList: [],
      permissions: [],
      permission_name: ["修改文献", "删除文献", "修改问答对", "删除问答对"],
      total: 100,
      params: {
        page: 1,
        pageSize: 9,
      },
      visible: false,
      loading: true,
      username: "",
      user_id: "",
      permission_id: [],
      is_allowed: [],
      loading_permission: true,
    };
  },
  computed: {},
  methods: {
    getIdentity(role) {
      return role ? "管理员" : "普通用户";
    },
    updatePermission() {
      this.permission_id = [1, 2, 3, 4];
      this.permissions.forEach((item) => {
        this.is_allowed.push(item.is_allowed ? 1 : 0);
      });
      updatePermission({
        user_id: this.user_id,
        permission_id: this.permission_id.toString(),
        is_allowed: this.is_allowed.toString(),
      }).then((res) => {
        this.$message({
          message: "修改成功",
          type: "success",
        });
      });
    },
    guardAdmin(event, row) {
      this.$confirm(
        "确定要授予该用户管理员身份？此操作将使该用户与你等同权限",
        "提示",
        {
          confirmButtonText: "确定",
          cancelButtonText: "取消",
          type: "warning",
        }
      )
        .then(() => {
          guardAdmin({ user_id: row.user_id }).then((res) => {
            this.$message({
              message: "授权成功",
              type: "success",
            });
          });
          this.getUserList();
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消授权",
          });
        });
    },
    handleSizeChange(val) {
      this.params.pageSize = val;
      this.loading = true;
      this.getUserList();
    },
    handleCurrentChange(val) {
      this.params.page = val;
      this.loading = true;
      this.getUserList();
    },
    getUserList() {
      getUserList(this.params).then((res) => {
        this.userList = res.data.data.current_page_data;
        this.total =
          res.data.data.pagination.total_pages * this.params.pageSize;
        console.log(this.userList);
        this.loading = false;
        this.userList.forEach((item) => {
          item.role = this.getIdentity(item.role);
        });
      });
    },
    getPermission(userId, userName) {
      getPermission({ user_id: userId }).then((res) => {
        this.permissions = res.data.data;
        this.username = userName;
        this.user_id = userId;
        this.loading_permission = false;
      });
    },
    close() {
      this.visible = false;
    },
    handle(event, row) {
      event.stopPropagation();
      this.getPermission(row.user_id, row.username);
      this.visible = true;
    },
    save() {
      this.updatePermission();
      this.close();
    },
    deleteUser(event, row) {
      this.$confirm("确定要注销掉该用户账号？", "提示", {
        confirmButtonText: "确定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          deleteUser({ user_id: row.user_id }).then((res) => {
            if (res.status == 200) {
              this.$message({
                message: "注销成功",
                type: "success",
              });
              this.getUserList();
            }
          });
        })
        .catch(() => {
          this.$message({
            type: "info",
            message: "已取消注销",
          });
        });
    },
  },

  created() {
    this.getUserList();
  },
};
</script>
  <style scoped>
.username {
  margin-top: 10px;
  text-align: left;
  /* margin-left: 20px; */
}
.permission {
  margin-top: 30px;
  /* background-color: #5e85bf; */
  width: 200px;
}
.switch {
  /* background-color: #5e85bf; */
  width: 150px;
  height: 40px;
  display: flex;
  /* margin-top: 10px; */
}
.switch .permission_name {
  width: 70%;
}
.btn {
    position: relative;
    width: 180px;
    height: 80px;
    /* background-color: #5e85bf; */
    margin-left: 280px;
    margin-top: -80px;
}
.cancel {
  position: absolute;
  top: 30px;
  left:10px;
}
.confirm {
  position: absolute;
  top: 30px;
  left: 90px;
}
.users {
  margin-left: 20px;
  height: 100%;
}
div :deep(.el-table--border)::after,
div :deep(.el-table--group)::after,
div :deep(.el-table)::before {
  background-color: transparent;
}
.empty {
  height: 50px;
}
.table {
  width: 1000px;
  margin: 0 auto;
  cursor: pointer;
  height: 500px;
}
.el-pagination {
  text-align: center;
}
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
  z-index: -1;
}

.model-container {
  /* position: absolute; */
  width: 500px;
  height: 300px;
  top: 800px;
  max-width: 800px;
  background-color: #fff;
  border-radius: 10px;
  padding: 20px;
  z-index: 999;
}
h2 {
  text-align: center;
}
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
  z-index: -1;
}

.close-settings {
  position: absolute;
  top: 230px;
  right: 500px;
  font-size: 20px;
  z-index: 9999;
  cursor: pointer;
}
.close-settings :hover {
  color: #5e85bf;
}
h3 {
  margin-left: 55px;
}
.settings-save {
  margin-top: 20px;
  cursor: pointer;
  margin-left: 40px;
  border-radius: 20px;
  /* background-color: #5e85bf; */
  color: #5e85bf;
}
.el-icon-more {
  cursor: pointer;
  font-size: 18px;
}
.el-icon-more:hover {
  color: #5e85bf;
}
.el-icon-key:hover {
  color: #5e85bf;
}
.el-icon-delete:hover {
  color: #5e85bf;
}
</style>
  