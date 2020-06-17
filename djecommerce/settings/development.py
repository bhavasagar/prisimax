from .base import *
import os

DEBUG = True
ALLOWED_HOSTS = ['167.71.238.234','presimax.online','www.presimax.online']

SESSION_COOKIE_AGE = 60 * 60 * 24 * 30 # One month

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'myproject',
        'USER': 'myprojectuser',
        'PASSWORD': 'password',
        'HOST': 'localhost',
        'PORT': '',
    }
}



PAYTM_MERCHANT_ID = 'ZdBbsm80690060809413'
PAYTM_SECRET_KEY = 'R6xrODspE8O!_7I5'
PAYTM_WEBSITE = 'DEFAULT'
PAYTM_CHANNEL_ID = 'WEB'
PAYTM_INDUSTRY_TYPE_ID = 'Retail'