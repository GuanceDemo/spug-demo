"""
# Copyright: (c) OpenSpug Organization. https://github.com/openspug/spug
# Copyright: (c) <spug.dev@gmail.com>
# Released under the AGPL-3.0 License.

Django settings for spug project.

Generated by 'django-admin startproject' using Django 2.2.7.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.2/ref/settings/
"""

import os
import re
from ddtrace import tracer
import logging

redis_host = os.environ.get('REDIS_HOST',"127.0.0.1")
redis_port = os.environ.get('REDIS_PORT',"6379")
redis_url = "redis://"+ str(redis_host) + ":"  + str(redis_port) + "/1"
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'vk0do47)egwzz!uk49%(y3s(fpx4+ha@ugt-hcv&%&d@hwr&p7'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'apps.account',
    'apps.host',
    'apps.setting',
    'apps.exec',
    'apps.schedule',
    'apps.monitor',
    'apps.alarm',
    'apps.config',
    'apps.app',
    'apps.deploy',
    'apps.notify',
    'apps.repository',
    'apps.home',
    'channels',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.middleware.common.CommonMiddleware',
    'libs.middleware.AuthenticationMiddleware',
    'libs.middleware.HandleExceptionMiddleware',
]

ROOT_URLCONF = 'spug.urls'

WSGI_APPLICATION = 'spug.wsgi.application'
ASGI_APPLICATION = 'spug.routing.application'

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ATOMIC_REQUESTS': True,
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": redis_url,
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [(redis_host, redis_port)],
            "capacity": 1000,
            "expiry": 120,
        },
    },
}

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': False,
    },
]

TOKEN_TTL = 8 * 3600
SCHEDULE_KEY = 'spug:schedule'
SCHEDULE_WORKER_KEY = 'spug:schedule:worker'
MONITOR_KEY = 'spug:monitor'
MONITOR_WORKER_KEY = 'spug:monitor:worker'
EXEC_WORKER_KEY = 'spug:exec:worker'
REQUEST_KEY = 'spug:request'
BUILD_KEY = 'spug:build'
REPOS_DIR = os.path.join(os.path.dirname(os.path.dirname(BASE_DIR)), 'repos')
BUILD_DIR = os.path.join(REPOS_DIR, 'build')
TRANSFER_DIR = os.path.join(BASE_DIR, 'storage', 'transfer')

# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False

AUTHENTICATION_EXCLUDES = (
    '/account/login/',
    '/setting/basic/',
    re.compile('/apis/.*'),
)

SPUG_VERSION = 'v3.2.7'

# override default config
try:
    from spug.overrides import *
except ImportError:
    pass


# FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
#           '[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
#           '- %(message)s')
# logging.basicConfig(level=logging.INFO,format=FORMAT)

# 日志配置


# #1、配置日志要保存的文件夹，创建文件夹
# import time
# BASE_LOG_DIR = os.path.join(BASE_DIR, 'logs')
# error_path = os.path.join(BASE_DIR,'error')
# if not os.path.exists(error_path):
#     #如果logs/error/不存在，递归创建目录
#     os.makedirs(error_path)
 
# all_path = os.path.join(BASE_LOG_DIR,'all')
# if not os.path.exists(all_path):
#     #如果logs/all/目录不存在，就递归创建(如果logs目录不存在，也会创建)
#     os.makedirs(all_path)


FORMAT = ('%(asctime)s %(levelname)s [%(name)s] [%(filename)s:%(lineno)d] '
          '[dd.service=%(dd.service)s dd.env=%(dd.env)s dd.version=%(dd.version)s dd.trace_id=%(dd.trace_id)s dd.span_id=%(dd.span_id)s] '
          '- %(message)s')

logging.basicConfig(level=logging.INFO,format=FORMAT)

# #2、相关的日志配置
# LOGGING = {
#     'version': 1,
#     'disable_existing_loggers': False,  # 设置已存在的logger不失效
#     'filters': {
#     },
#     'formatters': {
#         'standard': {
#             'format': FORMAT,
#             'datefmt': '%Y-%m-%d %H:%M:%S'
#         },
#         'simple': {
#             'format': '[%(asctime)s][%(levelname)s]：%(message)s',
#             'datefmt': '%Y-%m-%d %H:%M:%S'
#         }
#     },
#     'handlers': {
#         'console': {
#             'level': 'DEBUG',
#             'class': 'logging.StreamHandler',
#             'formatter': 'simple'
#         },
#         'file': { #按照文件大小分割日志，将所有的日志信息都保存在这里
#             'level': 'DEBUG',
#             'class': 'logging.handlers.RotatingFileHandler',
#             'filename': os.path.join(BASE_LOG_DIR,'all', 'debug.log'),
#             'maxBytes': 1024 * 1024 * 50,  # 日志大小50M
#             'backupCount': 5,
#             'formatter': 'standard',
#             'encoding': 'utf-8',
#         },
#         'time_file':{#按照时间分割日志，每周一新增一个日志文件，存error等级以上的日志
#               'level': 'INFO',#日志的等级
#               'class': 'logging.handlers.TimedRotatingFileHandler',
#               'filename': os.path.join(BASE_LOG_DIR,'error',f"{time.strftime('%Y-%m-%d')}.log"),#日志的文件名
#               'when': 'D', #时间单位，M,H,D,'W0'(星期1),'W6'（星期天）
#               'interval': 1,
#               'backupCount': 5, #备份数量
#               'formatter': 'standard', #使用的日志格式
#               'encoding': 'utf-8',
#         }
 
#     },
#     'loggers': {
#         #INFO以上日志，打印在console，也写到以文件大小分割的日志中
#         'django': {
#             'handlers': ['console','file'],#handlers中存在的配置
#             'level': 'INFO',
#             'propagate': True
#         },
#         #error以上的日志写到按时间分割的日志文件中，同时打印在控制台
#         'django.request': {
#             'handlers': ['console','time_file'],#handlers中存在的配置
#             'level': 'ERROR',
#             'propagate': True
#         },
 
#     },
# }



LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': FORMAT,
            'style': '{',
        },
        'simple': {
            'format': FORMAT,
            'style': '{',
        },
        "default": {
            "format": FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default'
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.TimedRotatingFileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/debug.log'),
            'when': "D",
            'interval': 1,
            'formatter': 'default'
        },
        "request": {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/request.log'),
            'formatter': 'default'
        },
        "server": {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/server.log'),
            'formatter': 'default'
        },
        "root": {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/root.log'),
            'formatter': 'default'
        },
 
        "db_backends": {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/db_backends.log'),
            'formatter': 'default'
        },
        "autoreload": {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(BASE_DIR, 'logs/autoreload.log'),
            'formatter': 'default'
        }
    }
}
