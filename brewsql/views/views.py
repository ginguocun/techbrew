from django.shortcuts import render, HttpResponse
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.admin.models import LogEntry
from django.db.models.functions import TruncMonth
from ..utils import object_paginator, table_create, validate_date
import json
from ..forms import *


app_name = GeneralConfig.name


def income_by_products_pie(sale_incomes=None):
    if not sale_incomes:
        sale_incomes = Sale.objects.exclude(sale_price_link__isnull=True).filter(
            is_active=True).filter(is_confirmed=True)
    income_by_products = list()
    for p in Product.objects.all():
        s_i_p = sale_incomes.filter(pack__product_id=p.pk).annotate(
            mio=Sum('sale_price_link__money_in_out')).values('mio')
        if s_i_p:
            mio = 0
            for sss in s_i_p:
                mio += float(sss['mio'])
            income_by_products.append(['{0} [{1}]'.format(p.product_name.product_name_cn,
                                                          p.product_pack.product_pack_size_unit_cn), mio])
    return income_by_products


def outcome_by_types_pie(outcomes=None):
    if not outcomes:
        outcomes = MoneyInOut.objects.filter(is_confirmed=True).filter(is_active=True)
    outcome_by_types = list()
    for t in MoneyInOutType.objects.filter(is_negative=True):
        o_p = outcomes.filter(money_in_out_type_id=t.pk).annotate(mio=Sum('money_in_out')).values('mio')
        if o_p:
            mio = 0
            for sss in o_p:
                mio += float(sss['mio'])
            outcome_by_types.append(['{0}'.format(t.money_in_out_type_cn), - mio])
    return outcome_by_types


def io_per_month_column():
    io_per_month = None
    in_out_month = list()
    income_info = list()
    total_income = 0
    total_outcome = 0
    outcome_info = list()
    io_come_info = list()
    month_l = list()
    money_in_out = MoneyInOut.objects.exclude(
        money_in_out_date__isnull=True).filter(is_active=True).filter(is_confirmed=True)
    if money_in_out:
        io_per_month = money_in_out.annotate(
            month=TruncMonth('money_in_out_date')).annotate(sum=Sum('money_in_out')).values(
            'month', 'sum').order_by('month')
    if io_per_month:
        for opm in io_per_month:
            if opm['month'] not in month_l:
                in_out_month.append('{0}'.format(opm['month'].strftime("%Y-%m")))
                io_come_info.append(float(opm['sum']))
                if float(opm['sum']) > 0:
                    income_info.append(float(opm['sum']))
                    outcome_info.append(0)
                    total_income += float(opm['sum'])
                else:
                    income_info.append(0)
                    outcome_info.append(float(opm['sum']))
                    total_outcome += float(opm['sum'])
                month_l.append(opm['month'])
            else:
                io_come_info[-1] += float(opm['sum'])
                if float(opm['sum']) > 0:
                    income_info[-1] += float(opm['sum'])
                    total_income += float(opm['sum'])
                else:
                    outcome_info[-1] += float(opm['sum'])
                    total_outcome += float(opm['sum'])
    return [in_out_month, income_info, outcome_info, io_come_info, total_income, total_outcome]


