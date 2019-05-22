from django.core.paginator import Paginator
import math
import datetime
import re


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


def object_paginator(request, object_list, per_page_count=20, nav_l=3):
    paginator = Paginator(object_list, per_page_count)
    # paginator, page, queryset, is_paginated = self.paginate_queryset(queryset, page_size)
    page = request.GET.get('page')
    if page is None:
        page = 1
    queryset = paginator.get_page(page)
    page_range = []
    for p in range(1, paginator.num_pages + 1):
        if abs(p - int(page)) - (int(nav_l) / 2) <= 0:
            page_range.append(p)
        elif int(page) - nav_l // 2 <= 0 and p <= nav_l:
            page_range.append(p)
        elif int(page) - paginator.num_pages + nav_l // 2 >= 0 and p - paginator.num_pages + nav_l - 1 >= 0:
            page_range.append(p)
    return {
                'paginator': paginator,
                'page_obj': page,
                'page_range': page,
                'is_paginated': True,
                'data': queryset
            }


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


if __name__ == '__main__':
    print(validate_date('2019/0/1'))
