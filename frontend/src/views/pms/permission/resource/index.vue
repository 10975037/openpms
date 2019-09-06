<template>
  <div class="app-container"
       style="margin-top:1%;margin-left:1%;margin-right:1%;">
    <div class="filter-container">
      <el-select v-model="listQuery.app_id"
                 filterable
                 clearable
                 placeholder="Select App Name"
                 @change="fetchResourceWithAppData(listQuery.app_id);listQuery.resource_id = ''">
        <el-option v-for="item in app_list"
                   :key="item.id"
                   :label="item.app_name"
                   :value="item.id">
        </el-option>
      </el-select>

      <el-select v-model="listQuery.resource_id"
                 filterable
                 clearable
                 placeholder="Select Resource Name"
                 :disabled="listQuery.app_id === ''">
        <el-option v-for="item in resource_list"
                   :key="item.id"
                   :label="item.resource_name"
                   :value="item.id">
        </el-option>
      </el-select>

      <el-button class="el-icon-search"
                 type="primary"
                 style="margin-left:10px;"
                 @click.prevent="fetchPermissionData">
      </el-button>

      <el-button class="el-icon-plus"
                 type="primary"
                 @click.prevent="handleCreate">
      </el-button>
    </div>
    <br>

    <!-- ---------权限列表----- -->
    <el-table :data="pms_list"
              v-loading="listLoading"
              border
              fit
              highlight-current-row
              :stripe="true">
      <el-table-column type="index"
                       width="50"
                       label="#">
      </el-table-column>

      <el-table-column label="权限名称"
                       class-name="small-padding fixed-width"
                       align="left">
        <template slot-scope="scope">
          <span>{{ scope.row.permission_name }}</span>
        </template>
      </el-table-column>

      <el-table-column label="应用系统"
                       class-name="small-padding fixed-width"
                       align="left">
        <template slot-scope="scope">
          <span>{{ scope.row.app_name }}</span>
        </template>
      </el-table-column>
      <el-table-column label="资源名"
                       class-name="small-padding fixed-width"
                       align="left">
        <template slot-scope="scope">
          <span>{{ scope.row.resource_name }}</span>
        </template>
      </el-table-column>

      <el-table-column label="操作权限"
                       align="left"
                       class-name="small-padding fixed-width">
        <template slot-scope="scope">
          <span>{{ scope.row.action_list }}</span>
        </template>
      </el-table-column>

      <el-table-column label="说明"
                       align="left"
                       class-name="small-padding fixed-width">
        <template slot-scope="scope">
          {{ scope.row.remark }}
        </template>
      </el-table-column>

      <el-table-column label="操作"
                       width="120"
                       align="left">
        <template slot-scope="scope">
          <el-button type="primary"
                     size="mini"
                     circle
                     icon="el-icon-edit"
                     @click="handleUpdate(scope.row)"></el-button>
          <el-button type="danger"
                     size="mini"
                     circle
                     icon="el-icon-delete"
                     @click="handleDelete(scope.row.id)"></el-button>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination v-show="total>0"
                   :current-page="listQuery.page"
                   :page-sizes="[10,20,30, 50]"
                   :page-size="listQuery.limit"
                   :total="total"
                   background
                   layout="total, sizes, prev, pager, next, jumper"
                   @size-change="handleSizeChange"
                   @current-change="handleCurrentChange" />

    <!-- ---------添加权限------ -->
    <div>
      <el-dialog :title="textMap[dialogStatus]"
                 width="50%"
                 :visible.sync="dialogFormVisible">
        <el-form ref="dataForm"
                 :rules="rules"
                 :model="pmsform"
                 label-position="right"
                 label-width="150px">
          <el-form-item label="应用系统"
                        prop="app_id">
            <el-select v-model="pmsform.app_id"
                       style="width: 60%;"
                       filterable
                       clearable
                       placeholder="Select App Name"
                       @change="fetchResourceWithAppData(pmsform.app_id);pmsform.resource_id = ''"
                       :disabled="dialogStatus==='update'">
              <el-option v-for="item in app_list"
                         :key="item.id"
                         :label="item.app_name"
                         :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="资源名"
                        prop="resource_id">
            <el-select v-model="pmsform.resource_id"
                       filterable
                       style="width: 60%;"
                       clearable
                       placeholder="Select Resource Name"
                       @change="fetchResourceData()"
                       :disabled="dialogStatus==='update'">
              <el-option v-for="item in resource_list"
                         :key="item.id"
                         :label="item.resource_name"
                         :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="资源类型">
            <el-input v-model="query.resource_type"
                      style="width: 60%;"
                      disabled>
            </el-input>
          </el-form-item>

          <el-form-item label="Permission Action"
                        prop="action">
            <el-checkbox v-model="pmsform.action"
                         v-for="action in actions"
                         :label="action.key"
                         :key="action.key">{{action.value}}</el-checkbox>
          </el-form-item>
        </el-form>

        <span slot="footer"
              class="dialog-footer">
          <el-button @click="resetForm('dataForm')">Cancel</el-button>
          <el-button type="primary"
                     @click="dialogStatus==='create'?createData():updateData()">OK</el-button>
        </span>
      </el-dialog>
    </div>
  </div>

