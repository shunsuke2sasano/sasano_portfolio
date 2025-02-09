"""
Django settings for portfolio project.

Generated by 'django-admin startproject' using Django 5.1.3.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-u=_40r*)uola07=j^2h7exkefnr-h$j57!^(y43j6g**@#ma98'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'accounts', 
    'users', 
    'dashboard',
    'django.contrib.admin',
    'django.contrib.auth',
    'inquiry',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles', 
    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'accounts/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'portfolio_db',
        'USER': 'root',
        'PASSWORD': 'Bullshit03Sasano19',
        'HOST': 'portfolio_db',  # 修正: コンテナ名を合わせる
        'PORT': '3306',
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

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

AUTH_USER_MODEL = 'accounts.CustomUser'


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = 'ja'

TIME_ZONE = 'Asia/Tokyo'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = [BASE_DIR / 'static',]

STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

#AUTH_USER_MODEL = 'accounts.CustomUser'

INTERNAL_IPS = [
    '127.0.0.1',
]

MEDIA_URL = '/media/'

MEDIA_ROOT =  os.path.join(BASE_DIR, 'media')

# settings.py
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.office365.com'  # SMTPサーバーのホスト名
EMAIL_PORT = 587 # SMTPサーバーのポート番号
EMAIL_USE_TLS = True  # TLSを使用する場合はTrue
EMAIL_HOST_USER = 's.sasano@oplan.co.jp'  # Outlookの情報
EMAIL_HOST_PASSWORD = 'Sasano#####' # メールアカウントのパスワード
DEFAULT_FROM_EMAIL = 's.sasano@oplan.co.jp'   # メールのデフォルト送信元
NOTIFY_EMAILS = ['potoforiosongfuxian@gmail.com']  # 通知を送信するメールアドレス
ADMIN_EMAIL = 's.sasano@oplan.co.jp'
EMAIL_TIMEOUT = 10 

MESSAGE_STORAGE = 'django.contrib.messages.storage.fallback.FallbackStorage'

SESSION_COOKIE_DOMAIN = None  
SESSION_COOKIE_NAME = 'sessionid'
SESSION_COOKIE_SECURE = False  # HTTPS ではない場合
SESSION_EXPIRE_AT_BROWSER_CLOSE = False  # ブラウザを閉じてもセッション維持
SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # デフォルト
SESSION_COOKIE_NAME = 'sessionid'  # デフォルト
SESSION_COOKIE_SECURE = False  # HTTPSを使用しない場合
SESSION_COOKIE_HTTPONLY = True
SESSION_EXPIRE_AT_BROWSER_CLOSE = False
SESSION_COOKIE_AGE = 3600
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]
