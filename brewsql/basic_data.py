#!/usr/bin/python
# -*- coding: utf-8 -*-
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tb2.settings")


import django
django.setup()


from brewsql.models import *


def create_money_in_out_types(ob=MoneyInOutType):
    data = [
        {'id': '1', 'money_in_out_type_cn': '采购原料支出', 'money_in_out_type_en': 'Cost for buying materials',
         'is_negative': True, 'is_auto': True},
        {'id': '2', 'money_in_out_type_cn': '出售产品收入', 'money_in_out_type_en': 'Income from selling products',
         'is_negative':  False, 'is_auto': True},
        {'id': '3', 'money_in_out_type_cn': '日常支出', 'money_in_out_type_en': 'Daily spending',
         'is_negative': True, 'is_auto': False},
        {'id': '4', 'money_in_out_type_cn': '股东注资', 'money_in_out_type_en': 'Investment from shareholders',
         'is_negative': False, 'is_auto': False},
    ]
    for d in data:
        new_item = ob(
            money_in_out_type_cn=d['money_in_out_type_cn'],
            money_in_out_type_en=d['money_in_out_type_en'],
            is_negative=d['is_negative'],
            is_auto=d['is_auto'],
        )
        new_item.save()
        print('new item saved [{0}] {1}'.format(new_item.pk, new_item))


def create_tank_states(ob=TankState):
    data = [
        {'state_en': 'fermentation', 'state_cn': '正在发酵', 'with_product': True},
        {'state_en': 'cooling down', 'state_cn': '正在降温', 'with_product': True},
        {'state_en': 'maturation', 'state_cn': '正在冷储', 'with_product': True},
        {'state_en': 'ready to pack', 'state_cn': '可以灌装', 'with_product': True},
        {'state_en': 'need to clean', 'state_cn': '需要清洗', 'with_product': False},
        {'state_en': 'ready to use', 'state_cn': '可以使用', 'with_product': False},
        {'state_en': 'need to repair', 'state_cn': '需要检修', 'with_product': False},
    ]
    for d in data:
        new_item = ob(
            tank_state_en=d['state_en'],
            tank_state_cn=d['state_cn'],
            with_product=d['with_product'],
        )
        new_item.save()
        print('new item saved [{0}] {1}'.format(new_item.pk, new_item))


def create_product_types(ob=ProductType):
    data = [
        {'code': '0', 'name_cn': '自有产品', 'name_en': 'own product'},
        {'code': '1', 'name_cn': '代工产品', 'name_en': 'contract product'},
        {'code': '2', 'name_cn': '实验产品', 'name_en': 'test product'},
    ]
    for d in data:
        new_item = ob(
            product_type_code=d['code'],
            product_type_name_cn=d['name_cn'],
            product_type_name_en=d['name_en'],
        )
        new_item.save()
        print('new item saved [{0}] {1}'.format(new_item.pk, new_item))


def create_material_categories(ob=MaterialCategory):
    data = [
        {'code': 'M', 'name_cn': '麦芽', 'name_en': 'malts'},
        {'code': 'H', 'name_cn': '酒花', 'name_en': 'hops'},
        {'code': 'Y', 'name_cn': '酵母', 'name_en': 'yeasts'},
        {'code': 'F', 'name_cn': '辅料', 'name_en': 'accessories'},
        {'code': 'C', 'name_cn': '清洗剂', 'name_en': 'cleaners'},
        {'code': 'P', 'name_cn': '包装物', 'name_en': 'packs'},
        {'code': 'T', 'name_cn': '日用品', 'name_en': 'tools'},
        {'code': 'O', 'name_cn': '其他物品', 'name_en': 'others'},
    ]
    for d in data:
        new_item = ob(
            material_category_code=d['code'],
            material_category_en=d['name_en'],
            material_category_cn=d['name_cn'],
        )
        new_item.save()
        print('new item saved [{0}] {1}'.format(new_item.pk, new_item))


def create_tanks(s=1, e=30, tank_name='FV', volume=2000, ob=Tank):
    for t in range(s, e + 1):
        new_item = ob(
            tank_code='{0}'.format(str(t).zfill(2)),
            tank_name='{1}{0}'.format(str(t).zfill(2), tank_name),
            tank_standard_volume=volume,
        )
        new_item.save()
        print('new item saved [{0}] {1}'.format(new_item.pk, new_item))


