from django.http import HttpResponseRedirect
from django.views.generic.edit import UpdateView, DeleteView
from django.utils.decorators import method_decorator
from django.shortcuts import render
from django.contrib.admin.models import LogEntry, CHANGE, DELETION
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, permission_required
# from django.core.exceptions import ObjectDoesNotExist
from ..forms import *
# from tb2 import sms_aliyun


app_name = GeneralConfig.name


def get_content_type_for_model(obj):
    from django.contrib.contenttypes.models import ContentType
    return ContentType.objects.get_for_model(obj, for_concrete_model=False)


class TechBrewDeleteView(DeleteView):

    def delete(self, request, *args, **kwargs):
        oj = self.get_object()
        if oj:
            LogEntry.objects.log_action(
                user_id=self.request.user.pk,
                content_type_id=get_content_type_for_model(oj).pk,
                object_id=oj.pk,
                object_repr=str(oj),
                action_flag=DELETION,
            )
        if self.request.GET.get('next'):
            success_url = self.request.GET.get('next')
        else:
            success_url = self.get_success_url()
        oj.delete()
        return HttpResponseRedirect(success_url)


class TechBrewUpdateView(UpdateView):

    def get_success_url(self):
        if self.request.GET:
            if self.request.GET.get('next'):
                return self.request.GET.get('next')
        return super().get_success_url()

    def form_valid(self, form):
        if form.is_valid:
            model = form.save(commit=False)
            model.save()
            if model:
                LogEntry.objects.log_action(
                    user_id=self.request.user.pk,
                    content_type_id=get_content_type_for_model(model).pk,
                    object_id=model.pk,
                    object_repr=str(model),
                    action_flag=CHANGE,
                )
        return super().form_valid(form)


@login_required
@permission_required('{0}.change_tank'.format(app_name))
def tank_update(request,
                template_name='{0}/tank/tank_update.html'.format(app_name),
                ob=TankStateUpdateForm, 
                redirect='{0}:tanks_overview'.format(app_name)):
    tanks = Tank.objects.all().order_by('id')
    tank_states = TankState.objects.filter(pk__lte=5)
    if request.method == 'POST':
        form = ob(request.POST)
        if form.is_valid():
            r = request.POST
            tank_select = Tank.objects.get(id=form.data.get('tank'))
            new_data = form.cleaned_data
            new_data['tank_state_pre'] = tank_select.tank_state_id
            new_data['tank'] = r['tank']
            new_data['tank_state_now'] = r['tank_state_now']
            new_form = ob(new_data)
            new_form.save()
            # # TODO 短信发送接口
            # params = str({'name': request.user.username,
            #               'tank': Tank.objects.get(pk=r['tank']).tank_name,
            #               'state1': "[{0}]".format(
            #                   TankState.objects.get(pk=new_data['tank_state_pre']).tank_state_cn),
            #               'state2': "[{0}]".format(
            #                   TankState.objects.get(pk=new_data['tank_state_now']).tank_state_cn)})
            # rsp = sms_aliyun.tank_state_update_url(mobile=GeneralConfig.mobile, template_code="SMS_133969679",
            #                                        para=params)
            # if not rsp:
            #     pass
            Tank.objects.filter(id=form.data.get('tank')).update(tank_state_id=int(r['tank_state_now']))
        elif form.errors:
            return render(request,
                          template_name=template_name,
                          context={'form': form, 'tanks': tanks, 'tank_states': tank_states})
        return HttpResponseRedirect(reverse(redirect))
    else:
        form = ob()
    return render(request,
                  template_name=template_name,
                  context={'form': form, 'tanks': tanks, 'tank_states': tank_states})


