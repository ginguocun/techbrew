from copy import deepcopy
import datetime
from decimal import Decimal

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.admin.models import LogEntry, ADDITION
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.contenttypes.models import ContentType
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.paginator import Paginator
from django.db.models import F
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView

from ..utils import plato2sg, sg2plato, get_obj_permission_required
from ..forms import *


def get_month_date(d=timezone.localdate()):
    c_year = str(d)[2:4]
    c_month = str(d)[5:7]
    c_day = str(d)[8:10]
    # c_hour = str(d)[11:13]
    # c_min = str(d)[14:16]
    return '{0}{1}{2}'.format(c_year, c_month, c_day)


def get_content_type_for_model(obj):
    from django.contrib.contenttypes.models import ContentType
    return ContentType.objects.get_for_model(obj, for_concrete_model=False)


class TechBrewCreateView(PermissionRequiredMixin, CreateView):

    @staticmethod
    def get_required_object_permissions(model_cls):
        return '{0}.add_{1}'.format(getattr(model_cls, '_meta').app_label, getattr(model_cls, '_meta').model_name)

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
                    action_flag=ADDITION,
                )
        return super().form_valid(form)


class EmployeeStateCreate(TechBrewCreateView):
    model = EmployeeState
    form_class = EmployeeStateForm
    template_name_suffix = '/employee_state_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = EmployeeState.objects.all()
        return context


class EmployeeCreate(TechBrewCreateView):
    model = Employee
    form_class = EmployeeForm
    template_name_suffix = '/add_employee'


class ClientCreate(TechBrewCreateView):
    model = Client
    form_class = ClientForm
    template_name_suffix = '/add_client'


class SupplierCreate(TechBrewCreateView):
    model = Supplier
    form_class = SupplierForm
    template_name_suffix = '/add_supplier'


class CompanyCreate(TechBrewCreateView):
    model = Company
    form_class = CompanyForm
    template_name_suffix = '/add_company'


class ProductPackSizeUnitCreate(TechBrewCreateView):
    model = ProductPackSizeUnit
    form_class = ProductPackForm
    template_name_suffix = '/add_productpacksizeunit'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paginator = Paginator(ProductPackSizeUnit.objects.all(), 10)
        page = self.request.GET.get('page', 1)
        context['page_obj'] = paginator.get_page(page)
        return context


class ProductNameCreate(TechBrewCreateView):
    model = ProductName
    form_class = ProductNameForm
    template_name_suffix = '/add_productname'


class ProductCategoryCreate(TechBrewCreateView):
    model = ProductCategory
    form_class = ProductCategoryForm
    template_name_suffix = '/add_productcategory'


class ProductStyleCreateView(TechBrewCreateView):
    model = ProductStyle
    form_class = ProductStyleForm
    template_name_suffix = '/productstyle_create'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product_style_list'] = ProductStyle.objects.all()
        return context


class BrewCreate(TechBrewCreateView):
    model = Brew
    form_class = BrewForm
    template_name_suffix = '/add_brew'

    def form_valid(self, form):
        if form.is_valid:
            model = form.save(commit=False)
            if model.brew_batch_code:
                if len(model.brew_batch_code) < 3:
                    model.brew_batch_code = None
            if not model.brew_batch_code:
                product_name_code = ProductName.objects.get(id=model.product_name_id).product_name_code
                brew_batch_code_c = str(Brew.objects.filter(product_name_id=model.product_name_id).count() + 1).zfill(3)
                if not model.date_start:
                    model.date_start = timezone.localdate()
                brew_batch_code = '{0}{1}{2}'.format(get_month_date(d=model.date_start),
                                                     brew_batch_code_c,
                                                     product_name_code)
                while Brew.objects.filter(brew_batch_code=brew_batch_code):
                    brew_batch_code_c = str(int(brew_batch_code_c) + 1).zfill(3)
                    brew_batch_code = '{0}{1}{2}'.format(get_month_date(d=model.date_start),
                                                         brew_batch_code_c,
                                                         product_name_code)
                model.brew_batch_code = brew_batch_code
            model.save()
            if model:
                LogEntry.objects.log_action(
                    user_id=self.request.user.pk,
                    content_type_id=get_content_type_for_model(model).pk,
                    object_id=model.pk,
                    object_repr=str(model),
                    action_flag=ADDITION,
                )
            Tank.objects.filter(pk=form.data.get('tank')).update(current_brew_code=model.brew_batch_code,
                                                                 tank_state_id=1)
        return super(BrewCreate, self).form_valid(form)


class BrewMonitorCreate(TechBrewCreateView):
    model = BrewMonitor
    form_class = BrewMonitorForm
    template_name_suffix = '/add_brewmonitor'


