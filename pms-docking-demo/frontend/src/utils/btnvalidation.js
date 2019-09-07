import Vue from 'vue'

// 权限指令
const has = Vue.directive('has', {
  bind: function(el, binding, vnode) {
    // 获取页面按钮权限
    const element_name = binding.value
    if (!Vue.prototype.$_has(element_name)) {
      el.parentNode.removeChild(el)
    }
  }
})
// 权限检查方法
Vue.prototype.$_has = function(value) {
  let isExist = true
  const resources = JSON.parse(localStorage.getItem('element_perms'))

  for (const item of resources) {
    if (item.element === value && item.action === 0) {
      isExist = false
    }
  }
  return isExist
}

// 元素权限判断返回true or false
function hasperm(value) {
  let isExist = true
  const resources = JSON.parse(localStorage.getItem('element_perms'))

  for (const item of resources) {
    if (item.element === value && item.action === 0) {
      isExist = false
    }
  }
  return isExist
}

export default
{
  has,
  install: function(Vue) {
    Vue.prototype.hasperm = (value) => hasperm(value)
  }
}
