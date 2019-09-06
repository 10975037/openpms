<template>
  <div class="app-container"
       style="margin-top:1%;margin-left:1%;margin-right:1%;">

    <div class="filter-container">
      <!-- 搜索框 -->
      <el-input placeholder='Name'
                v-model="listQuery.key"
                style="width: 200px;"
                class="filter-item" />
      <!-- 创建组 -->
      <el-button class="el-icon-plus"
                 type="primary"
                 @click.prevent="handleDialog(null,'创建组')"></el-button>
    </div>
    <br>

    <!-- 表格 -->
    <el-table :data="searchList.slice((listQuery.page-1)*listQuery.limit,listQuery.page*listQuery.limit)"
              v-loading="listLoading"
              element-loading-text="Loading"
              border
              fit
              mini-witdh
              highlight-current-row
              :stripe="true">

      <el-table-column align="left"
                       width="150"
                       label="组名">
        <template slot-scope="scope">
          <span>{{ scope.row.group_name }}</span>
        </template>
      </el-table-column>

      <el-table-column align="left"
                       width="150"
                       label="所属系统">
        <template slot-scope="scope">
          <span>{{ scope.row.app_name.app_name }}</span>
        </template>
      </el-table-column>

      <el-table-column align="center"
                       width="300"
                       label="说明">
        <template slot-scope="scope">
          <span>{{ scope.row.remark }}</span>
        </template>
      </el-table-column>

      <el-table-column label='操作'
                       align="center"
                       class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <el-button type="primary"
                     size="mini"
                     class="icon iconfont icon-moban"
                     @click="handleDialog(scope.row.id,'成员分配')"></el-button>
          <el-button type="primary"
                     size="mini"
                     class="icon iconfont icon-ic_opt_feature"
                     @click="handleDialog(scope.row.id,'权限分配')"></el-button>
          <el-button type="primary"
                     size="mini"
                     class="el-icon-document"
                     @click="handleMenu(scope.row.id, scope.row.application, scope.row.perm_menu)"></el-button>
          <el-button type="danger"
                     size="mini"
                     icon="el-icon-delete"
                     @click="handleDelete(scope.row.id)"></el-button>

        </template>
      </el-table-column>

    </el-table>

    <!-- 分页 -->
    <div class="pagination-container"
         style="margin-top:10px">
      <el-pagination :current-page="listQuery.page"
                     :page-sizes="[10,20,30,50]"
                     :page-size="listQuery.limit"
                     :total="total"
                     background
                     layout="total, sizes, prev, pager, next, jumper"
                     @size-change="handleSizeChange"
                     @current-change="handleCurrentChange" />
    </div>

    <!-- 弹出对话框 -->
    <!-- 创建组 -->
    <el-dialog title="创建组"
               :visible.sync="group"
               :before-close="resetForm">
      <el-form :model="form"
               :rules="rules"
               ref="form">
        <el-form-item label="选择系统"
                      :label-width="formLabelWidth"
                      prop="app_selected">
          <el-select v-model="form.app_selected"
                     style="width:200px;"
                     placeholder="请选择">
            <el-option v-for="item in apps_data"
                       :key="item.value"
                       :label="item.label"
                       :value="item.value">
            </el-option>
          </el-select>
        </el-form-item>

        <el-form-item label="组名"
                      prop="group_name"
                      :label-width="formLabelWidth">
          <el-input :disabled="!form.app_selected"
                    v-model="form.group_name"
                    placeholder="请输入内容"
                    style="width:200px;"></el-input>
        </el-form-item>

        <el-form-item label="说明"
                      :label-width="formLabelWidth">
          <el-input type="textarea"
                    style="width:200px;"
                    :autosize="{ minRows: 2, maxRows: 4}"
                    :rows="2"
                    placeholder="请输入内容"
                    v-model="form.remark">
          </el-input>
        </el-form-item>
      </el-form>
      <div slot="footer"
           class="dialog-footer">
        <el-button @click="resetForm()">Cancel</el-button>
        <el-button type="primary"
                   @click="addSubmit('form')">OK</el-button>
      </div>
    </el-dialog>

    <!-- 成员分配 -->
    <el-dialog title="成员分配"
               :before-close="resetForm"
               :visible.sync="users">
      <el-transfer filterable
                   v-loading="loading"
                   :filter-method="filterMethod"
                   :titles="['待选择', '已选择']"
                   filter-placeholder="请输入姓名"
                   v-model="users_selected"
                   :data="users_data">
      </el-transfer>

      <div slot="footer"
           class="dialog-footer">
        <el-button @click="resetForm()">Cancel</el-button>
        <el-button type="primary"
                   @click="onSubmit()">OK</el-button>
      </div>
    </el-dialog>

    <!-- 权限分配 -->
    <el-dialog title="权限分配"
               :visible.sync="perms">
      <cus-transfer filterable
                    v-loading="loading"
                    :filter-method="filterMethod"
                    :titles="['待选择', '已选择']"
                    filter-placeholder="请输入权限名"
                    v-model="perms_selected"
                    :data="perms_data">
      </cus-transfer>
      <div slot="footer"
           class="dialog-footer">
        <el-button @click="resetForm()">Cancel</el-button>
        <el-button type="primary"
                   @click="onSubmit('form')">OK</el-button>
      </div>

    </el-dialog>

    <!-- Menu allocation Added by zongkai -->
    <el-dialog title="菜单分配"
               :visible.sync="menuVisable"
               v-loading="menuLoading"
               width="20%"
               :before-close="menuClose">
      <el-form ref="form"
               :model="mForm">
        <el-form-item>
          <el-select v-model="mForm.m_id"
                     placeholder='Menu'
                     clearable
                     style="width: 90%"
                     class="filter-item">
            <el-option v-for="item in menuList"
                       :key="item.id"
                       :label="item.p_menu_name"
                       :value="item.id">
            </el-option>
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button @click="resetForm()">Cancel</el-button>
          <el-button type="primary"
                     @click="menuSubmit()">OK</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { getUsers } from '@/api/pms'