@login_required
@permission_required('{0}.add_fermentmonitor'.format(app_name))
def add_ferment_monitor(request, pk=None):
    ob = FermentMonitorForm
    template_name = '{0}/fermentmonitor/add_ferment_record.html'.format(app_name)
    if pk is None:
        brew_batches = Brew.objects.filter(Q(tank__current_brew_code=F('brew_batch_code'))).distinct().order_by('-id')
        if request.GET.get('next'):
            redirect_to = request.GET.get('next')
        else:
            redirect_to = reverse('{0}:ferment_monitor_list'.format(app_name))
    else:
        brew_batches = Brew.objects.filter(pk=pk)
        redirect_to = reverse('{0}:brew_detail'.format(app_name), kwargs={"pk": pk})
    if request.method == 'POST':
        form = ob(request.POST, request.FILES)
        if form.is_valid():
            r = request.POST
            if form.cleaned_data['sg_plato']:
                plato = float(form.cleaned_data['sg_plato'])
                if plato >= 1.2 or plato <= 1:
                    sg = plato2sg(plato)
                else:
                    sg = plato
                    plato = sg2plato(sg)
                new_data = deepcopy(r)
                new_data['sg'] = Decimal(str(round(sg, 3)))
                new_data['plato'] = Decimal(str(round(plato, 1)))
                new_form = ob(new_data, request.FILES)
                if new_form.is_valid():
                    new_form.save()
                if new_form.errors:
                    return render(request, template_name=template_name,
                                  context={'form': form, 'brew_batches': brew_batches})
            else:
                model = form.save()
                if model:
                    LogEntry.objects.log_action(
                        user_id=request.user.pk,
                        content_type_id=get_content_type_for_model(model).pk,
                        object_id=model.pk,
                        object_repr=str(model),
                        action_flag=ADDITION,
                    )
            tank = Tank.objects.get(pk=Brew.objects.get(pk=r['brew']).tank.pk)
            if tank:
                if r['t_real']:
                    tank.jkm_t_real = r['t_real']
                if r['t_set']:
                    tank.jkm_t_set = r['t_set']
                tank.jkm_updated = timezone.now()
                tank.save()
        if form.errors:
            return render(request, template_name=template_name,
                          context={'form': form, 'brew_batches': brew_batches, 'pk': pk})
        return HttpResponseRedirect(redirect_to)
    else:
        form = ob()
        return render(request, template_name=template_name,
                      context={'form': form, 'brew_batches': brew_batches, 'pk': pk})


@login_required
@permission_required('{0}.add_pack'.format(app_name))
def add_pack(request, template_name='{0}/pack/add_pack.html'.format(app_name)):
    brews = Brew.objects.filter(Q(
        date_start__gte=(timezone.now() - datetime.timedelta(days=300))) | Q(
        tank__current_brew_code=F('brew_batch_code'))).distinct().order_by('-id')
    if request.method == 'POST':
        r = request.POST
        pack_form = PackForm(request.POST, prefix='pack')
        product_form = ProductForm(request.POST, prefix='product')
        if pack_form:
            brew = Brew.objects.get(id=int(r['pack-brew']))
            product_pack = ProductPackSizeUnit.objects.get(id=int(r['product-product_pack']))
            product_name = ProductName.objects.get(id=brew.product_name_id)
            pack_count = Pack.objects.filter(brew_id=int(brew.id)).count() + 1
            product_code = '{0}{1}'.format(product_name.product_name_code, product_pack.product_pack_code)
            while Product.objects.filter(product_code=product_code):
                product_code += 's'
            product, created = Product.objects.get_or_create(
                product_name_id=brew.product_name_id,
                product_pack_id=r['product-product_pack'],
                defaults={'product_code': product_code},)
            pack_batch_code = '{0}{1}{2}'.format(
                    brew.brew_batch_code,
                    product_pack.product_pack_code,
                    pack_count)
            while Pack.objects.filter(pack_batch_code=pack_batch_code):
                pack_count += 1
                pack_batch_code = '{0}{1}{2}'.format(
                    brew.brew_batch_code,
                    product_pack.product_pack_code,
                    pack_count)
            new_pack = deepcopy(r)
            new_pack['pack-pack_batch_code'] = pack_batch_code
            new_pack['pack-product'] = product.id
            new_pack['pack-state'] = True
            new_pack_form = PackForm(new_pack, prefix='pack')
            if new_pack_form.is_valid():
                model = new_pack_form.save()
                if model:
                    LogEntry.objects.log_action(
                        user_id=request.user.pk,
                        content_type_id=get_content_type_for_model(model).pk,
                        object_id=model.pk,
                        object_repr=str(model),
                        action_flag=ADDITION,
                    )
                if r['next']:
                    return redirect(r['next'])
                return redirect('{0}:pack_list'.format(app_name))
            else:
                return render(request, template_name=template_name,
                              context={'pack_form': new_pack_form, 'product_form': product_form, 'brews': brews})
        elif pack_form.errors or product_form.errors:
            return render(request, template_name=template_name,
                          context={'pack_form': pack_form, 'product_form': product_form, 'brews': brews})
    else:
        pack_form = PackForm(prefix='pack')
        product_form = ProductForm(prefix='product')
    return render(request, template_name=template_name,
                  context={'pack_form': pack_form, 'product_form': product_form, 'brews': brews})


