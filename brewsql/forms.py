from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, TextInput, Textarea, DateInput, CheckboxInput,\
    ModelMultipleChoiceField, Select, DateTimeInput, NumberInput, TimeInput
from django.db.utils import ProgrammingError
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError
from .models import *


class TbModelForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(TbModelForm, self).__init__(*args, **kwargs)
        if self.fields:
            for k, v in self.fields.items():
                v.widget.attrs.update({'class': 'form-control'})
                if isinstance(v.widget, DateTimeInput):
                    v.widget.attrs.update(
                        {'class': 'form-control', 'type': 'datetime', 'value': str(timezone.now())[:19]})
                if isinstance(v.widget, DateInput):
                    v.widget.attrs.update(
                        {'class': 'form-control', 'type': 'date', 'value': str(timezone.localdate())})
                if isinstance(v.widget, Select):
                    v.widget.attrs.update(
                        {'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'})
                if isinstance(v.widget, TimeInput):
                    v.widget.attrs.update(
                        {'class': 'form-control', 'value': str(timezone.localtime())[11:16], 'type': 'datetime'})
                if isinstance(v.widget, Textarea):
                    v.widget.attrs.update({'class': 'form-control summernote'})
                if isinstance(v.widget, CheckboxInput):
                    v.widget.attrs.update({'type': 'checkbox'})

    def save(self, commit=True):
        return super(TbModelForm, self).save(commit)


class EmployeeStateForm(TbModelForm):
    class Meta:
        model = EmployeeState
        fields = ['employee_state_cn', 'employee_state_en']
        widgets = {
            'employee_state_cn': TextInput(attrs={'class': 'form-control', 'placeholder': _('员工状态中文')}),
            'employee_state_en': TextInput(attrs={'class': 'form-control', 'placeholder': _('员工状态英文')}),
        }


class EmployeeForm(TbModelForm):

    class Meta:
        model = Employee
        exclude = ['datetime_created', 'datetime_updated']


class EmployeeUpdateForm(TbModelForm):

    class Meta:
        model = Employee
        exclude = ['datetime_created', 'datetime_updated', 'created_by']


class ClientLevelForm(TbModelForm):
    class Meta:
        model = ClientLevel
        exclude = ['datetime_created', 'datetime_updated']


class ClientForm(TbModelForm):
    class Meta:
        model = Client
        exclude = ['datetime_created', 'datetime_updated']


class ClientUpdateForm(TbModelForm):
    class Meta:
        model = Client
        exclude = ['datetime_created', 'datetime_updated', 'created_by']


class SupplierForm(TbModelForm):
    class Meta:
        model = Supplier
        exclude = ['datetime_created', 'datetime_updated']


class SupplierUpdateForm(TbModelForm):
    class Meta:
        model = Supplier
        exclude = ['datetime_created', 'datetime_updated', 'created_by']


class CompanyForm(TbModelForm):
    class Meta:
        model = Company
        exclude = ['datetime_created', 'datetime_updated']


class CompanyUpdateForm(TbModelForm):
    class Meta:
        model = Company
        exclude = ['datetime_created', 'datetime_updated', 'created_by']


class ProductNameForm(TbModelForm):
    class Meta:
        try:
            product_name_code = str(ProductName.objects.count() + 1).zfill(3)
        except ProgrammingError:
            product_name_code = ''
        model = ProductName
        fields = ['product_name_code', 'product_name_cn', 'product_name_en', 'brewer', 'client',
                  'product_type', 'notes', 'is_show', 'created_by']
        widgets = {
            'product_name_code': TextInput(attrs={'class': 'form-control', 'value': product_name_code,
                                                  'placeholder': _('建议3位数字形式')}),
            'product_name_cn': TextInput(attrs={'class': 'form-control', 'placeholder': '雪花'}),
            'product_name_en': TextInput(attrs={'class': 'form-control', 'placeholder': 'Snow'}),
        }


class ProductCategoryForm(TbModelForm):
    class Meta:
        model = ProductCategory
        exclude = ['datetime_created', 'datetime_updated']


class ProductPackForm(TbModelForm):
    class Meta:
        model = ProductPackSizeUnit
        fields = '__all__'
        widgets = {
            'product_pack_code': TextInput(attrs={'class': 'form-control', 'placeholder': 'A'}),
            'product_pack_size': NumberInput(attrs={'class': 'form-control', 'placeholder': '330'}),
            'product_pack_type_en': TextInput(attrs={'class': 'form-control', 'placeholder': 'Bottle'}),
            'product_pack_type_cn': TextInput(attrs={'class': 'form-control', 'placeholder': '瓶装'}),
        }


