<template>
  <el-container>
    <el-main>
      <div class="filter-container">
        <el-select v-model="listQuery.appId"
                   placeholder='App'
                   clearable
                   style="width: 150px"
                   class="filter-item">
          <el-option v-for="item in appList"
                     :key="item.id"
                     :label="item.app_name"
                     :value="item.id">
          </el-option>
        </el-select>

        <el-input :disabled="listQuery.appId === ''"
                  v-model="listQuery.name"
                  placeholder='Name'
                  style="width: 20%; margin-left:10px; margin-top:20px;"
                  class="filter-item">
        </el-input>

        <el-button class="el-icon-search"
                   :disabled="listQuery.appId === ''"
                   type="primary"
                   style="margin-left:10px;"
                   @click.prevent="handleSearch">
        </el-button>

        <el-button class="el-icon-plus"
                   type="primary"
                   @click.prevent="handleAdd">
        </el-button>
      </div>
      <br>
      <!-- {{appList}} -->
      <el-table :data="list"
                v-loading="listLoading"
                border
                fit
                mini-witdh
                highlight-current-row
                :stripe="true">

        <el-table-column type="index"
                         width="50"
                         label="序号">
        </el-table-column>

        <el-table-column align="left"
                         prop="resource_name"
                         width="120"
                         label="资源名"
                         sortable>
          <template slot-scope="scope">
            <span>{{ scope.row.resource_name }}</span>
          </template>
        </el-table-column>

        <el-table-column align="left"
                         prop="resource_type"
                         width="100"
                         label="类型"
                         sortable>
          <template slot-scope="scope">
            <span>{{ scope.row.resource_type }}</span>
          </template>
        </el-table-column>

        <el-table-column align="left"
                         prop="resource_code"
                         class-name="small-padding fixed-width"
                         label="资源代码">
          <template slot-scope="scope">
            <pre>{{ scope.row.resource_code }}</pre>
          </template>
        </el-table-column>

        <el-table-column align="left"
                         prop="description"
                         class-name="small-padding fixed-width"
                         label="资源描述">
          <template slot-scope="scope">
            <span>{{ scope.row.remark }}</span>
          </template>
        </el-table-column>

        <el-table-column label='操作'
                         align="center"
                         width="150">
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
      <pagination v-show="total>0"
                  :total="total"
                  :page.sync="listQuery.page"
                  :limit.sync="listQuery.limit"
                  @pagination="getPagination" />

      <el-dialog title="应用资源"
                 :visible.sync="dialogFormVisible"
                 :show-close="false"
                 :close-on-click-modal="false"
                 :close-on-press-escape="false">
        <el-form :model="form"
                 ref="form"
                 :rules="rules">

          <el-form-item label="应用"
                        :label-width="formLabelWidth"
                        prop="app_id">
            <el-select v-model="form.app_id"
                       placeholder='App'
                       clearable
                       style="width: 70%"
                       class="filter-item">
              <el-option v-for="(item, index) in appList"
                         :key="index"
                         :label="item.app_name"
                         :value="item.id" />
            </el-select>
          </el-form-item>

          <el-form-item label="资源名"
                        :label-width="formLabelWidth"
                        prop="resource_name">
            <el-input v-model="form.resource_name"
                      style="width: 70%;"></el-input>
          </el-form-item>

          <el-form-item label="类型"
                        :label-width="formLabelWidth"
                        prop="resource_type">
            <el-select v-model="form.resource_type"
                       placeholder='Resource Type'
                       clearable
                       style="width: 70%"
                       class="filter-item"
                       @change="phSyncup">
              <el-option v-for="(item, index) in typeOption"
                         :key="index"
                         :label="item.value"
                         :value="item.value" />
            </el-select>
          </el-form-item>

          <el-form-item label="资源代码"
                        :label-width="formLabelWidth"
                        prop="resource_code">
            <el-input :placeholder="formph"
                      type='textarea'
                      :rows="5"
                      v-model="form.resource_code"
                      style="width: 70%;"></el-input>
          </el-form-item>

          <el-form-item label="资源描述"
                        :label-width="formLabelWidth"
                        prop="desc">
            <el-input type='textarea'
                      :rows="5"
                      v-model="form.desc"
                      style="width: 70%;"></el-input>
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
import { getResource } from '@/api/pms'
import { postResource } from '@/api/pms'
import { putResource } from '@/api/pms'
import { deleteResource } from '@/api/pms'
import pagination from '@/components/Pagination'

