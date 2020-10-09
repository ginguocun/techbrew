from django.http import HttpResponseRedirect, Http404
from django.views.generic.edit import UpdateView, DeleteView
from django.shortcuts import render
from django.contrib.admin.models import LogEntry, CHANGE, DELETION
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.exceptions import ImproperlyConfigured
from ..forms import *
from ..utils import get_obj_permission_required

app_name = GeneralConfig.name


def get_content_type_for_model(obj):
    from django.contrib.contenttypes.models import ContentType
    return ContentType.objects.get_for_model(obj, for_concrete_model=False)


class TechBrewDeleteView(PermissionRequiredMixin, DeleteView):

    @staticmethod
    def get_required_object_permissions(model_cls):
        return '{0}.delete_{1}'.format(model_cls._meta.app_label, model_cls._meta.model_name)

    def get_permission_required(self):
        return get_obj_permission_required(self)

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


class TechBrewUpdateView(PermissionRequiredMixin, UpdateView):

    @staticmethod
    def get_required_object_permissions(model_cls):
        return '{0}.change_{1}'.format(getattr(model_cls, '_meta').app_label, getattr(model_cls, '_meta').model_name)

    def get_permission_required(self):
        return get_obj_permission_required(self)

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
@permission_required('{0}.change_tankstate'.format(app_name), raise_exception=True)
def tank_update(request,
                template_name='{0}/tank/tank_update.html'.format(app_name),
                ob=TankStateUpdateForm, 
                redirect='{0}:tanks_overview'.format(app_name)):
    tanks = Tank.objects.all().order_by('id')
    tank_states = TankState.objects.all()
    if request.method == 'POST':
        form = ob(request.POST)
        if form.is_valid():
            model = form.save(commit=False)
            model.save()
            if model:
                LogEntry.objects.log_action(
                    user_id=request.user.pk,
                    content_type_id=get_content_type_for_model(model).pk,
                    object_id=model.pk,
                    object_repr=str(model),
                    action_flag=CHANGE,
                )
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
            Tank.objects.filter(id=form.data.get('tank')).update(tank_state_id=int(request.POST['tank_state_now']))
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


class ClientUpdate(TechBrewUpdateView):
    model = Client
    form_class = ClientUpdateForm
    template_name_suffix = '/change_client'


class EmployeeStateUpdate(TechBrewUpdateView):
    model = EmployeeState
    form_class = EmployeeStateForm
    template_name_suffix = '/change_employee_state'


class EmployeeUpdate(TechBrewUpdateView):
    model = Employee
    form_class = EmployeeUpdateForm
    template_name_suffix = '/change_employee'


class SupplierUpdate(TechBrewUpdateView):
    model = Supplier
    form_class = SupplierUpdateForm
    template_name_suffix = '/change_supplier'


class CompanyTypeUpdate(TechBrewUpdateView):
    model = CompanyType
    form_class = CompanyTypeForm
    template_name_suffix = '/change_companytype'


class CompanyUpdate(TechBrewUpdateView):
    model = Company
    form_class = CompanyUpdateForm
    template_name_suffix = '/change_company'


class MaterialPackUpdate(TechBrewUpdateView):
    model = MaterialPackSizeUnit
    form_class = MaterialPackSizeUnitForm
    template_name_suffix = '/change_materialpacksizeunit'


class MaterialUpdate(TechBrewUpdateView):
    model = Material
    form_class = MaterialForm
    template_name_suffix = '/change_material'


class MaterialBatchUpdate(TechBrewUpdateView):
    model = MaterialBatch
    form_class = MaterialBatchUpdateForm
    template_name_suffix = '/change_materialbatch'


