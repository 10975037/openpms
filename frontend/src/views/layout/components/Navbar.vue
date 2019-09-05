<template>
  <el-menu class="navbar"
           mode="horizontal">
    <hamburger class="hamburger-container"
               :toggleClick="toggleSideBar"
               :isActive="sidebar.opened"></hamburger>
    <breadcrumb></breadcrumb>
    <el-dropdown class="avatar-container"
                 trigger="click">
      <div class="avatar-wrapper">
        <!-- <img class="user-avatar" :src="avatar+'?imageView2/1/w/80/h/80'"> -->
        <img class="user-avatar"
             src="../../../assets/face.gif">
        <i class="el-icon-caret-bottom"></i>
      </div>
      <el-dropdown-menu class="user-dropdown"
                        slot="dropdown">
        <router-link class="inlineBlock"
                     to="/">
          <el-dropdown-item>
            Home
          </el-dropdown-item>
        </router-link>
        <el-dropdown-item divided>
          <span @click="logout"
                style="display:block;">LogOut</span>
        </el-dropdown-item>
      </el-dropdown-menu>
    </el-dropdown>
  </el-menu>
</template>

<script>
import { mapGetters } from 'vuex'
import Breadcrumb from '@/components/Breadcrumb'
import Hamburger from '@/components/Hamburger'

export default {
  components: {
    Breadcrumb,
    Hamburger
  },
  computed: {
    ...mapGetters([
      'sidebar',
      'avatar'
    ])
  },
  methods: {
    toggleSideBar() {
      this.$store.dispatch('ToggleSideBar')
    },
    logout() {
      // this.$store.dispatch('CloseSideBar', { withoutAnimation: false }) // logout 收起菜单栏 不加载菜单的临时解决方案
      this.$store.dispatch('LogOut').then(() => {
        const redirect = (url, asLink = true) => asLink ? (window.location.href = url) : window.location.replace(url)
        // redirect('http://sso.sunmi.com?callbackUrl=http://104.250.34.119:9550&clientId=sm5c21de0f0c6fd&type=loginout')
        redirect(process.env.SSO_URL + '&type=loginout')
        // location.reload() // 为了重新实例化vue-router对象 避免bug
      })
    }
  }
}
</script>

<style rel="stylesheet/scss" lang="scss" scoped>
.navbar {
  height: 50px;
  line-height: 50px;
  border-radius: 0px !important;
  .hamburger-container {
    line-height: 58px;
    height: 50px;
    float: left;
    padding: 0 10px;
  }
  .screenfull {
    position: absolute;
    right: 90px;
    top: 16px;
    color: red;
  }
  .avatar-container {
    height: 50px;
    display: inline-block;
    position: absolute;
    right: 35px;
    .avatar-wrapper {
      cursor: pointer;
      margin-top: 5px;
      position: relative;
      .user-avatar {
        width: 40px;
        height: 40px;
        border-radius: 10px;
      }
      .el-icon-caret-bottom {
        position: absolute;
        right: -20px;
        top: 25px;
        font-size: 12px;
      }
    }
  }
}
</style>

