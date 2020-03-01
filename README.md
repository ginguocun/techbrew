# techbrew
这是一套适用于小型酿造酒厂的生产、销售、财务及人员管理系统。
建议采用 Nginx-uWsgi-Django 的方式进行服务部署。

### 安装说明
#### 拉取代码
```
git clone https://github.com/ginguocun/techbrew.git
```
#### 配置 settings.py

在项目的 tb2 目录下面添加 **settings.py** 文件

项目采用阿里云 oss 进行图片存储，所以需要自行申请 oss 并且进行配置。

```
# 域名配置
import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 请配置一个足够复杂的SECRET_KEY
SECRET_KEY = '******'

# 生产环境请将 DEBUG 设置为 False
DEBUG = True

# 域名和 ip 配置
ALLOWED_HOSTS = ['0.0.0.0', '127.0.0.1']

SESSION_COOKIE_AGE = 80000

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'aliyun_oss2_storage',
    'rest_framework',
    'brewsql',
    'django_filters'
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'tb2.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media'
            ],
        },
    },
]

WSGI_APPLICATION = 'tb2.wsgi.application'

LOGIN_URL = '/accounts/login/'

LOGIN_REDIRECT_URL = ''

LOGOUT_REDIRECT_URL = ''

# Database
# https://docs.djangoproject.com/en/2.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': '******',
        'USER': '******',
        'PASSWORD': '******',
        'HOST': 'localhost',
        'PORT': '',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/2.2/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = True

DEFAULT_CHARSET = 'utf-8'

FILE_CHARSET = 'utf-8'

LANGUAGES = (
    ('en', 'English'),
    ('zh-hans', '中文简体'),
    ('zh-hant', '中文繁體'),
)

LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.2/howto/static-files/

STATIC_URL = '/static/'
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'static'), ]
STATICFILES_FINDERS = (
  'django.contrib.staticfiles.finders.FileSystemFinder',
  'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

MEDIA_URL = '/media/'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': ('django_filters.rest_framework.DjangoFilterBackend',)
}

JWT_SIGNING_KEY = ''******''

EMAIL_HOST = 'smtp.163.com'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'techbrew@163.com'
EMAIL_HOST_PASSWORD = '******'
EMAIL_USE_LOCALTIME = True
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

APP_COMPANY_NAME = '科学酿造'

APP_ORDER_KEY = '******'

WX_SECRET_APP_ID = '******'
WX_SECRET_APP_SECRET = '******'

# https://pypi.org/project/django-aliyun-oss2-storage/
DEFAULT_FILE_STORAGE = 'aliyun_oss2_storage.backends.AliyunMediaStorage'
DEFAULT_MEDIA_STORAGE = 'aliyun_oss2_storage.backends.AliyunMediaStorage'
ACCESS_KEY_ID = "******"
ACCESS_KEY_SECRET = "******"
END_POINT = "oss-cn-zhangjiakou.aliyuncs.com"
BUCKET_NAME = "******"
BUCKET_ACL_TYPE = "private"

```

#### 安装相应的依赖

```
pip install -r requirements.txt
```

#### 启动服务

```
uwsgi --ini tb2_uwsgi.ini
```