def home_page_data():
    categories = list()  # 产品名称
    product_pack_ls = list()  # 产品包装
    gb_production = list()
    gb_sales = list()
    gb_left = list()
    data_reset = dict()
    if Product:
        dataset = Product.objects.all().order_by('product_name')
        if dataset:
            for entry in dataset:
                if str(entry.product_name.product_name_cn) not in data_reset:
                    categories.append('%s' % entry.product_name.product_name_cn)
                    if entry.product_pack_sum:
                        data_reset[entry.product_name.product_name_cn] = {
                            str(entry.product_pack.pk): [entry.product_pack_sum, int(entry.product_sale_sum),
                                                         int(entry.product_left_sum)]}
                else:
                    if entry.product_pack_sum:
                        data_reset[entry.product_name.product_name_cn][str(entry.product_pack.pk)] = \
                            [entry.product_pack_sum, int(entry.product_sale_sum), int(entry.product_left_sum)]
                if str(entry.product_pack.pk) not in product_pack_ls:
                    product_pack_ls.append('%s' % entry.product_pack.pk)
            for ppl in product_pack_ls:  # pack list
                product_packs_name = ProductPackSizeUnit.objects.get(pk=ppl).product_pack_size_unit_cn
                amount_by_categories_p = list()
                amount_by_categories_s = list()
                amount_by_categories_l = list()
                for category in categories:
                    if category in data_reset:
                        if ppl in data_reset[category]:
                            amount_by_categories_p.append(data_reset[category][ppl][0])
                            amount_by_categories_s.append(data_reset[category][ppl][1])
                            amount_by_categories_l.append(data_reset[category][ppl][2])
                        else:
                            amount_by_categories_p.append(0)
                            amount_by_categories_s.append(0)
                            amount_by_categories_l.append(0)
                    else:
                        categories.remove(category)
                gb_production.append({'name': product_packs_name, 'data': amount_by_categories_p})
                gb_sales.append({'name': product_packs_name, 'data': amount_by_categories_s})
                gb_left.append({'name': product_packs_name, 'data': amount_by_categories_l})
    return {'categories': categories, 'gb_production': gb_production, 'gb_sales': gb_sales, 'gb_left': gb_left}


# def update_money_io_date():
#     ms = MoneyInOut.objects.filter(money_in_out_date=None)
#     for m in ms:
#         m.money_in_out_date = str(m.datetime_created)[:10]
#         m.save()


@login_required
@permission_required('{0}.view_fermentmonitor'.format(app_name))
def ferment_monitor_list(request):
    template_name = '{0}/fermentmonitor/ferment_monitor_list.html'.format(app_name)
    context = table_create(request, FermentMonitor, order_by='-id')
    return render(request, template_name=template_name, context=context)


@login_required
@permission_required('{0}.view_tank'.format(app_name))
def tank_list(request):
    template_name = '{0}/tank/tank_list.html'.format(app_name)
    context = table_create(request, Tank)
    return render(request, template_name=template_name, context=context)


@login_required
@permission_required('{0}.view_tank'.format(app_name))
def tanks_overview(request):
    template_name = '{0}/tank/tanks_overview.html'.format(app_name)
    data = dict()
    tank_states = TankState.objects.all()
    for tank_state in tank_states:
        if tank_state.with_product:
            data[tank_state] = Tank.objects.filter(tank_state_id=tank_state.id).order_by('-current_brew_code')
    return render(request, template_name=template_name, context={'data': data})


@login_required
@permission_required('{0}.view_product'.format(app_name))
def home_overview(request):
    # update_money_io_date()  # TODO Need to remove after update success
    template_name = '{0}/home/overview.html'.format(app_name)
    hpd = home_page_data()
    total_brews = Brew.objects.all()
    if total_brews:
        total_brews = total_brews.count()
    else:
        total_brews = 0
    product_name_l = ProductName.objects.all()
    product_name_p = list()
    for p_n in product_name_l:
        product_name_p.append(
            [p_n.product_name_cn, Brew.objects.filter(product_name_id=p_n.pk).count()])
    last_12_sales = Sale.objects.all()
    if last_12_sales:
        if last_12_sales.count() > 13:
            last_12_sales = last_12_sales[:13]
    context = dict()
    context['total_sale_income'] = 0
    sales_mio = MoneyInOut.objects.filter(
        money_in_out_type__is_auto=True).filter(
        money_in_out_type__is_negative=False).aggregate(total_sale_income=Sum('money_in_out'))
    if sales_mio:
        if sales_mio['total_sale_income']:
            context['total_sale_income'] = sales_mio['total_sale_income']
    context['client_num'] = Client.objects.all().count()
    context['product_name_num'] = product_name_l.count()
    context['brew_num'] = total_brews
    context['total_income'] = io_per_month_column()[4]
    context['total_outcome'] = io_per_month_column()[5]
    context['product_name_p'] = json.dumps(product_name_p)
    context['categories'] = json.dumps(hpd['categories'])
    context['gb_production'] = json.dumps(hpd['gb_production'])
    context['gb_sales'] = json.dumps(hpd['gb_sales'])
    context['gb_left'] = json.dumps(hpd['gb_left'])
    context['in_out_month'] = json.dumps(io_per_month_column()[0])
    context['income_info'] = json.dumps(io_per_month_column()[1])
    context['outcome_info'] = json.dumps(io_per_month_column()[2])
    context['io_come_info'] = json.dumps(io_per_month_column()[3])
    context['income_by_products'] = json.dumps(income_by_products_pie())
    context['outcome_by_types'] = json.dumps(outcome_by_types_pie())
    context['last_12_sales'] = last_12_sales
    return render(request, template_name=template_name, context=context)