class ProductStyleForm(TbModelForm):
    class Meta:
        model = ProductStyle
        exclude = ['datetime_created', 'datetime_updated']
        widgets = {
            'product_style_cn': TextInput(attrs={'class': 'form-control', 'placeholder': '中文名称'}),
            'product_style_en': TextInput(attrs={'class': 'form-control', 'placeholder': '英文名称'}),
            'product_style_desc_cn': Textarea(attrs={'class': 'form-control', 'placeholder': '中文描述'}),
            'product_style_desc_en': Textarea(attrs={'class': 'form-control', 'placeholder': '英文描述'}),
        }


class ProductForm(TbModelForm):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['product_category'] = ModelMultipleChoiceField(
            queryset=ProductCategory.objects.all(),
            label=_('产品归类'),
        )

    class Meta:
        model = Product
        fields = ['product_code', 'product_name', 'product_pack', 'product_category', 'created_by']
        widgets = {
            'product_code': TextInput(attrs={'class': 'form-control', 'placeholder': _('产品名称编号+产品规格编号=001A')}),
        }


class ProductUpdateForm(TbModelForm):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['product_category'] = ModelMultipleChoiceField(
            queryset=ProductCategory.objects.all(),
            label=_('产品归类'),
        )

    class Meta:
        model = Product
        fields = ['product_code', 'image', 'image_banner', 'files', 'is_show', 'desc_en', 'desc_cn', 'supplier_price',
                  'abv', 'ibu', 'plato', 'barcode', 'product_style',
                  'bar_price', 'public_price', 'created_by', 'index', 'is_banner', 'product_category']
        widgets = {
            'product_code': TextInput(attrs={'class': 'form-control', 'readonly': 'True'}),
            'index': NumberInput(attrs={'class': 'form-control', 'placeholder': _('排序系数')}),
        }


class BrewForm(TbModelForm):
    class Meta:
        model = Brew
        fields = ['brew_batch_code', 'product_name', 'recipe', 'tank', 'theory_days',
                  'date_start', 'operator', 'notes', 'created_by']
        labels = {
            'tank': _('发酵罐号'),
        }
        help_texts = {
            'brew_batch_code': _('请输入酿造批次号'),
        }
        error_messages = {
            'brew_batch_code': {
                'max_length': _("酿造批次号太长了点,请缩减!"),
            },
        }
        widgets = {
            'brew_batch_code': TextInput(attrs={'class': 'form-control', 'value': '',
                                                'placeholder': _('非必填,可自动生成')}),
        }


class BrewUpdateForm(TbModelForm):
    class Meta:
        model = Brew
        fields = ['brew_batch_code', 'product_name', 'tank', 'theory_days',
                  'date_start', 'operator', 'notes', 'created_by']
        labels = {
            'tank': _('发酵罐号'),
        }
        help_texts = {
            'brew_batch_code': _('请输入酿造批次号'),
        }
        widgets = {
            'brew_batch_code': TextInput(attrs={'class': 'form-control', 'readonly': 'True'}),
        }


class FermentMonitorForm(TbModelForm):
    class Meta:
        model = FermentMonitor
        fields = ['brew', 'sg_plato', 'sg', 'plato', 'ph', 't_real', 't_set', 'bar', 'diacetyl', 'qc_report',
                  'dry_hop', 'slag', 'notes', 'cell_mml', 'recorder', 'recorded', 'created_by']
        widgets = {
            'sg_plato': NumberInput(attrs={'class': 'form-control',
                                           'placeholder': _('自动识别')}),
            'cell_mml': NumberInput(attrs={'class': 'form-control',
                                           'placeholder': _('million/ml')}),
        }


class BrewMonitorForm(TbModelForm):
    class Meta:
        model = BrewMonitor
        exclude = ['datetime_created', 'datetime_updated']


class BrewMonitorUpdateForm(TbModelForm):
    class Meta:
        model = BrewMonitor
        exclude = ['datetime_created', 'datetime_updated']


class FermentMonitorUpdateForm(TbModelForm):
    class Meta:
        model = FermentMonitor
        fields = ['brew', 'sg_plato', 'sg', 'plato', 'ph', 't_real', 't_set', 'bar', 'diacetyl', 'qc_report',
                  'dry_hop', 'slag', 'notes', 'cell_mml', 'recorder', 'recorded', 'created_by']
        widgets = {
            'brew': Select(attrs={'class': 'form-control', 'readonly': 'True'}),
            'sg_plato': NumberInput(attrs={'class': 'form-control',
                                           'placeholder': _('1.001至1.199之间自动识别为比重')}),
            'cell_mml': NumberInput(attrs={'class': 'form-control', 'placeholder': _('百万每毫升')}),
        }


