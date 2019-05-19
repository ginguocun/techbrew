from django import template

register = template.Library()


@register.filter(name='mobile')
def mobile_hide(mobile='15068826001'):
    if mobile:
        length = len(mobile)
        if length >= 8:
            mobile_1 = mobile[:length - 7]
            mobile_2 = mobile[-3:]
            mobile = mobile_1 + '****' + mobile_2
    return mobile