@login_required
@permission_required('{0}.view_employee'.format(app_name))
def employee_list(request):
    template_name = '{0}/employee/employee_list.html'.format(app_name)
    context = table_create(request, Employee)
    return render(request, template_name=template_name, context=context)


@login_required
@permission_required('{0}.view_client'.format(app_name))
def client_list(request):
    template_name = '{0}/client/client_list.html'.format(app_name)
    object_list = Client.objects.all()
    if request.user:
        linked_employee = Employee.objects.filter(linked_account=request.user.id)
        if linked_employee.exists():
            object_list = object_list.filter(created_by=request.user.id)
    return render(request, template_name=template_name, context=object_paginator(request, object_list))


@login_required
@permission_required('{0}.view_supplier'.format(app_name))
def supplier_list(request):
    template_name = '{0}/supplier/supplier_list.html'.format(app_name)
    context = table_create(request, Supplier)
    return render(request, template_name=template_name, context=context)


@login_required
@permission_required('{0}.view_company'.format(app_name))
def company_list(request):
    template_name = '{0}/company/company_list.html'.format(app_name)
    context = table_create(request, Company)
    return render(request, template_name=template_name, context=context)


@login_required
@permission_required('{0}.view_productname'.format(app_name))
def product_name_list(request):
    template_name = '{0}/productname/productname_list.html'.format(app_name)
    context = table_create(request, ProductName)
    return render(request, template_name=template_name, context=context)


@login_required
@permission_required('{0}.view_productcategory'.format(app_name))
def product_category_list(request):
    template_name = '{0}/productcategory/productcategory_list.html'.format(app_name)
    context = table_create(request, ProductCategory)
    return render(request, template_name=template_name, context=context)


@login_required
@permission_required('{0}.view_productpacksizeunit'.format(app_name))
def product_pack_list(request):
    template_name = '{0}/productpacksizeunit/productpacksizeunit_list.html'.format(app_name)
    context = table_create(request, ProductPackSizeUnit)
    return render(request, template_name=template_name, context=context)


@login_required
@permission_required('{0}.view_product'.format(app_name))
def product_list(request):
    template_name = '{0}/product/product_list.html'.format(app_name)
    context = table_create(request, Product, order_by='index')
    return render(request, template_name=template_name, context=context)


@login_required
@permission_required('{0}.view_product'.format(app_name))
def product_inventory(request):
    template_name = '{0}/product/product_inventory.html'.format(app_name)
    if Pack.objects.count() > 0:
        object_list_1 = Product.objects.all().order_by('index')
        object_list_2 = Pack.objects.filter(state=True).order_by('pack_date')
    else:
        object_list_1 = None
        object_list_2 = None
    content = {'t1': object_list_1,
               't2': object_list_2}
    return render(request, template_name=template_name, context=content)


