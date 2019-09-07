import os
import time

basedir = os.path.abspath(os.path.dirname(__file__))


class DbConf:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    SQLALCHEMY_TRACK_MODIFICATIONS = True
    SQLALCHEMY_MIGRATE_REPO = os.path.join(basedir, 'db_repository')
    # 安全配置
    CSRF_ENABLED = True
    SECRET_KEY = 'jklklsadhfjkhwbii9/sdf\sdf'
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@127.0.0.1:3306/PMS?charset=utf8mb4'

class LogConf:
    LOGPATH = "logs"
    LOGNAME = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    LOGFORMAT = "%(asctime)s - %(levelname)s - %(filename)s - %(lineno)s - %(message)s"
    LOGLEVEL = "INFO"

class PmsConf:
    APP_ID = 8
    PMS_URL = 'http://127.0.0.1:5000/'
    LOGIN_API = PMS_URL + 'v1/user/login'
    PRIVILEGE_API = PMS_URL + 'v1/pms/getPrivilege/'
    LOGOUT_API = PMS_URL + 'v1/user/logout'
    URL_PRIVILEGE_API = PMS_URL + 'v1/pms/apiPrivilege/'

class MailConf:
    MAIL_DEBUG = True  # 开启debug，便于调试看信息
    MAIL_SUPPRESS_SEND = False  # 发送邮件，为True则不发送
    MAIL_SERVER = 'smtp.qq.com'  # 邮箱服务器
    MAIL_PORT = 465  # 端口
    MAIL_USE_SSL = True  # 重要，qq邮箱需要使用SSL
    MAIL_USE_TLS = False  # 不需要使用TLS
    MAIL_USERNAME = '10000@qq.com'  # 填邮箱
    MAIL_PASSWORD = 'ssxemxmmxtaybbaj'  # 填授权码
    MAIL_DEFAULT_SENDER = '10000@qq.com'  # 填邮箱，默认发送者


class DevelopmentConfig(DbConf, LogConf, MailConf, PmsConf):
    pass