export default {
  components: { pagination },
  data() {
    return {
      list: [],
      appList: [],
      formph: '',
      listQuery: {
        page: 1,
        limit: 20,
        id: undefined,
        appId: undefined,
        name: undefined,
        type: undefined,
        code: undefined
      },
      total: 0,
      listLoading: false,
      dialogFormVisible: false,
      formLabelWidth: '200px',
      editQuery: {
        id: ''
      },
      form: {
        app_id: '',
        resource_name: '',
        resource_type: '',
        resource_code: '',
        desc: ''
      },
      action: '',
      typeOption: [
        { value: 'url' },
        { value: 'element' },
        { value: 'data' }
      ],
      rules: {
        app_id: [
          { required: true, message: 'This is mandatory field', trigger: 'change' }
        ],
        resource_name: [
          { required: true, message: 'This is mandatory field', trigger: 'blur' }
        ],
        resource_type: [
          { required: true, message: 'This is mandatory field', trigger: 'change' }
        ],
        resource_code: [
          { required: true, message: 'This is mandatory field', trigger: 'blur' }
        ]
      }
    }
  },
  created() {
    this.fetchApp()
  },
  methods: {
    fetchResource() {
      this.listLoading = true
      getResource(this.listQuery).then(response => {
        this.list = response.data[0]
        this.total = response.total
        this.listLoading = false
      })
    },
    fetchApp() {
      getApp().then(response => {
        this.appList = response.data[0]
        this.listQuery.appId = this.appList[this.appList.length - 1].id
        this.fetchResource()
      })
    },
    getPagination(val) {
      this.listQuery.limit = val.limit
      this.listQuery.page = val.page
      this.fetchResource()
    },
    resetForm(formName) {
      this.$refs[formName].resetFields()
      this.dialogFormVisible = false
    },
    handleAdd() {
      this.action = 'add'
      this.dialogFormVisible = true
    },
    handleEdit(id) {
      this.editQuery.id = id
      getResource(this.editQuery).then(response => {
        this.form.app_id = response.data[0][0]['application']
        this.form.resource_name = response.data[0][0]['resource_name']
        this.form.resource_type = response.data[0][0]['resource_type']
        this.form.resource_code = JSON.stringify(response.data[0][0]['resource_code'])
        this.form.desc = response.data[0][0]['remark']
      })
      this.action = 'edit'
      this.dialogFormVisible = true
    },
    handleDelete(id) {
      this.$confirm('Please confirm operation', '提示', {
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(() => {
        deleteResource(id).then(response => {
          this.fetchResource()
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
    handleSearch() {
      this.listQuery.page = 1
      this.fetchResource()
    },
    phSyncup() {
      if (this.form.resource_type === 'url') {
        this.formph = '{"url":"<url address>"}\n{"url":"/v1/pms/apps_selector/"}'
      } else if (this.form.resource_type === 'element') {
        this.formph = '{"element":<element id>}\n{"element":1}'
      } else if (this.form.resource_type === 'data') {
        this.formph = '{"data":{"table_name":"<table name>","<column_name>":"<value>"}}\n{"data":{"table_name":"user_info","user_name":"Steven"}}'
      } else {
        this.formph = ''
      }
    },
    onSubmit(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          // alert('submit!')
          if (this.action === 'add') {
            postResource(this.form.app_id, this.form.resource_name, this.form.resource_type, this.form.resource_code, this.form.desc).then(response => {
              this.listQuery.appId = this.form.app_id // 添加资源后，直接展现当前app下的资源
              this.fetchResource()
              this.dialogFormVisible = false
            })
          } else {
            putResource(this.editQuery.id, this.form.app_id, this.form.resource_name, this.form.resource_type, this.form.resource_code, this.form.desc).then(response => {
              this.fetchResource()
              this.dialogFormVisible = false
            })
          }
        } else {
          return false
        }
      })
    }
  }
}
</script>
