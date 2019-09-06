export function rFormat(routers) {
  // 简单检查是否是可以处理的数据
  if (!(routers instanceof Array)) {
    return false
  }
  // 处理后的容器
  const fmRouters = []
  routers.forEach(router => {
    const path = router.path
    const component = router.component
    const name = router.name
    const hidden = router.hidden
    let children = router.children
    const meta = router.meta

    // 如果有子组件，递归处理
    if (children && children instanceof Array) {
      children = rFormat(children)
    }
    const fmRouter = {
      path: path,
      component(resolve) {
        // 拼出相对路径，由于component无法识别变量
        // 利用Webpack 的 Code-Splitting 功能
        if (router.component === 'Layout') {
          require(['@/views/layout/Layout.vue'], resolve)
        } else {
          require(['@/views' + component], resolve)
        }
      },
      name: name,
      hidden: hidden,
      children: children,
      meta: meta
    }
    fmRouters.push(fmRouter)
  })
  return fmRouters
}