@login_required
@permission_required('{0}.view_brew'.format(app_name))
def brew_list(request):
    template_name = '{0}/brew/brew_list.html'.format(app_name)
    s = request.GET.get('s')
    e = request.GET.get('e')
    q = request.GET.get('q')
    object_list = Brew.objects.all()
    if validate_date(s):
        object_list = object_list.filter(date_start__gte=validate_date(s))
    if validate_date(e):
        object_list = object_list.filter(date_start__lte=validate_date(e))
    if q:
        object_list = object_list.filter(
            Q(brew_batch_code__icontains=q) | Q(notes__icontains=q) | Q(
                product_name__product_name_cn__icontains=q) | Q(
                product_name__product_name_en__icontains=q) | Q(
                product_name__product_name_code__icontains=q)).distinct()
    object_p_data = object_paginator(request, object_list)
    context = dict()
    context['data'] = object_p_data['data']
    context['page_range'] = object_p_data['page_range']
    return render(request, template_name=template_name, context=context)


@login_required
@permission_required('{0}.view_pack'.format(app_name))
def pack_list(request):
    template_name = '{0}/pack/pack_list.html'.format(app_name)
    s = request.GET.get('s')
    e = request.GET.get('e')
    q = request.GET.get('q')
    error_msg = ''
    pie_data = list()
    column_data_category = list()
    column_data_series = list()
    object_list = Pack.objects.all()
    if validate_date(s):
        object_list = object_list.filter(pack_date__gte=validate_date(s))
    if validate_date(e):
        object_list = object_list.filter(pack_date__lte=validate_date(e))
    if q:
        object_list = object_list.filter(
            Q(pack_batch_code__icontains=q) | Q(notes__icontains=q) | Q(
                product__product_name__product_name_cn__icontains=q) | Q(
                product__product_name__product_name_en__icontains=q) | Q(
                product__product_name__product_name_code__icontains=q)).distinct()
    if object_list:
        ps = Product.objects.all()
        pns = ProductName.objects.all()
        pps = ProductPackSizeUnit.objects.all()
        pack_sum_a = object_list.aggregate(pack_sum=Sum('pack_num'))
        if pack_sum_a and ps:
            if pack_sum_a['pack_sum']:
                for p in ps:
                    pack_sum_p = object_list.filter(product_id=p.pk).aggregate(pack_sum=Sum('pack_num'))
                    if pack_sum_p['pack_sum']:
                        pie_data.append({'name': '{0} ({1})'.format(p.product_name.product_name_cn,
                                                                    p.product_pack.product_pack_size_unit_cn),
                                        'y': round(pack_sum_p['pack_sum']/pack_sum_a['pack_sum']*100, 2)})
                for pn in pns:
                    column_data_category.append(pn.product_name_cn)
                for pp in pps:
                    pack_data = list()
                    for pn in pns:
                        pack_sum_pp = object_list.filter(
                            product__product_name_id=pn.pk).filter(
                            product__product_pack_id=pp.pk).aggregate(pack_sum=Sum('pack_num'))
                        if pack_sum_pp:
                            if pack_sum_pp['pack_sum']:
                                pack_data.append(pack_sum_pp['pack_sum'])
                            else:
                                pack_data.append(0)
                    column_data_series.append({'name': pp.product_pack_size_unit_cn,
                                               'data': pack_data})
    object_p_data = object_paginator(request, object_list, per_page_count=10)
    context = dict()
    context['data'] = object_p_data['data']
    context['page_range'] = object_p_data['page_range']
    context['error_msg'] = error_msg
    context['pie_data'] = json.dumps(pie_data)
    context['column_data_c'] = json.dumps(column_data_category)
    context['column_data_s'] = json.dumps(column_data_series)
    return render(request, template_name=template_name, context=context)