</template>

<script>
const actionOptions1 = [{ 'key': 8, 'value': 'DELETE' }, { 'key': 4, 'value': 'PUT' }, { 'key': 2, 'value': 'POST' }, { 'key': 1, 'value': 'GET' }]
const actionOptions2 = [{ 'key': 0, 'value': 'DISABLE' }]
import {
  getApp
} from '@/api/pms'
import {
  getResourceWithApp
} from '@/api/pms'
import {
  getResource
} from '@/api/pms'
import {
  addPermission
} from '@/api/pms'
import {
  delPermission
} from '@/api/pms'
import {
  editPermission
} from '@/api/pms'
import {
  getPermission
} from '@/api/pms'
export default {
  data() {
    return {
      formLabelWidth: '200px',
      pms_list: [],
      app_list: [],
      resource_list: [],
      listQuery: {
        page: 1,
        limit: 10,
        app_id: '',
        resource_id: ''
      },
      actions: actionOptions1,
      pmsform: {
        id: '',
        app_id: '',
        action: [],
        permission_name: '',
        resource_id: '',
        resource_name: ''
      },
      query: {
        id: '',
        resource_type: ''
      },
      total: 0,
      delvmapVisible: false,
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: '编辑',
        create: '创建'
      },
      listLoading: true,
      rules: {
        app_id: [{
          required: true,
          message: 'App Name',
          trigger: 'blur'
        }],
        resource_id: [{
          required: true,
          message: 'Resource Name',
          trigger: 'blur'
        }],
        action: [{
          required: true,
          message: '请选择权限动作',
          trigger: 'blur'
        }]
      }
    }
  },
  created() {
    this.fetchPermissionData()
    this.fetchAppData()
  },
  methods: {
    fetchAppData() {
      this.listLoading = true
      getApp().then(response => {
        // console.log(response.data[0])
        this.app_list = response.data[0]
      })
      this.listLoading = false
    },
    fetchResourceWithAppData(app_id) {
      this.listLoading = true
      getResourceWithApp(app_id).then(response => {
        // console.log(response.data[0])
        this.resource_list = response.data[0]
      })
      this.listLoading = false
    },
    fetchResourceData() {
      this.listLoading = true
      this.query.id = this.pmsform.resource_id
      getResource(this.query).then(response => {
        // console.log(response.data[0][0])
        this.query.resource_type = response.data[0][0].resource_type
        if (this.query.resource_type === 'element') {
          this.actions = actionOptions2
        } else {
          this.actions = actionOptions1
        }
        this.listLoading = false
      })
    },
    fetchPermissionData() {
      this.listLoading = true
      getPermission(this.listQuery).then(response => {
        // console.log(response.data[0])
        this.pms_list = response.data[0]
        this.total = response.total
      })
      this.listLoading = false
    },
    handleSizeChange(val) {
      this.listQuery.limit = val
      this.fetchPermissionData()
    },
    handleCurrentChange(val) {
      this.listQuery.page = val
      this.fetchPermissionData()
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
      this.dialogFormVisible = false
    },
    handleDelete(id) {
      this.$confirm('Please confirm operation', '提示', {
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(() => {
        delPermission(id).then(response => {
          this.fetchPermissionData()
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
    resetTemp() {
      this.pmsform = {
        id: '',
        app_id: '',
        action: [],
        resource_id: ''
      }
    },
    handleCreate() {
      this.resetTemp()
      this.fetchAppData()
      this.dialogStatus = 'create'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    createData() {
      // console.log(this.pmsform.action)
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          addPermission(this.pmsform).then(response => {
            this.fetchPermissionData()
            this.dialogFormVisible = false
          })
        }
      })
    },
    handleUpdate(row) {
      this.pmsform = Object.assign({}, row) // copy obj
      this.fetchResourceWithAppData(this.pmsform.app_id)
      this.fetchResourceData()
      this.dialogStatus = 'update'
      this.dialogFormVisible = true
      this.$nextTick(() => {
        this.$refs['dataForm'].clearValidate()
      })
    },
    updateData() {
      this.listLoading = true
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          const tempData = Object.assign({}, this.pmsform)
          editPermission(tempData).then(() => {
            this.dialogFormVisible = false
            this.fetchPermissionData()
          }).catch(() => { })
        }
      })
      this.listLoading = false
    }
  }
}
</script>
