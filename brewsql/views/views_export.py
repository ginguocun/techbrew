from django.http import HttpResponse
from xlwt import *
# import os
from io import BytesIO
from django.contrib.auth.decorators import login_required, permission_required
from django.views.decorators.http import require_http_methods
from ..apps import GeneralConfig
from ..models import Brew, Pack, Sale
from ..utils import validate_date


app_name = GeneralConfig.name


def excel_export(request, file_name='test', model=None, list_obj=None, head=None, fields=None):
    if not request.user.is_authenticated:
        return HttpResponse(u'请登录！')
    if list_obj is None and model:
        list_obj = model.objects.all()
    if list_obj:
        ws = Workbook(encoding='utf-8')
        w = ws.add_sheet(file_name)
        excel_row = 0
        k = 0
        if head:
            for h in head:
                w.write(excel_row, k, h)
                k += 1
        excel_row = 1
        k = 0
        for obj in list_obj:
            if fields:
                for d in fields:
                    w.write(excel_row, k, '{0}'.format(getattr(obj, d)),)
                    k += 1
            excel_row += 1
            k = 0
        bio = BytesIO()
        ws.save(bio)
        bio.seek(0)
        response = HttpResponse(bio.getvalue(), content_type='application/vnd.ms-excel')
        response['Content-Disposition'] = 'attachment; filename={0}.xls'.format(file_name)
        response.write(bio.getvalue())
        return response
    return HttpResponse('没有数据')


@login_required
@permission_required('{0}.can_export_brew_data'.format(app_name))
@require_http_methods(["GET"])
def brew_export(request):
    s = request.GET.get('s')
    e = request.GET.get('e')
    model = Brew
    list_obj = None
    if validate_date(s):
        list_obj = model.objects.filter(date_start__gte=validate_date(s))
        if validate_date(e):
            list_obj = list_obj.filter(date_start__lte=validate_date(e))
    head = ['id', u'产品名称ID', u'产品名称', u'设备ID', u'设备', u'日期', u'操作人员ID', u'操作人员', u'备注', u'创建时间',
            u'最后更新']
    fields = ['pk', 'product_name_id', 'product_name', 'tank_id', 'tank', 'date_start', 'operator_id', 'operator',
              'notes', 'datetime_created', 'datetime_updated']
    return excel_export(request, file_name='brew', model=model, list_obj=list_obj, head=head, fields=fields)


@login_required
@permission_required('{0}.can_export_pack_data'.format(app_name))
@require_http_methods(["GET"])
def pack_export(request):
    s = request.GET.get('s')
    e = request.GET.get('e')
    model = Pack
    list_obj = None
    if validate_date(s):
        list_obj = Pack.objects.filter(pack_date__gte=validate_date(s))
        if validate_date(e):
            list_obj = list_obj.filter(pack_date__lte=validate_date(e))
    head = ['id', u'灌装日期', u'灌装批次', u'生产批次ID', u'生产批次', u'产品ID', u'产品', u'数量',
            u'灌装开始', u'灌装结束', u'备注', u'创建时间', u'最后更新']
    fields = ['pk', 'pack_date', 'pack_batch_code', 'brew_id', 'brew', 'product_id', 'product', 'pack_num',
              'pack_start', 'pack_end', 'notes', 'datetime_created', 'datetime_updated']
    return excel_export(request, file_name='pack', model=model, list_obj=list_obj, head=head, fields=fields)


@login_required
@permission_required('{0}.can_export_sale_data'.format(app_name))
@require_http_methods(["GET"])
def sale_export(request):
    s = request.GET.get('s')
    e = request.GET.get('e')
    model = Sale
    list_obj = None
    if validate_date(s):
        list_obj = Sale.objects.filter(sale_date__gte=validate_date(s))
        if validate_date(e):
            list_obj = list_obj.filter(sale_date__lte=validate_date(e))
    head = ['id', u'销售日期', u'销售单号ID', u'销售单号', u'灌装批次ID', u'灌装批次', u'数量', u'销售价格ID', u'销售价格',
            u'备注', u'正常出售', u'是否有效', u'是否确认', u'创建时间', u'最后更新']
    fields = ['pk', 'sale_date', 'sale_order_id', 'sale_order', 'pack_id', 'pack', 'sale_num', 'sale_price_link_id',
              'sale_price', 'notes', 'is_sale', 'is_active', 'is_confirmed', 'datetime_created', 'datetime_updated']
    return excel_export(request, file_name='sale', model=model, list_obj=list_obj, head=head, fields=fields)