import { getPerms } from '@/api/pms'
import { getAppsSelector } from '@/api/pms'
import { createGroup } from '@/api/pms'
import { getGroups } from '@/api/pms'
import { updateGroup } from '@/api/pms'
import { deleteGroup } from '@/api/pms'
import CusTransfer from '@/components/custom/transfer/index'
import { getPermMenuWithApp } from '@/api/pms'
import { groupUniqueCheck } from '@/api/pms'

export default {
  components: {
    CusTransfer
  },
  data() {
    var group_unique_check = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('不能为空'))
      }
      groupUniqueCheck(this.form.app_selected, value).then(response => {
        if (response.data !== 0) {
          return callback(new Error('组已经存在'))
        } else {
          callback()
        }
      })
    }
    return {
      users_data: [],
      perms_data: [],
      apps_data: [],
      users_selected: [],
      perms_selected: [],
      filterMethod(query, item) {
        return item.label.indexOf(query) > -1
      },
      list: [],
      listQuery: {
        page: 1,
        key: '',
        limit: 20,
        status: 1
      },
      listLoading: true,
      loading: true,
      group: false,
      users: false,
      perms: false,
      form: {
        app_selected: '',
        group_name: '',
        remark: ''
      },
      formLabelWidth: '120px',
      rules: {
        group_name: [
          { validator: group_unique_check, trigger: 'blur', required: true }
        ],
        app_selected: [
          { required: true, message: '请选择系统', trigger: 'change' }
        ]
      },
      action: '',
      my_id: undefined,
      mForm: {
        m_id: ''
      },
      menuVisable: false,
      currentG: '',
      menuList: [],
      menuLoading: false
    }
  },
  created() {
    this.fetchGroup()
  },
  computed: {
    searchList() {
      var list = this.list.filter((val) => {
        return JSON.stringify(val).toLowerCase().includes(this.listQuery.key.toLowerCase())
      })
      this.listQuery.page = 1
      this.total = list.length
      return list
    }
  },
  methods: {
    fetchGroup() {
      this.listLoading = true
      getGroups().then(response => {
        this.list = response.data[0]
        this.listLoading = false
      })
    },
    handleSizeChange(val) {
      this.listQuery.limit = val
    },
    handleCurrentChange(val) {
      this.listQuery.page = val
    },
    async handleDialog(id, val) {
      this.loading = true
      this.group_id = id
      if (val === '创建组') {
        this.action = 'add'
        getAppsSelector().then(response => {
          this.apps_data = response.data
        })
        this.group = true
      } else if (val === '成员分配') {
        this.action = 'users'
        this.users = true
        await getUsers(this.group_id).then(response => {
          this.users_data = response.data[0]
          this.users_selected = response.data[1]
        })
        this.loading = false
      } else if (val === '权限分配') {
        this.action = 'perms'
        this.perms = true
        await getPerms(this.group_id).then(response => {
          this.perms_data = response.data[0]
          this.perms_selected = response.data[1]
        })
        this.loading = false
      }
    },
    addSubmit(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          createGroup(this.form.group_name, this.form.app_selected, this.form.remark).then(response => {
            this.fetchGroup()
            this.group = false
            this.form = {}
          })
        } else {
          return false
        }
      })
    },
    onSubmit() {
      if (this.action === 'users') {
        updateGroup(this.group_id, this.action, this.users_selected).then(response => {
          this.users = false
          this.form = {}
        })
      } else {
        updateGroup(this.group_id, this.action, this.perms_selected).then(response => {
          this.perms = false
          this.form = {}
        })
      }
    },
    resetForm(done) {
      this.group = false
      this.users = false
      this.perms = false
      this.form = {}
      this.users_data = []
      this.perms_data = []
      this.mForm.m_id = ''
      this.currentG = ''
      this.menuVisable = false
      if (done !== undefined) {
        done()
      }
    },
    handleDelete(id) {
      this.$confirm('Please confirm operation', '提示', {
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(() => {
        deleteGroup(id).then(response => {
          this.fetchGroup()
          this.$message({
            type: 'success',
            message: 'Success'
          })
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: 'Canceled'
        })
      })
    },
    handleMenu(g_id, app_id, mSelect) {
      this.menuVisable = true
      this.menuLoading = true
      this.currentG = g_id
      this.mForm.m_id = mSelect
      getPermMenuWithApp(app_id).then(response => {
        this.menuList = response.data[0]
        this.menuLoading = false
      })
    },
    menuSubmit() {
      updateGroup(this.currentG, 'menu', this.mForm.m_id)
      this.fetchGroup()
      this.menuVisable = false
    },
    menuClose(done) {
      this.resetForm()
      done()
    }
  }
}
</script>
