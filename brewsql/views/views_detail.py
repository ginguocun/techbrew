from django.contrib.auth.decorators import login_required, permission_required
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
from django.shortcuts import get_object_or_404, render

from ..utils import convert_num_to_chinese
from ..forms import *


app_name = GeneralConfig.name


@login_required
@permission_required('{0}.view_client'.format(app_name))
def client_detail(request, pk):
    client = get_object_or_404(Client, pk=pk)
    if not request.user.has_perm('{0}.view_all_clients'.format(app_name)):
        linked_employee = Employee.objects.filter(linked_account=request.user.pk)
        if linked_employee.exists() and client:
            if not client.created_by == request.user:
                return HttpResponseNotFound()
    order_list = Sale.objects.filter(sale_order__client_id=client.pk)
    order_pr = None
    if order_list:
        paginator = Paginator(order_list, 10)
        page = request.GET.get('page', 1)
        order_pr = paginator.get_page(page)
    total_income = order_list.aggregate(total_income=Sum('sale_price_link__money_in_out'))
    total_income_cn = ''
    if total_income['total_income']:
        total_income = total_income['total_income']
        total_income_cn = convert_num_to_chinese(float(total_income))
    else:
        total_income = 0
    context = dict()
    context['client_data'] = client
    context['page_obj'] = order_pr
    context['total_income'] = total_income
    context['total_income_cn'] = total_income_cn
    return render(request, '{0}/client/client_detail.html'.format(app_name), context=context)


@login_required
@permission_required('{0}.view_supplier'.format(app_name))
def supplier_detail(request, pk):
    supplier = get_object_or_404(Supplier, pk=pk)
    order_list = MaterialIn.objects.filter(supplier_id=supplier.pk)
    order_pr = None
    if order_list:
        paginator = Paginator(order_list, 10)
        page = request.GET.get('page', 1)
        order_pr = paginator.get_page(page)
    total_cost = order_list.aggregate(total_cost=Sum('material_cost_link__money_in_out'))
    total_cost_cn = ''
    if total_cost['total_cost']:
        total_cost = - total_cost['total_cost']
        if total_cost:
            total_cost_cn = convert_num_to_chinese(float(total_cost))
        else:
            total_cost_cn = None
    else:
        total_cost = 0
    context = dict()
    context['supplier_data'] = supplier
    context['page_obj'] = order_pr
    context['total_cost'] = total_cost
    context['total_cost_cn'] = total_cost_cn
    return render(request, '{0}/supplier/supplier_detail.html'.format(app_name), context=context)


def brew_ferment_m(ferment_ms=None):
    plato_data = list()
    ph_data = list()
    t_real = list()
    t_set = list()
    if ferment_ms:
        for ferment_m in ferment_ms:
            c_time_string = ferment_m.recorded
            c_year = str(c_time_string)[0:4]
            c_month = int(str(c_time_string)[5:7]) - 1
            c_day = str(c_time_string)[8:10]
            c_hour = str(c_time_string)[11:13]
            c_min = str(c_time_string)[14:16]
            if ferment_m.plato:
                plato_data.append({'year': c_year, 'month': c_month, 'day': c_day,
                                   'hour': c_hour, 'min': c_min, 'data': str(ferment_m.plato)})
            if ferment_m.ph:
                ph_data.append({'year': c_year, 'month': c_month, 'day': c_day,
                                'hour': c_hour, 'min': c_min, 'data': str(ferment_m.ph)})
            if ferment_m.t_real:
                t_real.append({'year': c_year, 'month': c_month, 'day': c_day,
                               'hour': c_hour, 'min': c_min, 'data': str(ferment_m.t_real)})
            if ferment_m.t_set:
                t_set.append({'year': c_year, 'month': c_month, 'day': c_day,
                              'hour': c_hour, 'min': c_min, 'data': str(ferment_m.t_set)})
    return plato_data, ph_data, t_real, t_set


def brew_data(request, pk=1):
    brew = get_object_or_404(Brew, pk=pk)
    ferment_ms = FermentMonitor.objects.filter(brew_id=brew.pk).order_by('recorded')
    paginator = Paginator(ferment_ms, 20)
    page = request.GET.get('page', 1)
    [plato_data, ph_data, t_real, t_set] = brew_ferment_m(ferment_ms)
    context = dict()
    context['brew'] = brew
    context['plato_data'] = plato_data
    context['ph_data'] = ph_data
    context['t_real'] = t_real
    context['t_set'] = t_set
    context['page_obj'] = paginator.get_page(page)
    context['brew_monitors'] = BrewMonitor.objects.filter(brew=brew)
    context['packs'] = Pack.objects.filter(brew=brew)
    context['sales'] = Sale.objects.filter(pack__brew=brew)
    context['materials'] = MaterialOut.objects.filter(brew=brew)
    return context


@login_required
@permission_required('{0}.view_brew'.format(app_name))
def brew_detail(request, pk):
    template_name = '{0}/brew/brew_detail.html'.format(app_name)
    context = brew_data(request, pk=pk)
    return render(request, template_name=template_name, context=context)


def brew_detail_public(request, pk, brew_key):
    template_name = '{0}/brew/brew_detail_public.html'.format(app_name)
    brew = get_object_or_404(Brew, pk=pk)
    if brew:
        if brew.brew_key == brew_key:
            context = brew_data(request, pk=pk)
            return render(request, template_name=template_name, context=context)
    return HttpResponseNotFound()


@login_required
@permission_required('{0}.view_materialbatch'.format(app_name))
def material_batch_detail(request, pk):
    material_batch = get_object_or_404(MaterialBatch, pk=pk)
    material_in = MaterialIn.objects.filter(material_batch_id=material_batch.pk)
    material_out = MaterialOut.objects.filter(material_batch_id=material_batch.pk)
    if material_in.exists():
        material_in = material_in[:50]
    if material_out.exists():
        material_out = material_out[:50]
    total_cost = material_in.aggregate(total_cost=Sum('material_cost_link__money_in_out'))
    total_cost_cn = ''
    if total_cost:
        if total_cost['total_cost']:
            total_cost = - total_cost['total_cost']
            total_cost_cn = convert_num_to_chinese(float(total_cost))
    else:
        total_cost = 0
    context = dict()
    context['data'] = material_batch
    context['material_in'] = material_in
    context['material_in_amount'] = material_in.aggregate(material_in_amount=Sum('amount'))
    context['material_out_amount'] = material_out.aggregate(material_out_amount=Sum('amount'))
    context['material_out'] = material_out
    context['total_cost'] = total_cost
    context['total_cost_cn'] = total_cost_cn
    return render(request, '{0}/materialbatch/material_batch_detail.html'.format(app_name), context=context)


@login_required
@permission_required('{0}.view_saleorder'.format(app_name))
def sale_order_detail(request, pk):
    sale_order_s = SaleOrder.objects.filter(pk=pk)
    if not request.user.has_perm('{0}.view_all_sale_orders'.format(app_name)):
        sale_order_s = sale_order_s.filter(created_by=request.user)
    if sale_order_s.exists():
        selected_sale_order = sale_order_s.first()
    else:
        return HttpResponseNotFound()
    context = dict()
    context['d'] = selected_sale_order
    return render(request, '{0}/saleorder/sale_order_detail.html'.format(app_name), context=context)
