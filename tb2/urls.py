"""
Written by Guoqun Jin(guoqun.jin@hotmail.com),
2019-05-01
"""
from django.contrib import admin
from django.urls import re_path
from django.conf import settings
from django.conf.urls import include
# from django.conf.urls.i18n import i18n_patterns
from django.http import Http404, HttpResponseRedirect
# from django.http import FileResponse
# import mimetypes
from django.contrib.auth.decorators import login_required
from django.utils.translation import gettext as _
from .views import *
import oss2


@login_required
def oss2_serve(request, path):
    auth = oss2.Auth(settings.ACCESS_KEY_ID, settings.ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, settings.END_POINT, settings.BUCKET_NAME)
    if settings.MEDIA_URL:
        full_path = '{0}{1}'.format(settings.MEDIA_URL, path)
    else:
        full_path = path
    try:
        secret_url = bucket.sign_url('GET', full_path[1:], 5 * 60)
    except oss2.exceptions.NoSuchKey:
        raise Http404(_('"%(path)s" does not exist') % {'path': full_path})
    return HttpResponseRedirect(redirect_to=secret_url)
    # try:
    #     oj = bucket.get_object(str(full_path[1:]).encode('utf-8'))
    # except oss2.exceptions.NoSuchKey:
    #     raise Http404(_('"%(path)s" does not exist') % {'path': full_path})
    # content_type, encoding = mimetypes.guess_type(str(full_path))
    # content_type = content_type or 'application/octet-stream'
    # response = FileResponse(oj, content_type=content_type, as_attachment=True)
    # if encoding:
    #     response["Content-Encoding"] = encoding
    # return response


urlpatterns = [
    re_path(r'^api/brewsql/', include('brewsql.urls_api', namespace='brewsql-api')),
    re_path(r'^brix-plato$', brix_plato, name='brix_plato'),
    re_path(r'', include('brewsql.urls', namespace='brewsql')),
    re_path(r'^admincjzh/', admin.site.urls, name='admin'),
    re_path(r'^accounts/login/$', tb_login, name='login'),
    re_path(r'^accounts/logout/$', tb_logout, name='logout'),
    re_path(r'^%s(?P<path>.*)$' % settings.MEDIA_URL[1:], oss2_serve),
]

# urlpatterns += i18n_patterns(
#     re_path(r'^brix-plato$', brix_plato, name='brix_plato'),
#     re_path(r'', include('brewsql.urls', namespace='brewsql')),
#     re_path(r'^admincjzh/', admin.site.urls, name='admin'),
#     re_path(r'^accounts/login/$', tb_login, name='login'),
#     re_path(r'^accounts/logout/$', tb_logout, name='logout')
# )