class PackForm(TbModelForm):
    class Meta:
        model = Pack
        fields = ['pack_batch_code', 'brew', 'product', 'pack_date', 'pack_start', 'pack_end',
                  'pack_num', 'employee', 'notes', 'created_by']
        widgets = {
            'pack_num': NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }


class PackUpdateForm(TbModelForm):
    class Meta:
        model = Pack
        fields = ['pack_batch_code', 'pack_date', 'pack_start', 'pack_end', 'state',
                  'pack_num', 'employee', 'notes', 'created_by']
        labels = {
            'state': _('可出库'),
        }
        widgets = {
            'pack_batch_code': TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'pack_start': TimeInput(attrs={'class': 'form-control timepicker-24'}),
            'pack_end': TimeInput(attrs={'class': 'form-control timepicker-24'}),
            'pack_num': NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }


class ReportForm(TbModelForm):
    class Meta:
        model = Report
        exclude = ['datetime_created', 'datetime_updated']
        widgets = {
            'ebc': NumberInput(attrs={'class': 'form-control', 'placeholder': _('色度/EBC')}),
            'turbidity': NumberInput(attrs={'class': 'form-control', 'placeholder': _('浊度/EBC')}),
            'foam': NumberInput(attrs={'class': 'form-control', 'placeholder': _('泡持性/s')}),
            'abv': NumberInput(attrs={'class': 'form-control', 'placeholder': _('酒精度/%')}),
            'plato': NumberInput(attrs={'class': 'form-control', 'placeholder': _('原麦汁度/°P')}),
            'total_acid': NumberInput(attrs={'class': 'form-control', 'placeholder': _('总酸含量/(mL/100mL)')}),
            'co2': NumberInput(attrs={'class': 'form-control', 'placeholder': _('二氧化碳/%(质量分数)')}),
            'diacetyl': NumberInput(attrs={'class': 'form-control', 'placeholder': _('双乙酰/mg/L')}),
        }


class SaleOrderForm(TbModelForm):

    class Meta:
        model = SaleOrder
        exclude = ['datetime_created', 'datetime_updated', 'is_active', 'order_state', 'is_delivered', 'fee_received']


class SaleOrderUpdateForm(TbModelForm):

    class Meta:
        model = SaleOrder
        exclude = ['datetime_created', 'datetime_updated', 'is_delivered', 'fee_received', 'is_from_wx']


class SaleOrderStateUpdateForm(TbModelForm):

    class Meta:
        model = SaleOrder
        fields = ['sale_order_code', 'sale_order_date', 'order_state', 'notes', 'is_active', 'created_by']


class SaleForm(TbModelForm):

    def clean_sale_num(self):
        data = self.cleaned_data['sale_num']
        selected_pack = self.cleaned_data['pack']
        if selected_pack:
            pack_net_left = float(selected_pack.pack_num_left) - float(data)
            if pack_net_left < 0:
                raise ValidationError(_('所选批次库存不足！'))
        return data

    class Meta:
        model = Sale
        fields = ['sale_order', 'sale_date', 'pack', 'sale_num', 'sale_price', 'notes', 'is_sale', 'is_active',
                  'created_by']


class SaleUpdateForm(TbModelForm):

    class Meta:
        model = Sale
        fields = ['sale_order', 'sale_date', 'pack', 'sale_num', 'sale_price', 'notes', 'is_sale', 'is_active',
                  'created_by']


class TankStateUpdateForm(TbModelForm):
    class Meta:
        model = TankSateUpdate
        fields = ['tank', 'tank_state_now', 'created_by']


class MaterialForm(TbModelForm):
    class Meta:
        model = Material
        fields = ['material_code', 'material_en', 'material_cn', 'material_category', 'account_code',
                  'notes', 'created_by']
        widgets = {
            'material_code': TextInput(attrs={'class': 'form-control',
                                              'placeholder': _('可自动生成')}),
            'material_en': TextInput(attrs={'class': 'form-control', 'placeholder': _('Pale ale malt')}),
            'material_cn': TextInput(attrs={'class': 'form-control', 'placeholder': _('浅色大麦芽')}),
            'account_code': TextInput(attrs={'class': 'form-control', 'placeholder': _('财务记账编号')}),
        }


class MaterialBatchForm(TbModelForm):
    class Meta:
        model = MaterialBatch
        fields = ['material_batch_code', 'material', 'material_pack_size_unit', 'expire_date', 'qc_report',
                  'para', 'notes', 'created_by']
        widgets = {
            'material_batch_code': TextInput(attrs={'class': 'form-control', 'placeholder': _('必填且不得重复')}),
            'para': TextInput(attrs={'class': 'form-control', 'placeholder': _('参数')}),
        }


