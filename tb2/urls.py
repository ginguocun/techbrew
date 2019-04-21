"""
This App is written by Guoqun Jin(guoqun.jin@hotmail.com),
in the year of 2018.
"""
from django.contrib import admin
from django.urls import re_path
from django.conf.urls import include
# from django.conf.urls.i18n import i18n_patterns
from .views import *


urlpatterns = [
    re_path(r'^api/brewsql/', include('brewsql.urls_api', namespace='brewsql-api')),
    re_path(r'^brix-plato$', brix_plato, name='brix_plato'),
    re_path(r'', include('brewsql.urls', namespace='brewsql')),
    re_path(r'^admincjzh/', admin.site.urls, name='admin'),
    re_path(r'^accounts/login/$', tb_login, name='login'),
    re_path(r'^accounts/logout/$', tb_logout, name='logout')
]

# urlpatterns += i18n_patterns(
#     re_path(r'^brix-plato$', brix_plato, name='brix_plato'),
#     re_path(r'', include('brewsql.urls', namespace='brewsql')),
#     re_path(r'^admincjzh/', admin.site.urls, name='admin'),
#     re_path(r'^accounts/login/$', tb_login, name='login'),
#     re_path(r'^accounts/logout/$', tb_logout, name='logout')
# )
