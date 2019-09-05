<template>
  <el-container>
    <el-main>
      <div class="filter-container">
        <el-select v-model="filter.appId"
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

        <el-button class="el-icon-plus"
                   type="primary"
                   @click.prevent="handleAdd()">
        </el-button>
      </div>
      <br>
      <div class="app_container">
        <el-table :data="listFilter.slice((listQuery.page-1)*listQuery.limit,listQuery.page*listQuery.limit)"
                  v-loading="listLoading"
                  element-loading-text="Loading"
                  border
                  fit
                  mini-witdh
                  highlight-current-row>

          <el-table-column type="index"
                           width="50"
                           label="#">
          </el-table-column>

          <el-table-column align="left"
                           prop="app_name"
                           width="300"
                           label="App Name"
                           sortable>
            <template slot-scope="scope">
              <span>{{ scope.row.app_name.app_name }}</span>
            </template>
          </el-table-column>

          <el-table-column align="left"
                           prop="desc"
                           width="300"
                           label="Description"
                           sortable>
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
        <myDialog :dialogvisable.sync="dialogVisable"
                  :action.sync="action"
                  @listReloading="handleReload"
                  ref='mydialog' />
      </div>
    </el-main>
  </el-container>
</template>

<script>
import { getResourceMenu } from '@/api/pms'
import { deleteResourceMenu } from '@/api/pms'
import { getApp } from '@/api/pms'
import myDialog from './components/myDialog'

export default {
  components: { myDialog },
  data() {
    return {
      list: [],
      listLoading: false,
      appList: [],
      filter: {
        appId: '',
        menuName: ''
      },
      listQuery: {
        page: 1,
        limit: 20
      },
      dialogVisable: false,
      action: '',
      menuId: Number
    }
  },
  created() {
    this.fetchData()
    this.fetchApp()
  },
  computed: {
    listFilter() {
      const list = this.list.filter((val) => {
        if (this.filter.appId === '') {
          return this.list
        } else {
          return val.app_id === this.filter.appId
        }
      })
      return list
    }
  },
  methods: {
    fetchData() {
      this.listLoading = true
      getResourceMenu().then(response => {
        this.list = response.data[0]
        this.listLoading = false
      })
    },
    fetchApp() {
      getApp().then(response => {
        this.appList = response.data[0]
      })
    },
    handleEdit(id) {
      this.dialogVisable = true
      this.$refs.mydialog.initPage('edit', id) // 触发子组件方法
    },
    handleAdd() {
      this.dialogVisable = true
      this.action = 'add'
    },
    handleDelete(id) {
      this.$confirm('Please confirm operation', '提示', {
        confirmButtonText: 'OK',
        cancelButtonText: 'Cancel',
        type: 'warning'
      }).then(() => {
        deleteResourceMenu(id).then(response => {
          this.fetchData()
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
    handleReload() {
      this.fetchData()
    }
  }
}
</script>