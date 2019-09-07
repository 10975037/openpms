import request from '@/utils/request'

export function login(username, password) {
  return request({
    url: '/pms/login/',
    method: 'post',
    data: {
      username,
      password
    }
  })
}

export function getInfo(token) {
  return request({
    url: '/pms/user_privilege/',
    method: 'post',
    data: { token }
  })
}

export function logout() {
  return request({
    url: '/pms/logout/',
    method: 'post'
  })
}