class MaterialBatchUpdateForm(TbModelForm):
    class Meta:
        model = MaterialBatch
        fields = ['material_batch_code', 'material', 'material_pack_size_unit', 'expire_date', 'state', 'qc_report',
                  'para', 'notes', 'modified_by']
        labels = {
            'state': _('显示'),
        }
        widgets = {
            'material_batch_code': TextInput(attrs={'class': 'form-control', 'placeholder': _('必填且不得重复')}),
            'para': TextInput(attrs={'class': 'form-control', 'placeholder': _('参数')}),

        }


class MaterialInForm(TbModelForm):
    class Meta:
        model = MaterialIn
        fields = ['material_in_date', 'material_batch', 'warehouse', 'supplier',
                  'amount', 'material_cost', 'material_cost_link', 'recorder', 'notes', 'created_by', 'is_confirmed']
        widgets = {
            'amount': NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'material_cost': NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }


class MaterialInUpdateForm(TbModelForm):
    class Meta:
        model = MaterialIn
        fields = ['material_in_date', 'material_batch', 'warehouse', 'supplier',
                  'amount', 'material_cost', 'recorder', 'notes', 'created_by', 'is_confirmed']
        widgets = {
            'amount': NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }


class MaterialOutForm(TbModelForm):

    def clean_amount(self):
        data = self.cleaned_data['amount']
        selected_material_batch = self.cleaned_data['material_batch']
        if selected_material_batch:
            material_net_left = float(selected_material_batch.material_batch_total_left) - float(data)
            if material_net_left < -0.5:
                raise ValidationError(_('所选批次原料的库存不足！'))
        return data

    class Meta:
        model = MaterialOut
        fields = ['material_out_date', 'material_batch', 'brew', 'amount',
                  'recorder', 'notes', 'created_by']
        widgets = {
            'amount': NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }


class MaterialOutUpdateForm(TbModelForm):
    class Meta:
        model = MaterialOut
        fields = ['material_out_date', 'material_batch', 'brew', 'amount', 'recorder', 'notes', 'created_by']


class MoneyInOutTypeForm(TbModelForm):
    class Meta:
        model = MoneyInOutType
        exclude = ['is_auto']


class MoneyInOutForm(TbModelForm):
    class Meta:
        model = MoneyInOut
        fields = ['money_in_out', 'money_in_out_date', 'money_in_out_type', 'notes',
                  'recorded_by', 'created_by', 'appendix', 'is_confirmed']


class MoneyInOutUpdateForm(TbModelForm):
    class Meta:
        model = MoneyInOut
        fields = ['money_in_out', 'money_in_out_date', 'money_in_out_type', 'notes',
                  'recorded_by', 'modified_by', 'appendix', 'is_confirmed']


class MoneyInOutStateUpdateForm(TbModelForm):
    class Meta:
        model = MoneyInOut
        fields = ['money_in_out_date', 'notes', 'recorded_by', 'appendix', 'modified_by']


class MaterialPackSizeUnitForm(TbModelForm):
    class Meta:
        model = MaterialPackSizeUnit
        fields = '__all__'


class WarehouseForm(TbModelForm):
    class Meta:
        model = Warehouse
        fields = '__all__'
        widgets = {
            'place_code': TextInput(attrs={'class': 'form-control', 'placeholder': _('位置编号')}),
            'place_desc': TextInput(attrs={'class': 'form-control', 'placeholder': _('位置描述')}),
        }


class CompanyTypeForm(TbModelForm):
    class Meta:
        model = CompanyType
        fields = '__all__'
        widgets = {
            'company_type_en': TextInput(attrs={'class': 'form-control', 'placeholder': _('类型英文名')}),
            'company_type_cn': TextInput(attrs={'class': 'form-control', 'placeholder': _('类型中文名')}),
        }


class HandBookForm(TbModelForm):
    class Meta:
        model = HandBook
        exclude = ['datetime_created', 'datetime_updated']
        widgets = {
            'chapter': NumberInput(attrs={'class': 'form-control', 'min': '0'}),
        }


class UserUpdateForm(TbModelForm):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['groups'] = ModelMultipleChoiceField(
            queryset=Group.objects.all(),
            required=True,
            label=_('权限分组'),
            error_messages={'required': "以下是必填项"},
        )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'groups', 'is_active']
        labels = {
            'email': 'E-mail',
        }


class GroupForm(TbModelForm):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['permissions'] = ModelMultipleChoiceField(
            queryset=Permission.objects.all(),
            required=True,
            label=_('权限'),
            error_messages={'required': "以下是必填项"},
        )

    class Meta:
        model = Group
        fields = ['name', 'permissions']