class ReportCreate(TechBrewCreateView):
    model = Report
    form_class = ReportForm
    template_name_suffix = '/add_report'


class SaleOrderCreate(TechBrewCreateView):
    model = SaleOrder
    form_class = SaleOrderForm
    template_name_suffix = '/add_saleorder'

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


class SaleCreate(TechBrewCreateView):
    model = Sale
    form_class = SaleForm
    template_name_suffix = '/add_sale'

    def get_context_data(self, **kwargs):
        context = super(SaleCreate, self).get_context_data(**kwargs)
        context['packs'] = Pack.objects.filter(state=True)
        sale_orders = SaleOrder.objects.filter(is_delivered=False)
        if not self.request.user.has_perm('{0}.view_all_sale_orders'.format(app_name)):
            sale_orders = sale_orders.filter(created_by=self.request.user)
        context['sale_orders'] = sale_orders
        return context

    def form_valid(self, form):
        if form.is_valid:
            model = form.save(commit=False)
            selected_pack = model.pack
            # if model.sale_price is not None:
            #     mio = MoneyInOut(
            #         money_in_out=model.sale_price,
            #         money_in_out_date=model.sale_date,
            #         money_in_out_type_id=2,  # TODO add id=2 to MoneyInOutType
            #         notes=u'订单:{0} 产品:{1} 数量: {2}'.format(
            #             model.sale_order,
            #             getattr(selected_pack, 'pack_batch_code'),
            #             model.sale_num
            #         ),
            #         recorded_by_id=self.request.user.pk,
            #         is_confirmed=False,
            #         created_by=model.created_by)
            #     mio.save()
            #     if mio:
            #         LogEntry.objects.log_action(
            #             user_id=self.request.user.pk,
            #             content_type_id=get_content_type_for_model(mio).pk,
            #             object_id=mio.pk,
            #             object_repr=str(mio),
            #             action_flag=ADDITION,
            #         )
            #     model.sale_price_link = mio
            model.save()
            if model:
                LogEntry.objects.log_action(
                    user_id=self.request.user.pk,
                    content_type_id=get_content_type_for_model(model).pk,
                    object_id=model.pk,
                    object_repr=str(model),
                    action_flag=ADDITION,
                )
            if selected_pack.pack_num_left <= 0:
                Pack.objects.filter(pk=selected_pack.pk).update(state=False)
        return super(SaleCreate, self).form_valid(form)


class MaterialCreate(TechBrewCreateView):
    model = Material
    form_class = MaterialForm
    template_name_suffix = '/add_material'

    def form_valid(self, form):
        if form.is_valid:
            model = form.save(commit=False)
            if model.material_code:
                if len(model.material_code) < 3:
                    model.material_code = None
            if not model.material_code:
                material_code_c = str(Material.objects.filter(
                    material_category=model.material_category_id).count() + 1).zfill(3)
                material_category_c = MaterialCategory.objects.get(id=model.material_category_id).material_category_code
                material_code = '{0}{1}'.format(material_category_c, material_code_c)
                while Material.objects.filter(material_code=material_code):
                    material_code_c = str(int(material_code_c)+1).zfill(3)
                    material_code = '{0}{1}'.format(material_category_c, material_code_c)
                model.material_code = material_code
            model.save()
            if model:
                LogEntry.objects.log_action(
                    user_id=self.request.user.pk,
                    content_type_id=get_content_type_for_model(model).pk,
                    object_id=model.pk,
                    object_repr=str(model),
                    action_flag=ADDITION,
                )
        return super().form_valid(form)


class MaterialBatchCreate(TechBrewCreateView):
    model = MaterialBatch
    form_class = MaterialBatchForm
    template_name_suffix = '/add_materialbatch'


