export function tree2list(tree) {
  var queen = []
  var out = []
  queen = queen.concat(tree)
  while (queen.length) {
    var first = queen.shift()
    if (first.children) {
      first.children.forEach(item => {
        item.pid = first.id
      })
      queen = queen.concat(first.children)
      delete first['children']
    }
    out.push(first)
  }
  return out
}

// 将数据写成树结构
export function toTree(data) {
  // 删除 所有 children,以防止多次调用
  data.forEach(function(item) {
    delete item.children
    delete item.data // 删除data数据 Added by zongkai
  })

  // 将数据存储为 以 id 为 KEY 的 map 索引数据列
  var map = {}
  data.forEach(function(item) {
    map[item.id] = item
  })
  //        console.log(map);

  var val = []
  data.forEach(function(item) {
    // 以当前遍历项，的pid,去map对象中找到索引的id
    var parent = map[item.pid]

    // 如果找到索引，那么说明此项不在顶级当中,那么需要把此项添加到，他对应的父级中
    if (parent) {
      (parent.children || (parent.children = [])).push(item)
    } else {
      // 如果没有在map中找到对应的索引ID,那么直接把 当前的item添加到 val结果集中，作为顶级
      val.push(item)
    }
  })
  return val
}

export function getCheckedKeys(data) {
  data.forEach(item => {
    // 判断flag是否为true，并且有无子集，element-tree中父级设置选中的话，下面的子集也就全选中了，所有得排除掉
    if (item.flag === true && !item.children) {
      this.checkedKeys.push(item.id)
    }
    if (item.children && item.children.length) {
      // 如果存在子集，递归调用该方法
      this.getCheckedKeys(item.children)
    }
  })
}