class ClientLevelUpdate(TechBrewUpdateView):
    model = ClientLevel
    form_class = ClientLevelForm
    template_name_suffix = '/change_clientlevel'

    @method_decorator([login_required, permission_required('{0}.change_clientlevel'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class ClientUpdate(TechBrewUpdateView):
    model = Client
    form_class = ClientForm
    template_name_suffix = '/change_client'

    @method_decorator([login_required, permission_required('{0}.change_client'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(__class__, self).dispatch(request, *args, **kwargs)


class EmployeeStateUpdate(TechBrewUpdateView):
    model = EmployeeState
    form_class = EmployeeStateForm
    template_name_suffix = '/change_employee_state'

    @method_decorator([login_required, permission_required('{0}.change_employeestate'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(__class__, self).dispatch(request, *args, **kwargs)


class EmployeeUpdate(TechBrewUpdateView):
    model = Employee
    form_class = EmployeeUpdateForm
    template_name_suffix = '/change_employee'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['app_users'] = User.objects.filter(groups__permissions__content_type__app_label=app_name).distinct()
        return context

    @method_decorator([login_required, permission_required('{0}.change_employee'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(__class__, self).dispatch(request, *args, **kwargs)


class SupplierUpdate(TechBrewUpdateView):
    model = Supplier
    form_class = SupplierForm
    template_name_suffix = '/change_supplier'

    @method_decorator([login_required, permission_required('{0}.change_supplier'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(__class__, self).dispatch(request, *args, **kwargs)


class CompanyTypeUpdate(TechBrewUpdateView):
    model = CompanyType
    form_class = CompanyTypeForm
    template_name_suffix = '/change_companytype'

    @method_decorator([login_required, permission_required('{0}.change_companytype'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(__class__, self).dispatch(request, *args, **kwargs)


class CompanyUpdate(TechBrewUpdateView):
    model = Company
    form_class = CompanyForm
    template_name_suffix = '/change_company'

    @method_decorator([login_required, permission_required('{0}.change_company'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(__class__, self).dispatch(request, *args, **kwargs)


class MaterialPackUpdate(TechBrewUpdateView):
    model = MaterialPackSizeUnit
    form_class = MaterialPackSizeUnitForm
    template_name_suffix = '/change_materialpacksizeunit'
    decorators = [login_required, permission_required('{0}.change_materialpacksizeunit'.format(app_name))]

    @method_decorator(decorators)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class MaterialUpdate(TechBrewUpdateView):
    model = Material
    form_class = MaterialForm
    template_name_suffix = '/change_material'
    decorators = [login_required, permission_required('{0}.change_material'.format(app_name))]

    @method_decorator(decorators)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class MaterialBatchUpdate(TechBrewUpdateView):
    model = MaterialBatch
    form_class = MaterialBatchUpdateForm
    template_name_suffix = '/change_materialbatch'
    decorators = [login_required, permission_required('{0}.change_materialbatch'.format(app_name))]

    @method_decorator(decorators)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class WarehouseUpdate(TechBrewUpdateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name_suffix = '/change_warehouse'
    decorators = [login_required, permission_required('{0}.change_warehouse'.format(app_name))]

    @method_decorator(decorators)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class MaterialInUpdate(UpdateView):
    model = MaterialIn
    form_class = MaterialInUpdateForm
    template_name_suffix = '/change_materialin'
    decorators = [login_required, permission_required('{0}.change_materialin'.format(app_name))]

    def get_success_url(self):
        if self.request.GET:
            if self.request.GET.get('next'):
                return self.request.GET.get('next')
        return super().get_success_url()

    def form_valid(self, form):
        if form.is_valid:
            model = form.save(commit=False)
            if model.material_cost > 0:
                model.material_cost = - model.material_cost
            if model.material_cost_link_id:
                MoneyInOut.objects.filter(pk=self.object.material_cost_link_id).update(
                    money_in_out=self.object.material_cost,
                    money_in_out_date=self.object.material_in_date)
            model.save()
            if model:
                LogEntry.objects.log_action(
                    user_id=self.request.user.pk,
                    content_type_id=get_content_type_for_model(model).pk,
                    object_id=model.pk,
                    object_repr=str(model),
                    action_flag=CHANGE,
                )
        return super().form_valid(form)

    @method_decorator(decorators)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class MaterialOutUpdate(TechBrewUpdateView):
    model = MaterialOut
    form_class = MaterialOutUpdateForm
    template_name_suffix = '/change_materialout'
    decorators = [login_required, permission_required('{0}.change_materialout'.format(app_name))]

    @method_decorator(decorators)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class FermentMonitorDelete(TechBrewDeleteView):
    model = FermentMonitor
    template_name_suffix = '/fermentmonitor_confirm_delete'
    success_url = '/{0}/ferment_monitor_list/'.format(app_name)

    @method_decorator([login_required, permission_required('{0}.delete_fermentmonitor'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(__class__, self).dispatch(request, *args, **kwargs)


class MoneyInOutTypeUpdate(TechBrewUpdateView):
    model = MoneyInOutType
    form_class = MoneyInOutTypeForm
    template_name_suffix = '/change_money_inout_type'
    decorators = [login_required, permission_required('{0}.change_moneyinouttype'.format(app_name))]

    @method_decorator(decorators)
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class MoneyInOutUpdate(UpdateView):
    model = MoneyInOut
    form_class = MoneyInOutUpdateForm
    template_name_suffix = '/change_moneyinout'

    def get_success_url(self):
        if self.request.GET:
            if self.request.GET.get('next'):
                return self.request.GET.get('next')
        return super().get_success_url()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['money_in_out_types'] = MoneyInOutType.objects.filter(is_auto=False)
        return context

    def form_valid(self, form):
        if form.is_valid:
            model = form.save(commit=False)
            if model.money_in_out_type.is_negative is True:
                if model.money_in_out > 0:
                    model.money_in_out = - model.money_in_out
            else:
                if model.money_in_out < 0:
                    model.money_in_out = - model.money_in_out
            model.save()
            if model:
                LogEntry.objects.log_action(
                    user_id=self.request.user.pk,
                    content_type_id=get_content_type_for_model(model).pk,
                    object_id=model.pk,
                    object_repr=str(model),
                    action_flag=CHANGE,
                )
        return super().form_valid(form)

    @method_decorator([login_required, permission_required('{0}.change_moneyinout'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class MoneyInOutDelete(DeleteView):
    model = MoneyInOut
    success_url = '/{0}/money_io_list/'.format(app_name)
    template_name_suffix = '/delete_moneyinout'

    def get_success_url(self):
        if self.request.GET:
            if self.request.GET.get('next'):
                return self.request.GET.get('next')
        return self.success_url

    def delete(self, request, *args, **kwargs):
        oj = self.get_object()
        if oj:
            if oj.money_in_out_type:
                if oj.money_in_out_type.is_auto is False:
                    LogEntry.objects.log_action(
                        user_id=self.request.user.pk,
                        content_type_id=get_content_type_for_model(oj).pk,
                        object_id=oj.pk,
                        object_repr=str(oj),
                        action_flag=DELETION,
                    )
                    oj.delete()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

    @method_decorator([login_required, permission_required('{0}.delete_moneyinout'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class MoneyInOutStateUpdate(UpdateView):
    model = MoneyInOut
    form_class = MoneyInOutStateUpdateForm
    template_name_suffix = '/change_moneyinout_state'

    def get_success_url(self):
        if self.request.GET:
            if self.request.GET.get('next'):
                print(self.request.GET.get('next'))
                return self.request.GET.get('next')
        return super().get_success_url()

    def form_valid(self, form):
        if form.is_valid:
            model = form.save(commit=False)
            if model.money_in_out_type.is_negative is True:
                if model.money_in_out > 0:
                    model.money_in_out = - model.money_in_out
            else:
                if model.money_in_out < 0:
                    model.money_in_out = - model.money_in_out
            model.save()
            if model:
                LogEntry.objects.log_action(
                    user_id=self.request.user.pk,
                    content_type_id=get_content_type_for_model(model).pk,
                    object_id=model.pk,
                    object_repr=str(model),
                    action_flag=CHANGE,
                )
        return super().form_valid(form)

    @method_decorator([login_required, permission_required('{0}.change_moneyinout'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


@login_required
@permission_required('{0}.confirm_moneyinout'.format(app_name))
def confirm_moneyinout(request):
    if request.method == 'POST':
        redirect = request.POST.get('next')
        if redirect == '' or redirect is None:
            redirect = reverse('{0}:moneyinout_list'.format(app_name), kwargs={'d': '1'})
        moneyinout_id = request.POST.get('moneyinout_id')
        if moneyinout_id:
            linked_moneyinout = MoneyInOut.objects.filter(pk=moneyinout_id)
            if linked_moneyinout.exists():
                linked_moneyinout.update(is_confirmed=True)
        return HttpResponseRedirect(redirect)


class ProductUpdate(TechBrewUpdateView):
    model = Product
    form_class = ProductUpdateForm
    template_name_suffix = '/change_product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = Product.objects.get(pk=self.object.pk)
        return context

    @method_decorator([login_required, permission_required('{0}.change_product'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class ProductNameUpdate(TechBrewUpdateView):
    model = ProductName
    form_class = ProductNameForm
    template_name_suffix = '/change_productname'

    @method_decorator([login_required, permission_required('{0}.change_productname'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class ProductStyleUpdateView(UpdateView):
    model = ProductStyle
    form_class = ProductStyleForm
    template_name_suffix = '/productstyle_update'

    @method_decorator([login_required, permission_required('{0}.change_productstyle'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class ProductCategoryUpdate(TechBrewUpdateView):
    model = ProductCategory
    form_class = ProductCategoryForm
    template_name_suffix = '/change_productcategory'

    @method_decorator([login_required, permission_required('{0}.change_productcategory'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class ProductPackUpdate(TechBrewUpdateView):
    model = ProductPackSizeUnit
    form_class = ProductPackForm
    template_name_suffix = '/change_productpacksizeunit'

    @method_decorator([login_required, permission_required('{0}.change_productpacksizeunit'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class BrewUpdate(UpdateView):
    model = Brew
    form_class = BrewUpdateForm
    template_name_suffix = '/change_brew'

    def get_success_url(self):
        if self.request.GET:
            if self.request.GET.get('next'):
                return self.request.GET.get('next')
        return super().get_success_url()

    def form_valid(self, form):
        if form.is_valid:
            model = form.save(commit=False)
            model.save()
            if model:
                LogEntry.objects.log_action(
                    user_id=self.request.user.pk,
                    content_type_id=get_content_type_for_model(model).pk,
                    object_id=model.pk,
                    object_repr=str(model),
                    action_flag=CHANGE,
                )
            Tank.objects.filter(current_brew_code=self.object.brew_batch_code).update(current_brew_code=None,
                                                                                      tank_state_id=None)
            Tank.objects.filter(pk=self.object.tank_id).update(current_brew_code=self.object.brew_batch_code,
                                                               tank_state_id=1)
        return super().form_valid(form)

    @method_decorator([login_required, permission_required('{0}.change_brew'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class PackUpdate(TechBrewUpdateView):
    model = Pack
    form_class = PackUpdateForm
    template_name_suffix = '/change_pack'

    @method_decorator([login_required, permission_required('{0}.change_pack'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class ReportUpdate(TechBrewUpdateView):
    model = Report
    form_class = ReportForm
    template_name_suffix = '/change_report'

    @method_decorator([login_required, permission_required('{0}.change_report'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class SaleOrderUpdate(TechBrewUpdateView):
    model = SaleOrder
    form_class = SaleOrderUpdateForm
    template_name_suffix = '/change_saleorder'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.user:
            linked_employee = Employee.objects.filter(linked_account=self.request.user.id)
            linked_client = Client.objects.filter(created_by=self.request.user.id).filter(is_active=True)
            if linked_employee.exists():
                context['employee'] = linked_employee
                context['client'] = linked_client
            else:
                context['employee'] = Employee.objects.filter(is_salesman=True)
                context['client'] = Client.objects.filter(is_active=True)
        return context

    @method_decorator([login_required, permission_required('{0}.change_saleorder'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


@login_required
@permission_required('{0}.delete_saleorder'.format(app_name))
def delete_sale_order(request, pk):
    if request:
        ojs = SaleOrder.objects.filter(pk=pk)
        if ojs.exists():
            oj = ojs.first()
            linked_sales = Sale.objects.filter(sale_order=oj)
            if linked_sales.exists():
                for linked_sale in linked_sales:
                    if linked_sale.sale_price_link:
                        linked_mio = MoneyInOut.objects.filter(pk=linked_sale.sale_price_link.pk)
                        if linked_mio.exists():
                            linked_mio = linked_mio.first()
                            LogEntry.objects.log_action(
                                user_id=request.user.pk,
                                content_type_id=get_content_type_for_model(linked_mio).pk,
                                object_id=linked_mio.pk,
                                object_repr=str(linked_mio),
                                action_flag=DELETION,
                            )
                            linked_mio.delete()
                    LogEntry.objects.log_action(
                        user_id=request.user.pk,
                        content_type_id=get_content_type_for_model(linked_sale).pk,
                        object_id=linked_sale.pk,
                        object_repr=str(linked_sale),
                        action_flag=DELETION,
                    )
                    linked_sale.delete()
            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=get_content_type_for_model(oj).pk,
                object_id=oj.pk,
                object_repr=str(oj),
                action_flag=DELETION,
            )
            oj.delete()
        return HttpResponseRedirect(reverse('{0}:sale_order_list'.format(app_name)))
    return HttpResponseRedirect(reverse('{0}:sale_order_list'.format(app_name)))


class SaleOrderStateUpdate(TechBrewUpdateView):
    model = SaleOrder
    form_class = SaleOrderStateUpdateForm
    template_name_suffix = '/update_order_state'

    @method_decorator([login_required, permission_required('{0}.confirm_sale'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class SaleUpdate(UpdateView):
    model = Sale
    form_class = SaleUpdateForm
    template_name_suffix = '/change_sale'

    def get_success_url(self):
        if self.request.GET:
            if self.request.GET.get('next'):
                return self.request.GET.get('next')
        return super().get_success_url()

    def form_valid(self, form):
        if form.is_valid:
            model = form.save(commit=False)
            if model.sale_price < 0:
                model.sale_price = - model.sale_price
            if model.sale_price_link_id:
                MoneyInOut.objects.filter(pk=self.object.sale_price_link_id).update(
                    money_in_out=self.object.sale_price,
                    money_in_out_date=self.object.sale_date,
                    is_confirmed=self.object.fee_received,
                    is_active=self.object.is_active,
                )
            model.save()
            if model:
                LogEntry.objects.log_action(
                    user_id=self.request.user.pk,
                    content_type_id=get_content_type_for_model(model).pk,
                    object_id=model.pk,
                    object_repr=str(model),
                    action_flag=CHANGE,
                )
            selected_pack = model.pack
            pn_left = Pack.objects.get(pk=selected_pack.pk).pack_num_left
            if pn_left > 0:
                Pack.objects.filter(pk=selected_pack.pk).update(state=True)
            elif pn_left <= 0:
                Pack.objects.filter(pk=selected_pack.pk).update(state=False)
        return super().form_valid(form)

    @method_decorator([login_required, permission_required('{0}.change_sale'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


@login_required
@permission_required('{0}.delete_sale'.format(app_name))
def sale_delete(request, pk):
    if request:
        ojs = Sale.objects.filter(pk=pk)
        if ojs.exists():
            oj = ojs.first()
            selected_pack = oj.pack
            order_id = oj.sale_order.pk
            linked_money_io = MoneyInOut.objects.filter(pk=oj.sale_price_link.pk)
            if linked_money_io.exists():
                l_mio = linked_money_io.first()
                LogEntry.objects.log_action(
                    user_id=request.user.pk,
                    content_type_id=get_content_type_for_model(l_mio).pk,
                    object_id=l_mio.pk,
                    object_repr=str(l_mio),
                    action_flag=DELETION,
                )
                l_mio.delete()
            LogEntry.objects.log_action(
                user_id=request.user.pk,
                content_type_id=get_content_type_for_model(oj).pk,
                object_id=oj.pk,
                object_repr=str(oj),
                action_flag=DELETION,
            )
            oj.delete()
            if Pack.objects.get(pk=selected_pack.pk).pack_num_left > 0:
                Pack.objects.filter(pk=selected_pack.pk).update(state=True)
            return HttpResponseRedirect(reverse('{0}:sale_order_detail'.format(app_name), args=[order_id]))


@login_required
@permission_required('{0}.confirm_sale'.format(app_name))
def sale_confirm(request):
    if request.method == 'POST':
        redirect = request.POST.get('next')
        if redirect == '' or redirect is None:
            redirect = reverse('{0}:sale_list'.format(app_name), kwargs={'c': '1'})
        sale_id = request.POST.get('sale_id')
        if sale_id:
            linked_sale = Sale.objects.filter(pk=sale_id)
            if linked_sale.exists():
                linked_sale.update(is_confirmed=True)
            linked_sale_order = SaleOrder.objects.filter(pk=linked_sale.first().sale_order_id)
            if linked_sale_order.exists():
                related_sales = Sale.objects.filter(
                    sale_order_id=linked_sale.first().sale_order_id).filter(is_confirmed=False)
                if not related_sales.exists():
                    linked_sale_order.update(is_delivered=True)
        return HttpResponseRedirect(redirect)


@login_required
@permission_required('{0}.confirm_fee_receive'.format(app_name))
def sale_pay(request):
    if request.method == 'POST':
        redirect = request.POST.get('next')
        if redirect == '' or redirect is None:
            redirect = reverse('{0}:sale_list'.format(app_name), kwargs={'d': '1'})
        sale_id = request.POST.get('sale_id')
        if sale_id:
            linked_sale = Sale.objects.filter(pk=sale_id)
            if linked_sale.exists():
                linked_sale.update(fee_received=True)
                linked_money_io = linked_sale.first().sale_price_link
                if linked_money_io:
                    MoneyInOut.objects.filter(pk=linked_money_io.pk).update(is_confirmed=True)
            linked_sale_order = SaleOrder.objects.filter(pk=linked_sale.first().sale_order_id)
            if linked_sale_order.exists():
                related_sales = Sale.objects.filter(
                    sale_order_id=linked_sale.first().sale_order_id).filter(fee_received=False)
                if not related_sales.exists():
                    linked_sale_order.update(fee_received=True)
        return HttpResponseRedirect(redirect)


@login_required
@permission_required('{0}.confirm_sale'.format(app_name))
def sale_order_good_deliver(request):
    if request.method == 'POST':
        redirect = request.POST.get('next')
        sale_order_id = request.POST.get('sale_order_id')
        if redirect == '' or redirect is None:
            if sale_order_id:
                redirect = reverse('{0}:sale_order_detail'.format(app_name), kwargs={'pk': sale_order_id})
            else:
                redirect = reverse('{0}:sale_order_list'.format(app_name))
        if sale_order_id:
            SaleOrder.objects.filter(pk=sale_order_id).update(is_delivered=True)
            Sale.objects.filter(sale_order_id=sale_order_id).update(is_confirmed=True)
        return HttpResponseRedirect(redirect)


@login_required
@permission_required('{0}.confirm_fee_receive'.format(app_name))
def sale_order_fee_receive(request):
    if request.method == 'POST':
        redirect = request.POST.get('next')
        sale_order_id = request.POST.get('sale_order_id')
        if redirect == '' or redirect is None:
            if sale_order_id:
                redirect = reverse('{0}:sale_order_detail'.format(app_name), kwargs={'pk': sale_order_id})
            else:
                redirect = reverse('{0}:sale_order_list'.format(app_name))
        if sale_order_id:
            SaleOrder.objects.filter(pk=sale_order_id).update(fee_received=True)
            Sale.objects.filter(sale_order_id=sale_order_id).update(fee_received=True)
            linked_sales = Sale.objects.filter(sale_order_id=sale_order_id)
            for s in linked_sales:
                if s.sale_price_link:
                    MoneyInOut.objects.filter(pk=s.sale_price_link.pk).update(is_confirmed=True)
        return HttpResponseRedirect(redirect)


@login_required
@permission_required('{0}.change_saleorder'.format(app_name))
def sale_order_next(request):
    if request.method == 'POST':
        redirect = request.POST.get('next')
        if redirect == '' or redirect is None:
            redirect = reverse('{0}:sale_order_list'.format(app_name))
        sale_order_id = request.POST.get('sale_order_id')
        current_order = SaleOrder.objects.filter(pk=sale_order_id)
        if current_order.exists():
            current_order = current_order.first()
            order_state_next = current_order.order_state_id + 1
            if OrderState.objects.filter(pk=order_state_next).exists():
                SaleOrder.objects.filter(pk=sale_order_id).update(order_state_id=order_state_next)
        return HttpResponseRedirect(redirect)


@login_required
@permission_required('{0}.view_product'.format(app_name))
def password_change_own(request):
    redirect = 'public'
    template_name = '{0}/user/password_change.html'.format(app_name)
    if request.user.is_authenticated:
        u = User.objects.get(id=request.user.id)
        form = PasswordChangeForm(u)
        if request.method == 'POST':
            form = PasswordChangeForm(u, request.POST)
            if form.is_valid():
                u.set_password(form.cleaned_data['new_password1'])
                u.save()
        return render(request, template_name=template_name, context={'form': form})
    else:
        return HttpResponseRedirect(reverse(redirect))


class HandBookUpdate(TechBrewUpdateView):
    model = HandBook
    form_class = HandBookForm
    template_name_suffix = '/change_handbook'

    @method_decorator([login_required, permission_required('{0}.change_handbook'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class MaterialInDelete(DeleteView):
    model = MaterialIn
    success_url = '/{0}/material_in_list/'.format(app_name)
    template_name_suffix = '/delete_materialin'

    def get_success_url(self):
        if self.request.GET:
            if self.request.GET.get('next'):
                return self.request.GET.get('next')
        return self.success_url

    def delete(self, request, *args, **kwargs):
        linked_money_io = None
        oj = self.get_object()
        if oj:
            LogEntry.objects.log_action(
                user_id=self.request.user.pk,
                content_type_id=get_content_type_for_model(oj).pk,
                object_id=oj.pk,
                object_repr=str(oj),
                action_flag=DELETION,
            )
        if oj.material_cost_link:
            linked_money_io = oj.material_cost_link
        oj.delete()
        if linked_money_io:
            linked_money_io.delete()
        success_url = self.get_success_url()
        return HttpResponseRedirect(success_url)

    @method_decorator([login_required, permission_required('{0}.delete_materialin'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class MaterialOutDelete(TechBrewDeleteView):
    model = MaterialOut
    success_url = '/{0}/material_out_list/'.format(app_name)
    template_name_suffix = '/delete_materialout'

    @method_decorator([login_required, permission_required('{0}.delete_materialout'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class BrewMonitorUpdate(TechBrewUpdateView):
    model = BrewMonitor
    form_class = BrewMonitorUpdateForm
    template_name_suffix = '/change_brewmonitor'

    @method_decorator([login_required, permission_required('{0}.change_brewmonitor'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class UserUpdate(UpdateView):
    model = User
    form_class = UserUpdateForm
    template_name_suffix = '/update_user'
    success_url = '/{0}/users/'.format(app_name)
    queryset = User.objects.filter(Q(
        user_permissions__content_type__app_label=app_name) | Q(
        groups__permissions__content_type__app_label=app_name)).filter(
        is_superuser=False).distinct().order_by('id')

    def get_success_url(self):
        if self.request.GET:
            if self.request.GET.get('next'):
                return self.request.GET.get('next')
        return self.success_url
    
    def get_template_names(self):
        names = list()
        names.append("{0}/{1}{2}.html".format(app_name, 'user', self.template_name_suffix))
        return names

    def form_valid(self, form):
        if form.is_valid:
            model = form.save(commit=False)
            model.save()
            if model:
                LogEntry.objects.log_action(
                    user_id=self.request.user.pk,
                    content_type_id=get_content_type_for_model(model).pk,
                    object_id=model.pk,
                    object_repr=str(model),
                    action_flag=CHANGE,
                )
        return super().form_valid(form)

    @method_decorator([login_required, permission_required('{0}.change_employee'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)


class GroupUpdate(UpdateView):
    model = Group
    form_class = GroupForm
    template_name_suffix = '/update_group'
    success_url = '/{0}/groups/'.format(app_name)
    queryset = Group.objects.filter(permissions__content_type__app_label=app_name).distinct().order_by('id')

    def get_success_url(self):
        if self.request.GET:
            if self.request.GET.get('next'):
                return self.request.GET.get('next')
        return self.success_url

    def get_template_names(self):
        names = list()
        names.append("{0}/{1}{2}.html".format(app_name, 'user', self.template_name_suffix))
        return names

    def form_valid(self, form):
        if form.is_valid:
            model = form.save(commit=False)
            if app_name not in model.name:
                model.name = '{0}-{1}'.format(app_name, model.name)
                while Group.objects.filter(name=model.name):
                    k = 1
                    model.name = '{0}({1})'.format(model.name, k)
                    k += 1
            model.save()
            if model:
                LogEntry.objects.log_action(
                    user_id=self.request.user.pk,
                    content_type_id=get_content_type_for_model(model).pk,
                    object_id=model.pk,
                    object_repr=str(model),
                    action_flag=CHANGE,
                )
        return super().form_valid(form)

    @method_decorator([login_required, permission_required('{0}.change_employee'.format(app_name))])
    def dispatch(self, request, *args, **kwargs):
        return super(self.__class__, self).dispatch(request, *args, **kwargs)
