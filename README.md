# PMS统一权限管理系统
permission management system 支持多应用的统一权限管理系统，flask+vue实现

# 在线demo:
- pms前端：
  www.seczh.com
- pms后端：
  www.seczh.com:3344
- 账号：
  admin/admin test/test

- 对接应用前端：
  www.devopser.org:81
- 对接应用后端：
  www.devopser.org:7788
- 账号：
  test/test

# 克隆
```
git clone https://github.com/fish2018/pms.git
# 后端
cd backend
# 前端
cd frontend
```

# 后端

## 使用方法

### 修改配置
修改app/config/settings.py使用开发环境配置
```
APP_ENV = DevelopmentConfig
```
修改app/config/dev.py根据自己情况设置数据库等信息，数据库提前创建好
```
CREATE DATABASE `PMS` CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
```
```
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/PMS?charset=utf8mb4'
```
### 安装依赖
```
pip3 install -r requirements.txt
```

### 运行程序，默认监听host='0.0.0.0', port='5000'
```
python3 run.py
```

### 创建第一个用户，PMS默认第一个用户为管理员
http://127.0.0.1:5000 打开swagger，在页面创建用户 username: admin password: admin

![](https://raw.githubusercontent.com/fish2018/pms-template/master/img/backend.jpg)

# 前端

## 使用方法

### 修改配置
修改config/dev.env.js指定后端API地址
```
BASE_API: '"http://127.0.0.1:5000/v1"'
```
修改config/index.js指定前端监听地址
```
    host: '0.0.0.0',
    port: 9999,
```

### 安装依赖
```
npm install --unsafe-perm
```

### 启动程序
```
npm run dev
```

### 登录
http://127.0.0.1:5000 使用刚才创建的账号admin/admin登录

![](https://raw.githubusercontent.com/fish2018/pms-template/master/img/frontend.jpg)