def create_product_packs(ob=ProductPackSizeUnit):
    data = [
        {'size': '30', 'unit': 'L', 'type_en': 'stainless steel', 'type_cn': '不锈钢桶', 'type_c': 'A'},
        {'size': '20', 'unit': 'L', 'type_en': 'stainless steel', 'type_cn': '不锈钢桶', 'type_c': 'B'},
        {'size': '30', 'unit': 'L', 'type_en': 'KeyKeg', 'type_cn': '一次性桶', 'type_c': 'C'},
        {'size': '5', 'unit': 'L', 'type_en': 'Metal', 'type_cn': '马口铁罐', 'type_c': 'D'},
        {'size': '330', 'unit': 'mL', 'type_en': 'glass bottle', 'type_cn': '玻璃瓶', 'type_c': 'E'},
        {'size': '500', 'unit': 'mL', 'type_en': 'glass bottle', 'type_cn': '玻璃瓶', 'type_c': 'F'},
        {'size': '330', 'unit': 'mL', 'type_en': 'can', 'type_cn': '易拉罐', 'type_c': 'G'},
        {'size': '500', 'unit': 'mL', 'type_en': 'can', 'type_cn': '易拉罐', 'type_c': 'H'},
    ]
    for d in data:
        new_item = ob(
            product_pack_size=d['size'],
            product_pack_unit=d['unit'],
            product_pack_type_en=d['type_en'],
            product_pack_type_cn=d['type_cn'],
            product_pack_code=d['type_c'],
        )
        new_item.save()
        print('new item saved [{0}] {1}'.format(new_item.pk, new_item))


def create_employee_state(ob=EmployeeState):
    data = [
        {'id': '1', 'employee_state_cn': '在职', 'employee_state_en': 'Working'},
        {'id': '2', 'employee_state_cn': '离职', 'employee_state_en': 'Have left'},
        {'id': '2', 'employee_state_cn': '休假', 'employee_state_en': 'on holiday'},
    ]
    for d in data:
        new_item = ob(
            employee_state_cn=d['employee_state_cn'],
            employee_state_en=d['employee_state_en'],
        )
        new_item.save()
        print('new item saved [{0}] {1}'.format(new_item.pk, new_item))


def create_company_type(ob=CompanyType):
    data = [
        {'id': '1', 'company_type_en': 'Materials Supplier', 'company_type_cn': '原料供应商'},
        {'id': '2', 'company_type_en': 'Bar Client', 'company_type_cn': '酒吧客户'},
        {'id': '3', 'company_type_en': 'Beer Distributor', 'company_type_cn': '啤酒经销商'},
    ]
    for d in data:
        new_item = ob(
            company_type_en=d['company_type_en'],
            company_type_cn=d['company_type_cn'],
        )
        new_item.save()
        print('new item saved [{0}] {1}'.format(new_item.pk, new_item))


def create_order_state(ob=OrderState):
    data = [
        {'id': '1', 'order_state_cn': '待付款', 'order_state_en': 'Pending'},
        {'id': '2', 'order_state_cn': '待发货', 'order_state_en': 'Processing'},
        {'id': '3', 'order_state_cn': '待收货', 'order_state_en': 'Shipping'},
        {'id': '4', 'order_state_cn': '已收货', 'order_state_en': 'Completed'},
        {'id': '5', 'order_state_cn': '退款/售后', 'order_state_en': 'Service'},
        {'id': '6', 'order_state_cn': '发货未付款', 'order_state_en': 'Need To Pay'},
        {'id': '7', 'order_state_cn': '待处理', 'order_state_en': 'Follow Up'},
    ]
    for d in data:
        new_item = ob(
            order_state_cn=d['order_state_cn'],
            order_state_en=d['order_state_en'],
        )
        new_item.save()
        print('new item saved [{0}] {1}'.format(new_item.pk, new_item))


def add_init_data():
    create_money_in_out_types()
    create_tank_states()
    create_product_types()
    create_material_categories()
    create_tanks(1, 10, 'FV', 2000)
    create_tanks(11, 30, 'FV', 4000)
    create_product_packs()
    create_employee_state()
    create_company_type()
    create_order_state()


def test_send_email():
    from django.core.mail import send_mail

    send_mail(
        '今晚开会',
        '今晚8点半办公室开会, 常用当地时间。',
        'techbrew@163.com',
        ['2008----bjhyn@163.com'],
        fail_silently=False,
    )


if __name__ == '__main__':
    print(test_send_email())