@login_required
@permission_required('{0}.view_saleorder'.format(app_name))
def sale_order_list(request):
    template_name = '{0}/saleorder/sale_order_list.html'.format(app_name)
    c = request.GET.get('c')
    d = request.GET.get('d')
    s = request.GET.get('s')
    e = request.GET.get('e')
    q = request.GET.get('q')
    context = dict()
    object_list = SaleOrder.objects.all()
    if request.user:
        linked_employee = Employee.objects.filter(linked_account=request.user.id)
        if linked_employee.exists():
            object_list = object_list.filter(employee=linked_employee.first())
    context['order_num_all'] = object_list.count()
    if c:
        if c == '1':
            object_list = object_list.filter(is_delivered=False).order_by('pk')
        elif c == '2':
            object_list = object_list.filter(is_delivered=True).order_by('-pk')
    if d:
        if d == '1':
            object_list = object_list.filter(fee_received=False)
        elif d == '2':
            object_list = object_list.filter(fee_received=True)
    if validate_date(s):
        object_list = object_list.filter(sale_order_date__gte=validate_date(s))
    if validate_date(e):
        object_list = object_list.filter(sale_order_date__lte=validate_date(e))
    if q:
        object_list = object_list.filter(Q(
            sale_order_code__icontains=q) | Q(
            client__name__icontains=q) | Q(
            client__mobile__icontains=q) | Q(
            client__client_company__company_name_cn__icontains=q) | Q(
            client__client_company__company_name_en__icontains=q) | Q(
            client__client_company__company_address__icontains=q) | Q(
            notes__icontains=q)).distinct()
    object_p_data = object_paginator(request, object_list, per_page_count=20)
    context['data'] = object_p_data['data']
    context['page_range'] = object_p_data['page_range']
    return render(request, template_name=template_name, context=context)


@login_required
@permission_required('{0}.view_saleorder'.format(app_name))
def sale_order_list_wx(request):
    template_name = '{0}/saleorder/sale_order_list_wx.html'.format(app_name)
    c = request.GET.get('c')
    d = request.GET.get('d')
    s = request.GET.get('s')
    e = request.GET.get('e')
    q = request.GET.get('q')
    context = dict()
    object_list = SaleOrder.objects.filter(is_from_wx=True)
    context['order_num_all'] = object_list.count()
    if c:
        object_list = object_list.filter(order_state_id=c).order_by('pk')
    if d:
        if d == '1':
            object_list = object_list.filter(fee_received=False)
        elif d == '2':
            object_list = object_list.filter(fee_received=True)
    if validate_date(s):
        object_list = object_list.filter(sale_order_date__gte=validate_date(s))
    if validate_date(e):
        object_list = object_list.filter(sale_order_date__lte=validate_date(e))
    if q:
        object_list = object_list.filter(Q(
            sale_order_code__icontains=q) | Q(
            client__name__icontains=q) | Q(
            client__mobile__icontains=q) | Q(
            client__client_company__company_name_cn__icontains=q) | Q(
            client__client_company__company_name_en__icontains=q) | Q(
            client__client_company__company_address__icontains=q) | Q(
            notes__icontains=q)).distinct()
    object_p_data = object_paginator(request, object_list, per_page_count=20)
    context['data'] = object_p_data['data']
    context['page_range'] = object_p_data['page_range']
    context['order_states'] = list()
    order_states = OrderState.objects.all()
    for o_s in order_states:
        context['order_states'].append({'state': o_s,
                                        'state_count': object_list.filter(order_state_id=o_s.pk).count()},)
    context['order_num'] = object_list.count()
    return render(request, template_name=template_name, context=context)


