import request from '@/utils/request'

// Application
export function getApp(id = '') {
  return request({
    url: '/pms/application/',
    methods: 'get',
    params: { id }
  })
}

export function postApp(app_name, desc) {
  return request({
    url: '/pms/application/',
    method: 'post',
    data: {
      app_name,
      desc
    }
  })
}

export function putApp(app_id, app_name, desc) {
  return request({
    url: '/pms/application/',
    method: 'put',
    data: {
      app_id,
      app_name,
      desc
    }
  })
}

export function deleteApp(id) {
  return request({
    url: '/pms/application/',
    method: 'delete',
    params: { id }
  })
}

export function getAppsSelector() {
  return request({
    url: '/pms/apps_selector/',
    methods: 'get'
  })
}

export function appUniqueCheck(app_name) {
  return request({
    url: '/pms/app_unqiue_check/',
    methods: 'get',
    params: { app_name }
  })
}

// Resource
export function getResource(query) {
  return request({
    url: '/pms/resource/',
    method: 'get',
    params: { query }
  })
}

export function getResourceWithApp(app_id) {
  return request({
    url: '/pms/resource&app/',
    method: 'get',
    params: { app_id }
  })
}

export function postResource(app_id, resource_name, resource_type, resource_code, desc) {
  return request({
    url: '/pms/resource/',
    method: 'post',
    data: {
      app_id,
      resource_name,
      resource_type,
      resource_code,
      desc
    }
  })
}

export function putResource(resource_id, app_id, resource_name, resource_type, resource_code, desc) {
  return request({
    url: '/pms/resource/',
    method: 'put',
    data: {
      resource_id,
      app_id,
      resource_name,
      resource_type,
      resource_code,
      desc
    }
  })
}

export function deleteResource(id) {
  return request({
    url: '/pms/resource/',
    method: 'delete',
    params: { id }
  })
}

export function getMenuWithApp(app_id) {
  return request({
    url: '/pms/resource_menu&app/',
    method: 'get',
    params: { app_id }
  })
}

export function getResourceMenu(id = '') {
  return request({
    url: '/pms/resource_menu/',
    methods: 'get',
    params: { id }
  })
}

export function postResourceMenu(app_id, desc, menu_data) {
  return request({
    url: '/pms/resource_menu/',
    method: 'post',
    data: {
      app_id,
      desc,
      menu_data
    }
  })
}

export function putResourceMenu(menu_id, desc, menu_data) {
  return request({
    url: '/pms/resource_menu/',
    method: 'put',
    data: {
      menu_id,
      desc,
      menu_data
    }
  })
}

export function deleteResourceMenu(id) {
  return request({
    url: '/pms/resource_menu/',
    method: 'delete',
    params: { id }
  })
}

export function menuUniqueCheck(app_id) {
  return request({
    url: '/pms/menu_unique_check/',
    methods: 'get',
    params: { app_id }
  })
}

// Group
// 创建组
export function createGroup(group_name, app_selected, remark) {
  return request({
    url: '/pms/group/',
    method: 'post',
    data: {
      group_name,
      app_selected,
      remark
    }
  })
}

// 获取组列表
export function getGroups() {
  return request({
    url: '/pms/group/',
    method: 'get'
  })
}

// 设置组员/组权限
export function updateGroup(id, act, selected) {
  return request({
    url: '/pms/group/',
    method: 'put',
    data: {
      id,
      act,
      selected
    }
  })
}

// 删除组
export function deleteGroup(id) {
  return request({
    url: '/pms/group/',
    method: 'delete',
    data: {
      id
    }
  })
}

// 获取用户作为穿梭框待选项
export function getUsers(group_id) {
  return request({
    url: '/pms/users/',
    method: 'post',
    data: {
      group_id
    }
  })
}

// 获取权限作为穿梭框待选项
export function getPerms(group_id) {
  return request({
    url: '/pms/perms/',
    method: 'post',
    data: {
      group_id
    }
  })
}

export function groupUniqueCheck(app_id, group_name) {
  return request({
    url: '/pms/group_unique_check/',
    methods: 'get',
    params: {
      app_id,
      group_name
    }
  })
}

// Permission
export function addPermission(form) {
  return request({
    url: '/pms/permission/',
    method: 'post',
    data: { form }
  })
}

export function delPermission(id) {
  return request({
    url: '/pms/permission/',
    method: 'delete',
    params: { id }
  })
}

export function editPermission(form) {
  return request({
    url: '/pms/permission/',
    method: 'put',
    data: { form }
  })
}

export function getPermission(form) {
  return request({
    url: '/pms/permission/',
    method: 'get',
    params: { form }
  })
}

// Perm_menu
export function getPermmenu(form) {
  return request({
    url: '/pms/perm_menu/',
    method: 'get',
    params: { form }
  })
}

export function postPermmenu(form) {
  return request({
    url: '/pms/perm_menu/',
    method: 'post',
    data: { form }
  })
}

export function putPermmenu(form) {
  return request({
    url: '/pms/perm_menu/',
    method: 'put',
    data: { form }
  })
}

export function deletePermmenu(id) {
  return request({
    url: '/pms/perm_menu/',
    method: 'delete',
    params: { id }
  })
}

export function getPermMenuWithApp(app_id) {
  return request({
    url: '/pms/perm_menu&app/',
    method: 'get',
    params: { app_id }
  })
}
