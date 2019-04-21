from django.apps import AppConfig
from django.conf import settings


class GeneralConfig(AppConfig):
    name = 'brewsql'
    company_name = settings.APP_COMPANY_NAME
    order_key_generate = settings.APP_ORDER_KEY
    mobile_ls = settings.APP_MOBILE
    send_msg = settings.APP_SEND_MSG
    wx_app_id = settings.WX_SECRET_APP_ID
    wx_app_secret = settings.WX_SECRET_APP_SECRET
