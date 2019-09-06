<template>
  <div>
    <el-dialog title="菜单配置"
               :visible.sync="currentVisable"
               width="70%"
               :before-close="resetForm">
      <!-- 进度条 -->
      <el-steps :active="active"
                finish-status="success">
        <el-step title="基础信息"></el-step>
        <el-step title="菜单明细"></el-step>
        <el-step title="完成"></el-step>
      </el-steps>

      <br>
      <!-- first step -->
      <div>
        <el-form v-show="this.active === 0"
                 :model="form"
                 v-loading="listLoading"
                 ref="form"
                 :rules="rules">
          <el-form-item label="应用系统"
                        :label-width="formLabelWidth"
                        prop="appId">
            <el-select v-model="form.appId"
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
      </div>

      <!-- second step -->
      <myTree v-show="this.active === 1"
              :treedata.sync="menuData" />

      <el-button v-if="active > 0"
                 style="margin-top: 12px;"
                 @click="pre">上一步</el-button>
      <el-button v-if="active === 1"
                 style="margin-top: 12px;"
                 @click="onSubmit('form')">完成</el-button>
      <el-button v-else
                 style="margin-top: 12px;"
                 @click="next('form')">下一步</el-button>
    </el-dialog>
  </div>
</template>
<script>
import { getApp } from '@/api/pms'
import { getResourceMenu } from '@/api/pms'
import { postResourceMenu } from '@/api/pms'
import { putResourceMenu } from '@/api/pms'
import myTree from './myTree'
import { toTree } from '@/utils/treeformat'
import { tree2list } from '@/utils/treeformat'
import { menuUniqueCheck } from '@/api/pms'

export default {
  name: 'addDialog',
  components: { myTree },
  props: {
    dialogvisable: {
      type: Boolean,
      default: true
    },
    action: {
      type: String
    }
  },
  created() {
    this.fetchApp()
  },
  data() {
    var menu_unique_check = (rule, value, callback) => {
      if (!value) {
        return callback(new Error('不能为空'))
      }
      if (this.action === 'add') {
        menuUniqueCheck(this.form.appId).then(response => {
          if (response.data !== 0) {
            return callback(new Error('此应用已经存在菜单'))
          } else {
            callback()
          }
        })
      } else {
        callback()
      }
    }
    return {
      form: {
        name: '',
        desc: '',
        appId: ''
      },
      formLabelWidth: '120px',
      active: 0,
      appList: [],
      menuData: [],
      listLoading: false,
      currentMenuId: Number,
      rules: {
        appId: [
          { required: true, validator: menu_unique_check, trigger: 'change' }
        ],
        name: [
          { required: true, message: 'This is mandatory field', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    currentVisable: {
      get() {
        return this.dialogvisable
      },
      set(val) {
        this.$emit('update:dialogvisable', val)
      }
    }
  },
  methods: {
    next(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          if (this.active++ > 2) this.active = 0
        } else {
          return false
        }
      })
    },
    pre() {
      if (this.active-- < 0) this.active = 0
    },
    fetchApp() {
      getApp().then(response => {
        this.appList = response.data[0]
      })
    },
    initPage(action, menuId) {
      this.currentMenuId = menuId
      this.listLoading = true
      this.$emit('update:action', action)
      if (action === 'edit') {
        getResourceMenu(menuId).then(response => {
          this.form.name = response.data[0][0]['r_menu_name']
          this.form.desc = response.data[0][0]['description']
          this.form.appId = response.data[0][0]['app_id']
          this.menuData = toTree(response.data[0][0]['r_menu_data'])
          this.listLoading = false
        })
      }
    },
    onSubmit(formName) {
      const newMenu = tree2list(this.menuData)
      if (this.action === 'add') {
        postResourceMenu(this.form.appId, this.form.desc, newMenu)
      } else if (this.action === 'edit') {
        putResourceMenu(this.currentMenuId, this.form.desc, newMenu)
      }
      this.$emit('update:dialogvisable', false)
      this.$emit('listReloading')
      this.menuData = []
      this.active = 0
      this.$refs[formName].resetFields()
    },
    resetForm(done) {
      this.menuData = []
      this.active = 0
      this.form.name = ''
      this.form.desc = ''
      this.form.appId = ''
      done()
    }
  }
}
</script>