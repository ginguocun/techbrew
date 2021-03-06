import datetime
import math
import re

from django.contrib.auth.models import Permission
from django.core.exceptions import ImproperlyConfigured


def get_obj_permission_required(obj):
    if obj.permission_required is None:
        if obj.model is None:
            raise ImproperlyConfigured(
                '{0} is missing the model attribute.'.format(obj.__class__.__name__)
            )
        else:
            obj.permission_required = obj.get_required_object_permissions(obj.model)
    if isinstance(obj.permission_required, str):
        perms = (obj.permission_required,)
    else:
        perms = obj.permission_required
    return perms


def convert_num_to_chinese(t_price):
    dict_chinese = [u'零', u'壹', u'贰', u'叁', u'肆', u'伍', u'陆', u'柒', u'捌', u'玖']
    unit_chinese = [u'', u'拾', u'佰', u'仟', '', u'拾', u'佰', u'仟']
    part_a = int(math.floor(t_price))
    part_b = round(t_price - part_a, 2)
    str_part_a = str(part_a)
    str_part_b = ''

    if part_b != 0:
        str_part_b = str(part_b)[2:]

    single_num = []
    if len(str_part_a) != 0:
        i = 0
        while i < len(str_part_a):
            single_num.append(str_part_a[i])
            i += 1
    t_num_chinese_part_a = []
    num_chinese_part_a = []
    j = 0
    bef = '0'
    if len(str_part_a) != 0:
        while j < len(str_part_a):
            curr = single_num.pop()
            if curr == '0' and bef != '0':
                t_num_chinese_part_a.append(dict_chinese[0])
                bef = curr
            if curr != '0':
                t_num_chinese_part_a.append(unit_chinese[j])
                t_num_chinese_part_a.append(dict_chinese[int(curr)])
                bef = curr
            if j == 3:
                t_num_chinese_part_a.append(u'万')
                bef = '0'
            j += 1

        for i in range(len(t_num_chinese_part_a)):
            num_chinese_part_a.append(t_num_chinese_part_a.pop())

    a = ''
    for i in num_chinese_part_a:
        a = a + i

    b = ''
    if len(str_part_b) == 1:
        b = dict_chinese[int(str_part_b[0])] + u'角'
    if len(str_part_b) == 2 and str_part_b[0] != '0':
        b = dict_chinese[int(str_part_b[0])] + u'角' + dict_chinese[int(str_part_b[1])] + u'分'
    if len(str_part_b) == 2 and str_part_b[0] == '0':
        b = dict_chinese[int(str_part_b[0])] + dict_chinese[int(str_part_b[1])] + u'分'
    s = ''
    if len(str_part_b) == 0:
        s = a + u'圆整'
    if len(str_part_b) != 0:
        s = a + u'圆' + b
    return s


def plato2sg(plato=12):
    sg = 1 + (plato/(258.6-((plato/258.2)*227.1)))
    return sg


def sg2plato(sg=1.048):
    plato = (-1 * 616.868) + (1111.14 * sg) - (630.272 * sg ** 2) + (135.997 * sg ** 3)
    return plato


def validate_date(date_text):
    if not date_text:
        return False
    try:
        date_reg_exp_1 = re.compile('\d{4}[-/]\d{1,2}[-/]\d{1,2}')
        matches_list = date_reg_exp_1.findall(date_text)
        if matches_list:
            date_text = matches_list[0].replace('/', '-')
            date_text = datetime.datetime.strptime(date_text, "%Y-%m-%d").strftime('%Y-%m-%d')
            return date_text
    except ValueError:
        return False
        # raise ValueError("错误是日期格式或日期,格式是年-月-日")


def update_permissions_name():
    ps = Permission.objects.all()
    c = 0
    t_c = 0
    for p in ps:
        t_c += 1
        if 'Can view' in p.name:
            p.name = str(p.name).replace('Can view ', '可以查看')
            c += 1
        if 'Can add' in p.name:
            p.name = str(p.name).replace('Can add ', '可以添加')
            c += 1
        if 'Can delete' in p.name:
            p.name = str(p.name).replace('Can delete ', '可以删除')
            c += 1
        if 'Can change' in p.name:
            p.name = str(p.name).replace('Can change ', '可以修改')
            c += 1
        if 'user' in p.name:
            p.name = str(p.name).replace('user', '用户')
        if 'group' in p.name:
            p.name = str(p.name).replace('group', '权限分组')
        if 'permission' in p.name:
            p.name = str(p.name).replace('permission', '权限')
        if 'log entry' in p.name:
            p.name = str(p.name).replace('log entry', '日志')
        if 'content type' in p.name:
            p.name = str(p.name).replace('content type', '内容类型')
        if 'session' in p.name:
            p.name = str(p.name).replace('session', '会话')
        p.save()
    print('总共{}条，更新了{}条'.format(t_c, c))
