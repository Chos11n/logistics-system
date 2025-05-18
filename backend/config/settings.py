import os
import sys
from pathlib import Path
from dotenv import load_dotenv

# 加载环境变量（docker-compose 传入）
load_dotenv()

# 基础路径
BASE_DIR = Path(__file__).resolve().parent.parent

# ==================== #
# 安全配置（生产环境必须！）
# ==================== #
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'django-insecure-dev-key')

DEBUG = os.environ.get('DEBUG', 'False').lower() == 'true'

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

CSRF_TRUSTED_ORIGINS = [
    'https://*.logistics.com',
    'http://localhost:3000'
]

# ==================== #
# 应用定义
# ==================== #
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',  # 生产静态文件
    'django.contrib.staticfiles',
    
    # 第三方库
    'rest_framework',
    'corsheaders',
    'django_filters',
    
    # 物流系统模块
    'logistics.core',
    'logistics.orders',
    'logistics.inventory',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # 静态文件缓存
    'corsheaders.middleware.CorsMiddleware',       # CORS处理
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# ==================== #
# 数据库配置（PostgreSQL优化）
# ==================== #
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'logistics'),
        'USER': os.environ.get('DB_USER', 'logistics'),
        'PASSWORD': os.environ.get('DB_PASSWORD', ''),
        'HOST': os.environ.get('DB_HOST', 'database'),
        'PORT': os.environ.get('DB_PORT', '5432'),
        'CONN_MAX_AGE': 600,  # 连接池
        'OPTIONS': {
            'application_name': 'logistics_django',
            'connect_timeout': 10,
        }
    }
}

if 'test' in sys.argv:
    DATABASES['default'] = {'ENGINE': 'django.db.backends.sqlite3'}

# ==================== #
# 缓存配置（Redis）
# ==================== #
CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": f"redis://{os.environ.get('REDIS_HOST', 'redis')}:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
            "CONNECTION_POOL_KWARGS": {"max_connections": 100}
        },
        "KEY_PREFIX": "logistics"
    }
}

# ==================== #
# REST框架配置
# ==================== #
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/hour',
        'user': '1000/hour'
    }
}

# ==================== #
# 文件存储（生产环境建议使用S3）
# ==================== #
DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
AWS_ACCESS_KEY_ID = os.environ.get('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
AWS_STORAGE_BUCKET_NAME = 'logistics-files'
AWS_S3_REGION_NAME = 'ap-southeast-1'

# ==================== #
# 日志配置
# ==================== #
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': '{levelname} {asctime} {module} {message}',
            'style': '{',
        },
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'file': {
            'level': 'ERROR',
            'class': 'logging.handlers.RotatingFileHandler',
            'filename': '/var/log/django/error.log',
            'maxBytes': 1024*1024*5,  # 5MB
            'backupCount': 5,
        },
    },
    'loggers': {
        'django': {
            'handlers': ['console', 'file'],
            'level': os.environ.get('LOG_LEVEL', 'INFO'),
        },
    },
}

# ==================== #
# 其他关键配置
# ==================== #
ROOT_URLCONF = 'config.urls'
WSGI_APPLICATION = 'config.wsgi.application'
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# 国际化
LANGUAGE_CODE = 'zh-hans'
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_TZ = True

# CORS配置
CORS_ALLOWED_ORIGINS = [
    "http://localhost:3000",
    "https://logistics-web.com"
]
CORS_ALLOW_CREDENTIALS = True

# 安全头（生产环境启用）
if not DEBUG:
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True