class MaterialInCreate(TechBrewCreateView):
    model = MaterialIn
    form_class = MaterialInForm
    template_name_suffix = '/add_materialin'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['material_batches'] = MaterialBatch.objects.filter(state=True)
        return context

    def form_valid(self, form):
        if form.is_valid:
            model = form.save(commit=False)
            if model.material_cost > 0:
                model.material_cost = - model.material_cost
            # mio = MoneyInOut(
            #     money_in_out=model.material_cost,
            #     money_in_out_date=model.material_in_date,
            #     money_in_out_type_id='1',  # TODO add id=1 to MoneyInOutType
            #     notes='{0} + {1}'.format(model.material_batch, model.amount),
            #     recorded_by_id=model.recorder_id,
            #     is_confirmed=False,
            #     created_by=model.created_by,)
            # mio.save()
            # if mio:
            #     LogEntry.objects.log_action(
            #         user_id=self.request.user.pk,
            #         content_type_id=get_content_type_for_model(mio).pk,
            #         object_id=mio.pk,
            #         object_repr=str(mio),
            #         action_flag=ADDITION,
            #     )
            # model.material_cost_link_id = mio.pk
            model.save()
            if model:
                LogEntry.objects.log_action(
                    user_id=self.request.user.pk,
                    content_type_id=get_content_type_for_model(model).pk,
                    object_id=model.pk,
                    object_repr=str(model),
                    action_flag=ADDITION,
                )
        return super().form_valid(form)


class MaterialOutCreate(TechBrewCreateView):
    model = MaterialOut
    form_class = MaterialOutForm
    template_name_suffix = '/add_materialout'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['material_batches'] = MaterialBatch.objects.all()
        context['brews'] = Brew.objects.filter(Q(
            date_start__gte=(timezone.now() - datetime.timedelta(days=300))) | Q(
            tank__current_brew_code=F('brew_batch_code'))).distinct().order_by('-id')
        return context


class MoneyInOutTypeCreate(TechBrewCreateView):
    model = MoneyInOutType
    form_class = MoneyInOutTypeForm
    template_name_suffix = '/add_money_inout_type'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['inout_types'] = MoneyInOutType.objects.all()
        return context


class MoneyInOutCreate(TechBrewCreateView):
    model = MoneyInOut
    form_class = MoneyInOutForm
    template_name_suffix = '/add_moneyinout'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['money_in_out_type'] = MoneyInOutType.objects.filter(is_auto=False)
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
                    action_flag=ADDITION,
                )
        return super().form_valid(form)


class MaterialPackSizeUnitCreate(TechBrewCreateView):
    model = MaterialPackSizeUnit
    form_class = MaterialPackSizeUnitForm
    template_name_suffix = '/material_pack_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = MaterialPackSizeUnit.objects.all()
        return context


class WarehouseCreate(TechBrewCreateView):
    model = Warehouse
    form_class = WarehouseForm
    template_name_suffix = '/warehouse_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['warehouse_list'] = Warehouse.objects.all()
        return context


class CompanyTypeCreate(TechBrewCreateView):
    model = CompanyType
    form_class = CompanyTypeForm
    template_name_suffix = '/company_type_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = CompanyType.objects.all()
        return context


class ClientLevelCreate(TechBrewCreateView):
    model = ClientLevel
    form_class = ClientLevelForm
    template_name_suffix = '/clientlevel_list'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data'] = ClientLevel.objects.all()
        return context


class HandBookCreate(TechBrewCreateView):
    model = HandBook
    form_class = HandBookForm
    template_name_suffix = '/add_handbook'


@login_required
@permission_required('{0}.add_employee'.format(app_name))
def create_s_user(request):
    template_name = '{0}/user/user_list.html'.format(app_name)
    form = AuthenticationForm
    user_created = None
    permission = Permission.objects.get(
        codename='view_product',
        content_type=ContentType.objects.get_for_model(Product),
    )
    users_have = User.objects.filter(is_superuser=False).distinct().order_by('id')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        if username and password:
            user_exist = User.objects.filter(username=username)
            if user_exist.exists():
                return render(request, template_name=template_name,
                              context={'form': form, 'user_exist': user_exist,
                                       'users_have': users_have})
            user_created = User.objects.create_user(username, '', password)
            user_created.user_permissions.add(permission)
            if user_created:
                LogEntry.objects.log_action(
                    user_id=request.user.pk,
                    content_type_id=get_content_type_for_model(user_created).pk,
                    object_id=user_created.pk,
                    object_repr=str(user_created),
                    action_flag=ADDITION,
                )
            users_have = User.objects.filter(is_superuser=False).distinct().order_by('id')
    return render(request, template_name=template_name,
                  context={'form': form, 'user_created': user_created, 'users_have': users_have})


class GroupCreate(TechBrewCreateView):
    model = Group
    form_class = GroupForm
    template_name_suffix = '/group_list'
    success_url = '/groups/'

    def get_template_names(self):
        names = list()
        names.append("{0}/{1}{2}.html".format(app_name, 'user', self.template_name_suffix))
        return names

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['groups'] = Group.objects.all()
        return context