@login_required
@permission_required('{0}.view_sale'.format(app_name))
def sale_list(request):
    template_name = '{0}/sale/sale_list.html'.format(app_name)
    c = request.GET.get('c')
    d = request.GET.get('d')
    s = request.GET.get('s')
    e = request.GET.get('e')
    q = request.GET.get('q')
    error_msg = ''
    context = dict()
    pie_data = list()
    column_data_category = list()
    column_data_series = list()
    if c:
        if c == '1':
            object_list = Sale.objects.filter(is_confirmed=False).order_by('pk')
        elif c == '2':
            object_list = Sale.objects.filter(is_confirmed=True).order_by('-pk')
        else:
            object_list = Sale.objects.all()
    else:
        object_list = Sale.objects.all()
    if request.user:
        linked_employee = Employee.objects.filter(linked_account=request.user.id)
        if linked_employee.exists():
            object_list = object_list.filter(sale_order__employee=linked_employee.first())
    if d:
        if d == '1':
            object_list = object_list.filter(fee_received=False).order_by('-pk')
        elif d == '2':
            object_list = object_list.filter(fee_received=True).order_by('-pk')
    if validate_date(s):
        object_list = object_list.filter(sale_date__gte=validate_date(s))
    if validate_date(e):
        object_list = object_list.filter(sale_date__lte=validate_date(e))
    if q:
        object_list = object_list.filter(
            Q(sale_order__sale_order_code__icontains=q) | Q(notes__icontains=q) | Q(
                pack__product__product_name__product_name_cn__icontains=q) | Q(
                pack__product__product_name__product_name_en__icontains=q) | Q(
                pack__product__product_name__product_name_code__icontains=q)).distinct()
    object_p_data = object_paginator(request, object_list, per_page_count=20)
    context['data'] = object_p_data['data']
    context['page_range'] = object_p_data['page_range']
    if object_list:
        object_list = object_list.filter(is_active=True)
        ps = Product.objects.all()
        pns = ProductName.objects.all()
        pps = ProductPackSizeUnit.objects.all()
        if ps:
            for p in ps:
                sale_sum_p = object_list.filter(pack__product_id=p.pk).aggregate(sale_sum=Sum('sale_num'))
                if sale_sum_p['sale_sum']:
                    pie_data.append({'name': '{0} ({1})'.format(p.product_name.product_name_cn,
                                                                p.product_pack.product_pack_size_unit_cn),
                                    'y': sale_sum_p['sale_sum']})
            for pn in pns:
                column_data_category.append(pn.product_name_cn)
            for pp in pps:
                pack_data = list()
                for pn in pns:
                    sale_sum_pp = object_list.filter(
                        pack__product__product_name_id=pn.pk).filter(
                        pack__product__product_pack_id=pp.pk).aggregate(sale_sum=Sum('sale_num'))
                    if sale_sum_pp:
                        if sale_sum_pp['sale_sum']:
                            pack_data.append(sale_sum_pp['sale_sum'])
                        else:
                            pack_data.append(0)
                column_data_series.append({'name': pp.product_pack_size_unit_cn,
                                           'data': pack_data})
        context['error_msg'] = error_msg
        context['pie_data'] = json.dumps(pie_data)
        context['column_data_c'] = json.dumps(column_data_category)
        context['column_data_s'] = json.dumps(column_data_series)
    return render(request, template_name=template_name, context=context)


