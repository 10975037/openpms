<template>
  <div class="app-container">
    <div class="filter-container">
      <el-select v-model="listQuery.app_id"
                 filterable
                 clearable
                 placeholder="Select App Name"
                 @change="fetchRMenuWithAppData(listQuery.app_id)">
        <el-option v-for="item in app_list"
                   :key="item.id"
                   :label="item.app_name"
                   :value="item.id">
        </el-option>
      </el-select>

      <el-button class="el-icon-search"
                 type="primary"
                 style="margin-left:10px;"
                 @click.prevent="fetchPermmenuData">
      </el-button>

      <el-button class="el-icon-plus"
                 type="primary"
                 @click.prevent="handleCreate">
      </el-button>
    </div>
    <br>

    <!-- ---------权限菜单列表----- -->
    <el-table :data="p_menu_list"
              v-loading="listLoading"
              border
              fit
              highlight-current-row
              :stripe="true">
      <el-table-column type="index"
                       width="50"
                       label="#">
      </el-table-column>

      <el-table-column label="Permmenu Name"
                       align="left">
        <template slot-scope="scope">
          <span>{{ scope.row.p_menu_name }}</span>
        </template>
      </el-table-column>

      <el-table-column label="App Name"
                       align="left">
        <template slot-scope="scope">
          <span>{{ scope.row.app_name.app_name }}</span>
        </template>
      </el-table-column>

      <el-table-column label="Description "
                       align="left">
        <template slot-scope="scope">
          {{ scope.row.description }}
        </template>
      </el-table-column>

      <el-table-column label="P_Menu Data"
                       align="left"><template slot-scope="scope">
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
        </template></el-table-column>
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
                       style="width: 60%"
                       filterable
                       clearable
                       placeholder="Select App Name"
                       @change="fetchRMenuWithAppData(pmsform.app_id);pmsform.res_menu_id = ''"
                       :disabled="dialogStatus==='update'">
              <el-option v-for="item in app_list"
                         :key="item.id"
                         :label="item.app_name"
                         :value="item.id">
              </el-option>
            </el-select>
          </el-form-item>

          <el-form-item label="菜单名"
                        prop="p_menu_name">
            <el-input v-model="pmsform.p_menu_name"
                      :disabled="dialogStatus==='update'"
                      style="width: 60%">
            </el-input>
          </el-form-item>

          <el-form-item label="描述"
                        prop="description">
            <el-input type="textarea"
                      v-model="pmsform.description"
                      style="width: 60%;"
                      rows="2"></el-input>
          </el-form-item>

          <el-form-item label="菜单权限"
                        prop="p_menu_data">
            <el-tree :data="data_tree"
                     show-checkbox
                     ref="tree"
                     node-key="id"
                     :default-checked-keys="pmsform.checked_keys"
                     default-expand-all>
            </el-tree>
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
  </el-container>
</template>

<script>
import {
  getApp
} from '@/api/pms'
import {
  getMenuWithApp
} from '@/api/pms'
import {
  getPermmenu
} from '@/api/pms'
import {
  postPermmenu
} from '@/api/pms'
import {
  putPermmenu
} from '@/api/pms'
import {
  deletePermmenu
} from '@/api/pms'
export default {
  data() {
    return {
      formLabelWidth: '200px',
      checkedKeys: [],
      data_tree: [],
      data_arr: [],
      p_menu_list: [],
      app_list: [],
      r_menu_list: [],
      listQuery: {
        page: 1,
        limit: 10,
        app_id: ''
      },
      pmsform: {
        app_id: '',
        p_menu_name: '',
        p_menu_data: [],
        checked_keys: [],
        description: ''
      },
      total: 0,
      dialogFormVisible: false,
      dialogStatus: '',
      textMap: {
        update: '编辑',
        create: '创建'
      },
      listLoading: true,
      rules: {
        p_menu_name: [{
          required: true,
          message: 'P_Menu Name',
          trigger: 'blur'
        }],
        app_id: [{
          required: true,
          message: 'App Name',
          trigger: 'blur'
        }],
        description: [{
          required: true,
          message: 'description',
          trigger: 'blur'
        }]
      }
    }
  },
  created() {
    this.fetchPermmenuData()
    this.fetchAppData()
  },
  methods: {
    fetchAppData() {
      // this.listLoading = true
      getApp().then(response => {
        // console.log(response.data[0])
        this.app_list = response.data[0]
        // this.listLoading = false
      })
    },
    fetchRMenuWithAppData(app_id) {
      this.listLoading = true
      getMenuWithApp(app_id).then(response => {
        console.log(response.data[0])
        this.r_menu_list = response.data[0]
        this.data_arr = response.data[0][0].r_menu_data
        this.data_tree = this.listToTree(this.data_arr)
      })
      this.listLoading = false
    },
    fetchPermmenuData() {
      this.listLoading = true
      getPermmenu(this.listQuery).then(response => {
        // console.log(response.data[0])
        this.p_menu_list = response.data[0]
        this.total = response.total
        this.listLoading = false
      })
    },
    handleSizeChange(val) {
      this.listQuery.limit = val
      this.fetchPermmenuData()
    },
    handleCurrentChange(val) {
      this.listQuery.page = val
      this.fetchPermmenuData()
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
        deletePermmenu(id).then(response => {
          this.fetchPermmenuData()
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
        app_id: '',
        p_menu_name: '',
        p_menu_data: [],
        checked_keys: [],
        description: ''
      }
      this.data_tree = []
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
      // console.log(this.data_arr)
      this.pmsform.checked_keys = this.$refs.tree.getCheckedKeys()
      this.$refs['dataForm'].validate((valid) => {
        if (valid) {
          postPermmenu(this.pmsform).then(response => {
            this.fetchPermmenuData()
            this.dialogFormVisible = false
          })
        }
      })
    },
    handleUpdate(row) {
      this.pmsform = Object.assign({}, row) // copy obj
      // console.log(this.pmsform)
      this.fetchRMenuWithAppData(this.pmsform.app_id)
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
          tempData.checked_keys = this.$refs.tree.getCheckedKeys()
          console.log(tempData)
          putPermmenu(tempData).then(() => {
            this.dialogFormVisible = false
            this.fetchPermmenuData()
          }).catch(() => { })
        }
      })
      this.listLoading = false
    },
    // 将数据写成树结构
    listToTree(data) {
      // 删除 所有 children,以防止多次调用
      data.forEach(function(item) {
        delete item.children
      })
      // 将数据存储为 以 id 为 KEY 的 map 索引数据列
      var map = {}
      data.forEach(function(item) {
        map[item.id] = item
      })
      //        console.log(map);
      var val = []
      data.forEach(function(item) {
        // 以当前遍历项，的pid,去map对象中找到索引的id
        var parent = map[item.pid]
        // 如果找到索引，那么说明此项不在顶级当中,那么需要把此项添加到，他对应的父级中
        if (parent) {
          (parent.children || (parent.children = [])).push(item)
        } else {
          // 如果没有在map中找到对应的索引ID,那么直接把 当前的item添加到 val结果集中，作为顶级
          val.push(item)
        }
      })
      return val
    }
  }
}
</script>
