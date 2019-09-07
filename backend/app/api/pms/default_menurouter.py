default_menurouter = [
  {
    "path": '/pms',
    "component": 'Layout',
    "redirect": '/pms/resource/application',
    "name": 'PMS',
    "meta": { "title": 'PMS', "icon": 'example' },
    "children": [
      {
        "path": 'resource',
        "name": 'Resource',
        "component": '/pms/resource/index.vue',
        "redirect": '/pms/resource/application',
        "meta": { "title": '资源管理', "icon": 'table' },
        "children": [
          {
            "path": 'application',
            "name": 'Application',
            "component": '/pms/resource/application/index.vue',
            "meta": { "title": '应用系统', "icon": 'table' }
          },
         {
            "path": 'app_resource',
            "name": 'AppResource',
            "component": '/pms/resource/appResource/index.vue',
            "meta": { "title": '应用资源', "icon": 'table' }
          },
         {
            "path": 'menu',
            "name": 'Menu',
            "component": '/pms/resource/menu/index.vue',
            "meta": { "title": '应用菜单', "icon": 'table' }
          }
        ]
      },
      {
        "path": 'permission',
        "name": 'Permission',
        "component": '/pms/permission/index.vue',
        "meta": { "title": '权限管理', "icon": 'table' },
        "children": [
          {
            "path": 'resource',
            "name": 'ResourcePermission',
            "component": '/pms/permission/resource/index.vue',
            "meta": { "title": '资源权限', "icon": 'table' },
          },
         {
            "path": 'menu',
            "name": 'MenuPermission',
            "component": '/pms/permission/menu/index.vue',
            "meta": { "title": '菜单权限', "icon": 'table' },
          }
        ]
      },
      {
        "path": 'group',
        "name": 'Group',
        "component":'/pms/organization/index.vue',
        "meta": { "title": '组织管理', "icon": 'table' }
      }
    ]
  }
]
