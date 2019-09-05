<template>
  <div>
    <el-button class="el-icon-plus"
               size="mini"
               type="primary"
               @click="nodeAdd">新建节点</el-button>
    <br>
    <el-tree :data="currentTreeData"
             node-key="id"
             default-expand-all
             :expand-on-click-node="false"
             :render-content="renderContent"
             v-loading="treeLoading">
    </el-tree>

    <el-dialog title="节点属性"
               :visible.sync="dialogVisable"
               append-to-body>
      <el-form :model="form"
               ref="form"
               :rules="rules">
        <el-form-item label="Menu Name"
                      label-width="150px"
                      prop="name">
          <el-input v-model="form.name"
                    style="width: 40%;"></el-input>
        </el-form-item>

        <el-form-item label="Title"
                      label-width="150px"
                      prop="title">
          <el-input v-model="form.title"
                    style="width: 40%;"></el-input>
        </el-form-item>

        <el-form-item label="Component"
                      label-width="150px"
                      prop="component">
          <el-input v-model="form.component"
                    style="width: 40%;"></el-input>
        </el-form-item>

        <el-form-item label="Icon"
                      label-width="150px"
                      prop="icon">
          <el-input v-model="form.icon"
                    style="width: 40%;"></el-input>
        </el-form-item>

        <el-form-item label="Hidden"
                      label-width="150px"
                      prop="hidden">
          <el-checkbox v-model="form.hidden"></el-checkbox>
        </el-form-item>

        <el-form-item label="Path"
                      label-width="150px"
                      prop="path">
          <el-input v-model="form.path"
                    style="width: 60%;"></el-input>
        </el-form-item>

        <el-form-item label="Redirect"
                      label-width="150px"
                      prop="redirect">
          <el-input v-model="form.redirect"
                    style="width: 60%;"></el-input>
        </el-form-item>

        <el-form-item label-width="150px">
          <el-button size="mini"
                     type="primary"
                     @click="nodeMetaSave('form')">保存</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>
<script>
export default {
  name: 'myTree',
  props: {
    treedata: {
      type: Array
    }
  },
  data() {
    return {
      form: {
        treeId: '',
        path: '',
        component: '',
        name: '',
        hidden: false,
        icon: '',
        redirect: '',
        title: ''
      },
      treeList: [], // 菜单树结构,
      treeLoading: false,
      dialogVisable: false,
      currentNode: Object,
      rules: {
        name: [
          { required: true, message: 'This is mandatory field', trigger: 'blur' }
        ],
        title: [
          { required: true, message: 'This is mandatory field', trigger: 'blur' }
        ],
        component: [
          { required: true, message: 'This is mandatory field', trigger: 'blur' }
        ],
        path: [
          { required: true, message: 'This is mandatory field', trigger: 'blur' }
        ]
      }
    }
  },
  computed: {
    currentTreeData: {
      get() {
        // console.log(this.treedata)
        return this.treedata
      },
      set(val) {
        this.$emit('update:treedata', val)
      }
    }
  },
  methods: {
    nodeAdd() { // 增加主节点
      this.treedata.push({ id: new Date().getTime(), label: '新建节点', isEdit: true })
      // console.log(this.treeList)
    },
    nodeAppend(data) { // 追加子节点
      const newChild = { id: new Date().getTime(), label: '', children: [], isEdit: true }
      // 判断是否有子节点
      if (!data.children) {
        this.$set(data, 'children', [])
      }
      data.children.push(newChild)
      this.expandedKey = [data] // 展开点击节点
    },
    nodeDelete(node, data) {
      // console.log(this.treeData)
      const parent = node.parent
      const children = parent.data.children || parent.data
      const index = children.findIndex(d => d.id === data.id)
      children.splice(index, 1)
      // console.log(data.id)
      // Vue.delete(this.treeData, data.id)
      // console.log(this.treeData)
    },
    nodeEdit(ev, store, data) { // 编辑节点名字
      // console.log(ev)
      data.isEdit = true
      this.$nextTick(() => { // 得到input
        const $input =
          ev.target.parentNode.parentNode.querySelector('input') ||
          ev.target.parentElement.parentElement.querySelector('input')
        !$input ? '' : $input.focus() // 获取焦点
      })
      // console.log(this.treeList)
    },
    nodeMetaEdit(node, data) {
      // this.currentNode = node
      this.dialogVisable = true
      // console.log(data.meta.name)
      if (!node.data.meta) {
        node.data.meta = {}
        node.data.meta.name = ''
        node.data.meta.path = ''
        node.data.meta.component = ''
        node.data.meta.hidden = ''
        node.data.meta.title = ''
        node.data.meta.icon = 'table'
        node.data.meta.redirect = ''
      }
      this.form.name = node.data.meta.name
      this.form.title = node.data.meta.title
      this.form.path = node.data.meta.path
      this.form.component = node.data.meta.component
      this.form.hidden = node.data.meta.hidden
      this.form.icon = node.data.meta.icon
      this.form.redirect = node.data.meta.redirect
      this.currentNode = node
    },
    nodeMetaSave(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          this.currentNode.data.meta.name = this.form.name
          this.currentNode.data.meta.title = this.form.title
          this.currentNode.data.meta.path = this.form.path
          this.currentNode.data.meta.component = this.form.component
          this.currentNode.data.meta.hidden = this.form.hidden
          this.currentNode.data.meta.icon = this.form.icon
          this.currentNode.data.meta.redirect = this.form.redirect
          this.dialogVisable = false
        } else {
          return false
        }
      })
      // this.currentNode.data.meta.name = this.form.name
      // this.currentNode.data.meta.path = this.form.path
      // this.currentNode.data.meta.component = this.form.component
      // this.currentNode.data.meta.hidden = this.form.hidden
      // this.currentNode.data.meta.icon = this.form.icon
      // this.currentNode.data.meta.redirect = this.form.redirect
      // this.dialogVisable = false
    },
    // 失焦事件
    edit_sure(ev, data) {
      const $input =
        ev.target.parentNode.parentNode.querySelector('input') ||
        ev.target.parentElement.parentElement.querySelector('input')
      if (!$input) {
        return false
      } else if ($input.value === '') {
        this.$message({
          type: 'info',
          message: '内容不能为空!'
        })
      } else { // 赋值value
        data.label = $input.value
        data.isEdit = false
      }
    },
    showOrEdit(data) { // 增加/修改节点时插入input控件
      if (data.isEdit) {
        return (
          <input type='text' class='node_labe' style='border-radius:6px;' value={data.label}
            on-blur={ev => this.edit_sure(ev, data)} />
        )
      } else {
        return <span class='node_labe'>{data.label}</span>
      }
    },
    renderContent(h, { node, data, store }) {
      return (
        <span class='custom-tree-node'>
          <span class='tree_node_label'>{this.showOrEdit(data)}</span>
          <div class='tree_node_op' style='text-align: right;'>
            <i class='el-icon-edit-outline' on-click={ev => this.nodeEdit(ev, store, data)} />
            <i class='el-icon-remove-outline'
              on-click={() => this.nodeDelete(node, data)} />
            <i class='el-icon-circle-plus-outline'
              on-click={() => this.nodeAppend(data)}></i>
            <i class='el-icon-document' on-click={() => this.nodeMetaEdit(node, data)} />
          </div>
        </span>
      )
    }
  }
}
</script>

<style>
.custom-tree-node {
  flex: 0.7;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 14px;
  padding-right: 8px;
}
</style>