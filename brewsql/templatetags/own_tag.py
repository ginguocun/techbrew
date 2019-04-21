from django import template
from tb2.settings import QINIU_BUCKET_DOMAIN

register = template.Library()


@register.filter(name='qiniu')
def make_qiniu_url(source_string):
    res = 'http://{0}{1}'.format(QINIU_BUCKET_DOMAIN, source_string)
    return res


@register.filter(name='mobile')
def mobile_hide(mobile='15068826001'):
    if mobile:
        length = len(mobile)
        if length >= 8:
            mobile_1 = mobile[:length - 7]
            mobile_2 = mobile[-3:]
            mobile = mobile_1 + '****' + mobile_2
    return mobile
