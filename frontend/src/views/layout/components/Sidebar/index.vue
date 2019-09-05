<template>
  <el-scrollbar wrapClass="scrollbar-wrapper">
    <el-menu
      mode="vertical"
      :show-timeout="200"
      :default-active="$route.path"
      :collapse="isCollapse"
      background-color="#304156"
      text-color="#bfcbd9"
      active-text-color="#409EFF"
    >
      <sidebar-item v-for="route in routes" :key="route.name" :item="route" :base-path="route.path"></sidebar-item>
    </el-menu>
  </el-scrollbar>
</template>

<script>
import { mapGetters } from 'vuex'
import SidebarItem from './SidebarItem'

export default {
  components: { SidebarItem },
  watch: {
    '$route': 'test'
  },
  computed: {
    ...mapGetters([
      'sidebar'
    ]),
    routes() {
      // console.log('siderbar', global.antRouter)
      // console.log('global', this.$router.options.routes)
      // return this.$router.options.routes
      // console.log(global.antRouter)
      return global.antRouter
    },
    isCollapse() {
      return !this.sidebar.opened
    }
  },
  methods: {
    test() {
      return this.$router.options.routes
    }
  }
}
</script>