@login_required
@permission_required('{0}.view_moneyinout'.format(app_name))
def moneyinout_list(request):
    template_name = '{0}/moneyinout/moneyinout_list.html'.format(app_name)
    context = dict()
    s = request.GET.get('s')
    e = request.GET.get('e')
    c = request.GET.get('c')
    d = request.GET.get('d')
    q = request.GET.get('q')
    object_list = MoneyInOut.objects.all()
    sale_incomes = Sale.objects.exclude(sale_price_link__isnull=True).filter(is_active=True).filter(fee_received=True)
    if c:
        object_list = object_list.filter(money_in_out_type_id=c)
    if d:
        if d == '1':
            object_list = object_list.filter(is_confirmed=False).order_by('-pk')
        elif d == '2':
            object_list = object_list.filter(is_confirmed=True).order_by('-pk')
    if validate_date(s):
        object_list = object_list.filter(money_in_out_date__gte=validate_date(s))
        sale_incomes = sale_incomes.filter(sale_price_link__money_in_out_date__gte=validate_date(s))
    if validate_date(e):
        object_list = object_list.filter(money_in_out_date__lte=validate_date(e))
        sale_incomes = sale_incomes.filter(sale_price_link__money_in_out_date__lte=validate_date(e))
    if q:
        object_list = object_list.filter(Q(notes__icontains=q)).distinct()
    object_p_data = object_paginator(request, object_list, per_page_count=10)
    context['data'] = object_p_data['data']
    context['page_range'] = object_p_data['page_range']
    context['money_io_t'] = MoneyInOutType.objects.all()
    context['in_out_month'] = json.dumps(io_per_month_column()[0])
    context['income_info'] = json.dumps(io_per_month_column()[1])
    context['outcome_info'] = json.dumps(io_per_month_column()[2])
    context['io_come_info'] = json.dumps(io_per_month_column()[3])
    context['income_by_products'] = json.dumps(income_by_products_pie(sale_incomes))
    context['outcome_by_types'] = json.dumps(outcome_by_types_pie(
        object_list.filter(is_confirmed=True).filter(is_active=True)))
    return render(request, template_name=template_name, context=context)


@login_required
@permission_required('{0}.view_material'.format(app_name))
def material_list(request):
    template_name = '{0}/material/material_list.html'.format(app_name)
    context = dict()
    c = request.GET.get('c')
    q = request.GET.get('q')
    object_list = Material.objects.all()
    if c:
        object_list = object_list.filter(material_category_id=c)
    if q:
        object_list = object_list.filter(Q(notes__icontains=q) | Q(material_en__icontains=q) | Q(
            material_cn__icontains=q) | Q(material_code__icontains=q)).distinct()
    object_p_data = object_paginator(request, object_list)
    context['data'] = object_p_data['data']
    context['page_range'] = object_p_data['page_range']
    context['material_category'] = MaterialCategory.objects.all()
    return render(request, template_name=template_name, context=context)


@login_required
@permission_required('{0}.view_materialbatch'.format(app_name))
def material_batch_list(request):
    template_name = '{0}/materialbatch/material_batch_list.html'.format(app_name)
    context = dict()
    s = request.GET.get('s')
    e = request.GET.get('e')
    c = request.GET.get('c')
    q = request.GET.get('q')
    object_list = MaterialBatch.objects.all()
    if c:
        object_list = object_list.filter(material__material_category_id=c)
    if validate_date(s):
        object_list = object_list.filter(expire_date__gte=validate_date(s))
    if validate_date(e):
        object_list = object_list.filter(expire_date__lte=validate_date(e))
    if q:
        object_list = object_list.filter(Q(notes__icontains=q) | Q(material__material_en__icontains=q) | Q(
            material__material_cn__icontains=q) | Q(material__material_code__icontains=q) | Q(
            material_batch_code__icontains=q)).distinct()
    object_p_data = object_paginator(request, object_list)
    context['data'] = object_p_data['data']
    context['page_range'] = object_p_data['page_range']
    context['material_category'] = MaterialCategory.objects.all()
    return render(request, template_name=template_name, context=context)


@login_required
@permission_required('{0}.view_materialin'.format(app_name))
def material_in_list(request):
    template_name = '{0}/materialin/material_in_list.html'.format(app_name)
    context = dict()
    s = request.GET.get('s')
    e = request.GET.get('e')
    c = request.GET.get('c')
    d = request.GET.get('d')
    q = request.GET.get('q')
    object_list = MaterialIn.objects.all()
    if c:
        object_list = object_list.filter(material_batch__material__material_category_id=c)
    if d:
        if d == '1':
            object_list = object_list.filter(is_confirmed=True)
        elif d == '2':
            object_list = object_list.filter(is_confirmed=False)
    if validate_date(s):
        object_list = object_list.filter(material_in_date__gte=validate_date(s))
    if validate_date(e):
        object_list = object_list.filter(material_in_date__lte=validate_date(e))
    if q:
        object_list = object_list.filter(Q(notes__icontains=q) | Q(
            material_batch__material_batch_code__icontains=q) | Q(
            material_batch__material__material_en__icontains=q) | Q(
            material_batch__material__material_cn__icontains=q) | Q(
            material_batch__material__material_code__icontains=q)).distinct()
    object_p_data = object_paginator(request, object_list)
    context['data'] = object_p_data['data']
    context['page_range'] = object_p_data['page_range']
    context['material_category'] = MaterialCategory.objects.all()
    return render(request, template_name=template_name, context=context)


