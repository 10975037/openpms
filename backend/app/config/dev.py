import os
import time

basedir = os.path.abspath(os.path.dirname(__file__))


class DbConf:
    SQLALCHEMY_COMMIT_ON_TEARDOWN = True
    # SQLALCHEMY_TRACH_MODIFICATIONS = False
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

class PmsConf:
    APP_ID = 1 # PMS 默认 APP_ID = 1，admin id = 1，鉴权里会用到

class DevelopmentConfig(DbConf, LogConf, MailConf, PmsConf):
    pass