class WarehouseUpdate(TechBrewUpdateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name_suffix = '/change_warehouse'


class MaterialInUpdate(TechBrewUpdateView):
    model = MaterialIn
    form_class = MaterialInUpdateForm
    template_name_suffix = '/change_materialin'

    def form_valid(self, form):
        if form.is_valid:
            model = form.save(commit=False)
            if model.material_cost > 0:
                model.material_cost = - model.material_cost
            # if model.material_cost_link_id:
            #     MoneyInOut.objects.filter(pk=self.object.material_cost_link_id).update(
            #         money_in_out=self.object.material_cost,
            #         money_in_out_date=self.object.material_in_date)
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


class MaterialOutUpdate(TechBrewUpdateView):
    model = MaterialOut
    form_class = MaterialOutUpdateForm
    template_name_suffix = '/change_materialout'


class FermentMonitorDelete(TechBrewDeleteView):
    model = FermentMonitor
    template_name_suffix = '/fermentmonitor_confirm_delete'
    success_url = '/ferment_monitor_list/'


class MoneyInOutTypeUpdate(TechBrewUpdateView):
    model = MoneyInOutType
    form_class = MoneyInOutTypeForm
    template_name_suffix = '/change_money_inout_type'


class MoneyInOutUpdate(TechBrewUpdateView):
    model = MoneyInOut
    form_class = MoneyInOutUpdateForm
    template_name_suffix = '/change_moneyinout'

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


class MoneyInOutDelete(TechBrewDeleteView):
    model = MoneyInOut
    success_url = '/money_io_list/'
    template_name_suffix = '/delete_moneyinout'

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


class MoneyInOutStateUpdate(TechBrewUpdateView):
    model = MoneyInOut
    form_class = MoneyInOutStateUpdateForm
    template_name_suffix = '/change_moneyinout_state'

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


class ProductNameUpdate(TechBrewUpdateView):
    model = ProductName
    form_class = ProductNameForm
    template_name_suffix = '/change_productname'


class ProductStyleUpdateView(UpdateView):
    model = ProductStyle
    form_class = ProductStyleForm
    template_name_suffix = '/productstyle_update'


class ProductCategoryUpdate(TechBrewUpdateView):
    model = ProductCategory
    form_class = ProductCategoryForm
    template_name_suffix = '/change_productcategory'


class ProductPackUpdate(TechBrewUpdateView):
    model = ProductPackSizeUnit
    form_class = ProductPackForm
    template_name_suffix = '/change_productpacksizeunit'


class BrewUpdate(TechBrewUpdateView):
    model = Brew
    form_class = BrewUpdateForm
    template_name_suffix = '/change_brew'

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


class PackUpdate(TechBrewUpdateView):
    model = Pack
    form_class = PackUpdateForm
    template_name_suffix = '/change_pack'


class ReportUpdate(TechBrewUpdateView):
    model = Report
    form_class = ReportForm
    template_name_suffix = '/change_report'


class SaleOrderUpdate(TechBrewUpdateView):
    model = SaleOrder
    form_class = SaleOrderUpdateForm
    template_name_suffix = '/change_saleorder'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        clients = Client.objects.filter(is_active=True)
        if not self.request.user.has_perm('{0}.view_all_clients'.format(app_name)):
            clients = clients.filter(created_by=self.request.user.pk)
        linked_employee = Employee.objects.filter(linked_account=self.request.user.pk)
        if linked_employee.exists():
            context['employee'] = linked_employee
        else:
            context['employee'] = Employee.objects.filter(is_salesman=True)
        context['client'] = clients
        return context

    def get_queryset(self):
        q = self.model.objects.all()
        if not self.request.user.has_perm('{0}.view_all_sale_orders'.format(app_name)):
            q = q.filter(created_by=self.request.user)
        return q


@login_required
@permission_required('{0}.delete_saleorder'.format(app_name))
def delete_sale_order(request, pk):
    if request:
        ojs = SaleOrder.objects.filter(pk=pk)
        if not request.user.has_perm('{0}.view_all_sale_orders'.format(app_name)):
            ojs = ojs.filter(created_by=request.user)
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
    permission_required = '{0}.confirm_sale'.format(app_name)

    def get_queryset(self):
        q = self.model.objects.all()
        if not self.request.user.has_perm('{0}.view_all_sale_orders'.format(app_name)):
            q = q.filter(created_by=self.request.user)
        return q


class SaleUpdate(TechBrewUpdateView):
    model = Sale
    form_class = SaleUpdateForm
    template_name_suffix = '/change_sale'

    def get_queryset(self):
        q = self.model.objects.all()
        if not self.request.user.has_perm('{0}.view_all_sale_orders'.format(app_name)):
            q = q.filter(created_by=self.request.user)
        return q

    def form_valid(self, form):
        if form.is_valid:
            model = form.save(commit=False)
            if model.sale_price < 0:
                model.sale_price = - model.sale_price
            # if model.sale_price_link_id:
            #     MoneyInOut.objects.filter(pk=self.object.sale_price_link_id).update(
            #         money_in_out=self.object.sale_price,
            #         money_in_out_date=self.object.sale_date,
            #         is_confirmed=self.object.fee_received,
            #         is_active=self.object.is_active,
            #     )
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


@login_required
@permission_required('{0}.delete_sale'.format(app_name))
def sale_delete(request, pk):
    if request:
        ojs = Sale.objects.filter(pk=pk)
        if ojs.exists():
            oj = ojs.first()
            selected_pack = oj.pack
            order_id = oj.sale_order.pk
            if oj.sale_price_link:
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
            if not request.user.has_perm('{0}.view_all_sale_orders'.format(app_name)):
                linked_sale = linked_sale.filter(created_by=request.user)
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
            if not request.user.has_perm('{0}.view_all_sale_orders'.format(app_name)):
                linked_sale = linked_sale.filter(created_by=request.user)
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
            sale_orders = SaleOrder.objects.filter(pk=sale_order_id)
            sales = Sale.objects.filter(sale_order_id=sale_order_id)
            if not request.user.has_perm('{0}.view_all_sale_orders'.format(app_name)):
                sale_orders = sale_orders.filter(created_by=request.user)
                sales = sales.filter(created_by=request.user)
            if sale_orders.exists():
                sale_orders.update(is_delivered=True)
            if sales.exists():
                sales.update(is_confirmed=True)
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
            sale_orders = SaleOrder.objects.filter(pk=sale_order_id)
            if not request.user.has_perm('{0}.view_all_sale_orders'.format(app_name)):
                sale_orders = sale_orders.filter(created_by=request.user)
            if sale_orders.exists():
                sale_orders.update(fee_received=True)
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
def password_change_own(request):
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
        return Http404


class HandBookUpdate(TechBrewUpdateView):
    model = HandBook
    form_class = HandBookForm
    template_name_suffix = '/change_handbook'


class MaterialInDelete(TechBrewDeleteView):
    model = MaterialIn
    success_url = '/material_in_list/'
    template_name_suffix = '/delete_materialin'

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


class MaterialOutDelete(TechBrewDeleteView):
    model = MaterialOut
    success_url = '/material_out_list/'
    template_name_suffix = '/delete_materialout'


class BrewMonitorUpdate(TechBrewUpdateView):
    model = BrewMonitor
    form_class = BrewMonitorUpdateForm
    template_name_suffix = '/change_brewmonitor'


class UserUpdate(TechBrewUpdateView):
    model = User
    form_class = UserUpdateForm
    template_name_suffix = '/update_user'
    success_url = '/users/'
    queryset = User.objects.filter(is_superuser=False)
    permission_required = '{0}.change_employee'.format(app_name)
    
    def get_template_names(self):
        names = list()
        names.append("{0}/{1}{2}.html".format(app_name, 'user', self.template_name_suffix))
        return names


class GroupUpdate(TechBrewUpdateView):
    model = Group
    form_class = GroupForm
    template_name_suffix = '/update_group'
    success_url = '/groups/'
    queryset = Group.objects.all()
    permission_required = '{0}.change_employee'.format(app_name)

    def get_template_names(self):
        names = list()
        names.append("{0}/{1}{2}.html".format(app_name, 'user', self.template_name_suffix))
        return names