@login_required
@permission_required('{0}.view_materialout'.format(app_name))
def material_out_list(request):
    template_name = '{0}/materialout/material_out_list.html'.format(app_name)
    context = dict()
    s = request.GET.get('s')
    e = request.GET.get('e')
    c = request.GET.get('c')
    q = request.GET.get('q')
    object_list = MaterialOut.objects.all()
    if c:
        object_list = object_list.filter(material_batch__material__material_category_id=c)
    if validate_date(s):
        object_list = object_list.filter(material_out_date__gte=validate_date(s))
    if validate_date(e):
        object_list = object_list.filter(material_out_date__lte=validate_date(e))
    if q:
        object_list = object_list.filter(Q(notes__icontains=q) | Q(
            material_batch__material_batch_code__icontains=q) | Q(
            material_batch__material__material_en__icontains=q) | Q(
            material_batch__material__material_cn__icontains=q) | Q(
            material_batch__material__material_code__icontains=q)).distinct()
    object_p_data = object_paginator(request, object_list)
    context['data'] = object_p_data['data']
    context['page_range'] = object_p_data['page_range']
    context['material_category'] = MaterialCategory.objects.all()
    return render(request, template_name=template_name, context=context)


# def update_temp(t_d=0.2):
#     jkm_t_s = JkmT()
#     data = jkm_t_s.return_data(t_d=t_d)
#     for key, value in data.items():
#         tank = Tank.objects.get(tank_code=key)
#         if tank.tank_state:
#             if int(tank.tank_state.pk) <= 4 and tank.current_brew_code:
#                 brew = Brew.objects.get(brew_batch_code=tank.current_brew_code)
#                 if brew:
#                     obj1 = FermentMonitor(brew_id=brew.pk, t_real=value['TREAL'],
#                                           t_set=value['TSET'], recorded=timezone.now())
#                     obj1.save()
#             tank.jkm_t_real = value['TREAL']
#             tank.jkm_t_set = value['TSET']
#             tank.jkm_updated = timezone.now()
#             tank.save()
#     return HttpResponse(content=data)


@login_required
@permission_required('{0}.view_product'.format(app_name))
def handbook(request):
    template_name = '{0}/handbook/handbook.html'.format(app_name)
    object_list = HandBook.objects.all()
    return render(request, template_name=template_name, context={'data': object_list})


@login_required
@permission_required('{0}.add_employee'.format(app_name))
def user_action_list(request):
    template_name = '{0}/user/action_list.html'.format(app_name)
    context = dict()
    s = request.GET.get('s')
    e = request.GET.get('e')
    q = request.GET.get('q')
    object_list = LogEntry.objects.filter(content_type__app_label=app_name)
    if validate_date(s):
        object_list = object_list.filter(action_time__gte=validate_date(s))
    if validate_date(e):
        object_list = object_list.filter(action_time__lte=validate_date(e))
    if q:
        object_list = object_list.filter(
            Q(object_repr__icontains=q) | Q(action_flag__icontains=q) | Q(
                change_message__icontains=q)).distinct()
    object_p_data = object_paginator(request, object_list)
    context['data'] = object_p_data['data']
    context['page_range'] = object_p_data['page_range']
    return render(request, template_name=template_name, context=context)
