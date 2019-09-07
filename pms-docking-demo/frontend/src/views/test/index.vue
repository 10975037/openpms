<template>
  <div class="app-container">
    api返回数据：{{ this.data }}<br><br>
    页面元素权限：{{this.element_perms}}<br><br>
    <el-button type="primary"
               v-if=btn>页面元素</el-button>
    <el-button type="primary"
               @click="press">测试</el-button>
  </div>
</template>

<script>
import { test } from '@/api/test'
export default {
  data() {
    return {
      data: this.data,
      btn: true,
      element_perms: this.element_perms
    }
  },

  methods: {
    press() {
      test().then(response => {
        this.btn = this.hasperm('btn')
        this.data = response
        console.log('code: ', this.data.code)
        this.element_perms = JSON.parse(localStorage.getItem('element_perms'))
        for (var j = 0, len = this.element_perms.length; j < len; j++) {
          console.log('element: ', this.element_perms[j]['element'], '-> action: ', this.element_perms[j]['action'])
        }
      }).catch(() => {
        console.log('warn: ', '没有权限')
      })
    }
  }

}
</script>

