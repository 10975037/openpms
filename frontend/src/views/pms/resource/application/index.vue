<template>
  <el-container>
    <el-main>
      <div class="filter-container">
        <el-input placeholder='Name'
                  v-model="filter"
                  style="width: 20%; margin-left:20px; margin-top:20px;"
                  class="filter-item">
        </el-input>

        <el-button class="el-icon-plus"
                   type="primary"
                   @click.prevent="handleAdd">
        </el-button>

      </div>
      <div class="app-container">
        <el-table :data="listFilter.slice((listQuery.page-1)*listQuery.limit,listQuery.page*listQuery.limit)"
                  v-loading="listLoading"
                  element-loading-text="Loading"
                  border
                  fit
                  mini-witdh
                  highlight-current-row>

          <el-table-column align="left"
                           prop="app_id"
                           width="100"
                           label="App ID"
                           sortable>
            <template slot-scope="scope">
              <span>{{ scope.row.id }}</span>
            </template>
          </el-table-column>

          <el-table-column align="left"
                           prop="app_name"
                           width="300"
                           label="App Name"
                           sortable>
            <template slot-scope="scope">
              <span>{{ scope.row.app_name }}</span>
            </template>
          </el-table-column>

          <el-table-column align="left"
                           width="500"
                           label="Description">
            <template slot-scope="scope">
              <span>{{ scope.row.description }}</span>
            </template>
          </el-table-column>

          <el-table-column label='Action'
                           align="center"
                           class-name="small-padding fixed-width">
            <template slot-scope="scope">
              <el-button type="primary"
                         size="mini"
                         icon="el-icon-edit"
                         circle
                         @click="handleEdit(scope.row.id)"></el-button>
              <el-button type="danger"
                         size="mini"
                         icon="el-icon-delete"
                         circle
                         @click="handleDelete(scope.row.id)"></el-button>
            </template>
          </el-table-column>

        </el-table>
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

      </div>
      <el-dialog title="Create App"
                 :visible.sync="dialogFormVisible"
                 :show-close="false"
                 :close-on-click-modal="false"
                 :close-on-press-escape="false">
        <el-form :model="form"
                 ref="form"
                 :rules="rules">
          <el-form-item label="App Name"
                        :label-width="formLabelWidth"
                        prop="app_name">
            <el-input :disabled="action === 'edit'"
                      v-model="form.app_name"
                      style="width: 40%;"></el-input>
          </el-form-item>

          <el-form-item label="Description"
                        :label-width="formLabelWidth"
                        prop="desc">
            <el-input type='textarea'
                      :rows="5"
                      v-model="form.desc"
                      style="width: 50%;"></el-input>
          </el-form-item>

        </el-form>
        <div slot="footer"
             class="dialog-footer">
          <el-button @click="resetForm('form')">Cancel</el-button>
          <el-button type="primary"
                     @click="onSubmit('form')">OK</el-button>
        </div>
      </el-dialog>
    </el-main>
  </el-container>
</template>

<script>
import { getApp } from '@/api/pms'
import { postApp } from '@/api/pms'
import { putApp } from '@/api/pms'
import { deleteApp } from '@/api/pms'
import { appUniqueCheck } from '@/api/pms'

export default {
  data() {
    var app_unique_check = (rule, value, callback) => {
      if (value === '') {
        return callback(new Error('不能为空'))
      }
      if (this.action === 'add') {
        appUniqueCheck(value).then(response => {
          if (response.data === 1) {
            return callback(new Error('已存在'))
          } else {
            callback()
          }
        })
      } else {
        callback()
      }
    }
    return {
      list: [],
      listLoading: false,
      filter: '',
      listQuery: {
        page: 1,
        limit: 20
      },
      total: '',
      dialogFormVisible: false,
      formLabelWidth: '100px',
      form: {
        app_name: '',
        desc: ''
      },
      appID: Number,
      action: '',
      rules: {
        app_name: [
          { validator: app_unique_check, trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.fetchApp()
  },
  computed: {
    listFilter() {
      var list = this.list.filter((val) => {
        return val.app_name.toLowerCase().includes(this.filter.toLowerCase())
      })
      this.listQuery.page = 1
      this.total = list.length
      return list
    }
  },
  methods: {
    fetchApp() {
      this.listLoading = true
      getApp().then(response => {
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
    handleAdd() {
      this.action = 'add'
      this.dialogFormVisible = true
    },
    handleEdit(id) {
      getApp(id).then(response => {
        this.form.app_name = response.data[0][0]['app_name']
        this.form.desc = response.data[0][0]['description']
      })
      this.action = 'edit'
      this.appID = id
      this.dialogFormVisible = true
    },
    handleDelete(id) {
      this.$confirm('Please confirm operation', '提示', {
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(() => {
        deleteApp(id).then(response => {
          this.fetchApp()
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
    resetForm(formName) {
      this.$refs[formName].resetFields()
      this.dialogFormVisible = false
    },
    onSubmit(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if (this.action === 'add') {
            postApp(this.form.app_name, this.form.desc).then(response => {
              this.fetchApp()
            })
          } else {
            putApp(this.appID, this.form.app_name, this.form.desc).then(response => {
              this.fetchApp()
            })
          }
          this.resetForm(formName)
        } else {
          return false
        }
      })
    }
  }
}
</script>