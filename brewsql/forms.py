from django.utils.translation import gettext_lazy as _
from django.forms import ModelForm, TextInput, Textarea, DateInput, CheckboxInput, SelectMultiple,\
    ModelMultipleChoiceField, Select, DateTimeInput, NumberInput, EmailInput, TimeInput, HiddenInput, FileInput
from django.db.utils import ProgrammingError
from django.contrib.auth.models import Group, Permission
from django.core.exceptions import ValidationError
from .models import *


class EmployeeStateForm(ModelForm):
    class Meta:
        model = EmployeeState
        fields = ['employee_state_cn', 'employee_state_en']
        widgets = {
            'employee_state_cn': TextInput(attrs={'class': 'form-control', 'placeholder': _('员工状态中文')}),
            'employee_state_en': TextInput(attrs={'class': 'form-control', 'placeholder': _('员工状态英文')}),
        }


class EmployeeForm(ModelForm):

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'birth', 'mobile', 'wechat', 'desc', 'gender', 'linked_account',
                  'title', 'department', 'employee_state', 'is_brewer', 'is_salesman', 'working', 'joined', 'created_by']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@techbrew.cn'}),
            'birth': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'mobile': TextInput(attrs={'class': 'form-control', 'placeholder': '15068800000'}),
            'wechat': TextInput(attrs={'class': 'form-control', 'placeholder': 'wechatID'}),
            'gender': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'desc': Textarea(attrs={'class': 'form-control'}),
            'title': TextInput(attrs={'class': 'form-control'}),
            'department': TextInput(attrs={'class': 'form-control'}),
            'employee_state': Select(attrs={'class': 'selectpicker show-tick form-control',
                                            'data-live-search': 'true'}),
            'is_brewer': CheckboxInput(),
            'is_salesman': CheckboxInput(),
            'working': CheckboxInput(attrs={'type': 'checkbox'}),
            'joined': DateInput(attrs={'class': 'form-control', 'type': 'date',
                                       'value': str(timezone.localdate())}),
            'created_by': HiddenInput(),
        }


class EmployeeUpdateForm(ModelForm):

    class Meta:
        model = Employee
        fields = ['first_name', 'last_name', 'email', 'birth', 'mobile', 'wechat', 'desc', 'gender', 'linked_account',
                  'title', 'department', 'employee_state', 'is_brewer', 'is_salesman', 'working', 'joined', 'created_by']
        widgets = {
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control', 'placeholder': 'email@techbrew.cn'}),
            'birth': DateInput(attrs={'class': 'form-control'}),
            'mobile': TextInput(attrs={'class': 'form-control', 'placeholder': '15068800000'}),
            'wechat': TextInput(attrs={'class': 'form-control', 'placeholder': 'wechatID'}),
            'gender': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'desc': Textarea(attrs={'class': 'form-control'}),
            'title': TextInput(attrs={'class': 'form-control'}),
            'department': TextInput(attrs={'class': 'form-control'}),
            'employee_state': Select(attrs={'class': 'selectpicker show-tick form-control',
                                            'data-live-search': 'true'}),
            'is_brewer': CheckboxInput(),
            'is_salesman': CheckboxInput(),
            'working': CheckboxInput(),
            'joined': DateInput(attrs={'class': 'form-control'}),
            'created_by': HiddenInput(),
        }


class ClientLevelForm(ModelForm):
    class Meta:
        model = ClientLevel
        exclude = ['datetime_created', 'datetime_updated']
        widgets = {
            'level_code': TextInput(attrs={'class': 'form-control'}),
            'level_cn': TextInput(attrs={'class': 'form-control'}),
            'level_en': TextInput(attrs={'class': 'form-control'}),
            'level_desc_cn': Textarea(attrs={'class': 'form-control'}),
            'level_desc_en': Textarea(attrs={'class': 'form-control'}),
        }


class ClientForm(ModelForm):
    class Meta:
        model = Client
        fields = ['name', 'email', 'mobile', 'gender', 'wechat', 'client_company', 'desc', 'client_level',
                  'is_active', 'created_by']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'mobile': TextInput(attrs={'class': 'form-control'}),
            'gender': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'birth': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'wechat': TextInput(attrs={'class': 'form-control'}),
            'client_company': Select(attrs={'class': 'selectpicker show-tick form-control',
                                            'data-live-search': 'true'}),
            'client_level': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'desc': Textarea(attrs={'class': 'form-control'}),
            'is_active': CheckboxInput(),
            'created_by': HiddenInput(),
        }


class SupplierForm(ModelForm):
    class Meta:
        model = Supplier
        fields = ['name', 'email', 'mobile', 'gender', 'wechat', 'supplier_company', 'desc', 'is_active', 'created_by']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'mobile': TextInput(attrs={'class': 'form-control'}),
            'gender': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'birth': DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'wechat': TextInput(attrs={'class': 'form-control'}),
            'supplier_company': Select(attrs={'class': 'selectpicker show-tick form-control',
                                              'data-live-search': 'true'}),
            'desc': Textarea(attrs={'class': 'form-control'}),
            'is_active': CheckboxInput(),
            'created_by': HiddenInput(),
        }


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['company_name_en', 'company_name_cn', 'company_address', 'company_tel', 'email', 'desc',
                  'company_type', 'company_share', 'created_by']
        widgets = {
            'company_name_en': TextInput(attrs={'class': 'form-control'}),
            'company_name_cn': TextInput(attrs={'class': 'form-control'}),
            'company_address': TextInput(attrs={'class': 'form-control'}),
            'company_tel': TextInput(attrs={'class': 'form-control'}),
            'email': EmailInput(attrs={'class': 'form-control'}),
            'desc': Textarea(attrs={'class': 'form-control'}),
            'company_type': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'company_share': CheckboxInput(),
            'created_by': HiddenInput(),
        }


class ProductNameForm(ModelForm):
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
            'brewer': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'client': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'product_type': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'created_by': HiddenInput(),
        }


class ProductCategoryForm(ModelForm):
    class Meta:
        model = ProductCategory
        exclude = ['datetime_created', 'datetime_updated']
        widgets = {
            'product_category_cn': TextInput(attrs={'class': 'form-control'}),
            'product_category_en': TextInput(attrs={'class': 'form-control'}),
            'product_category_desc_cn': Textarea(attrs={'class': 'form-control'}),
            'product_category_desc_en': Textarea(attrs={'class': 'form-control'}),
        }


class ProductPackForm(ModelForm):
    class Meta:
        model = ProductPackSizeUnit
        fields = '__all__'
        widgets = {
            'product_pack_code': TextInput(attrs={'class': 'form-control', 'placeholder': 'A'}),
            'product_pack_size': NumberInput(attrs={'class': 'form-control', 'placeholder': '330'}),
            'product_pack_unit': Select(
                attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'product_pack_type_en': TextInput(attrs={'class': 'form-control', 'placeholder': 'Bottle'}),
            'product_pack_type_cn': TextInput(attrs={'class': 'form-control', 'placeholder': '瓶装'}),
        }


class ProductStyleForm(ModelForm):
    class Meta:
        model = ProductStyle
        exclude = ['datetime_created', 'datetime_updated']
        widgets = {
            'product_style_cn': TextInput(attrs={'class': 'form-control', 'placeholder': '中文名称'}),
            'product_style_en': TextInput(attrs={'class': 'form-control', 'placeholder': '英文名称'}),
            'product_style_desc_cn': Textarea(attrs={'class': 'form-control', 'placeholder': '中文描述'}),
            'product_style_desc_en': Textarea(attrs={'class': 'form-control', 'placeholder': '英文描述'}),
        }


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = ['product_code', 'product_name', 'product_pack', 'product_category', 'created_by']
        widgets = {
            'product_code': TextInput(attrs={'class': 'form-control', 'placeholder': _('产品名称编号+产品规格编号=001A')}),
            'product_name': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'product_pack': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'product_category': SelectMultiple(attrs={'class': 'form-control'}),
            'created_by': HiddenInput(),
        }


class ProductUpdateForm(ModelForm):
    class Meta:
        model = Product
        fields = ['product_code', 'image', 'image_banner', 'files', 'is_show', 'desc_en', 'desc_cn', 'supplier_price',
                  'abv', 'ibu', 'plato', 'barcode', 'product_style',
                  'bar_price', 'public_price', 'created_by', 'index', 'is_banner', 'product_category']
        widgets = {
            'product_code': TextInput(attrs={'class': 'form-control', 'readonly': 'True'}),
            'image': FileInput(),
            'image_banner': FileInput(),
            'files': FileInput(),
            'desc_en': Textarea(attrs={'class': 'form-control'}),
            'desc_cn': Textarea(attrs={'class': 'form-control'}),
            'supplier_price': NumberInput(attrs={'class': 'form-control'}),
            'bar_price': NumberInput(attrs={'class': 'form-control'}),
            'public_price': NumberInput(attrs={'class': 'form-control'}),
            'created_by': HiddenInput(),
            'index': NumberInput(attrs={'class': 'form-control', 'placeholder': _('排序系数')}),
            'product_category': SelectMultiple(attrs={'class': 'form-control'}),
            'abv': TextInput(attrs={'class': 'form-control'}),
            'ibu': TextInput(attrs={'class': 'form-control'}),
            'plato': TextInput(attrs={'class': 'form-control'}),
            'barcode': TextInput(attrs={'class': 'form-control'}),
            'product_style': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
        }


class BrewForm(ModelForm):
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
            'date_start': DateInput(attrs={'class': 'form-control', 'type': 'date',
                                           'value': str(timezone.localdate()), }),
            'product_name': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'recipe': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'tank': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'operator': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'theory_days': NumberInput(attrs={'class': 'form-control'}),
            'created_by': HiddenInput(),
        }


class BrewUpdateForm(ModelForm):
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
            'date_start': DateInput(attrs={'class': 'form-control'}),
            'product_name': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'tank': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'operator': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'theory_days': NumberInput(attrs={'class': 'form-control'}),
            'created_by': HiddenInput(),
        }


class FermentMonitorForm(ModelForm):
    class Meta:
        model = FermentMonitor
        fields = ['brew', 'sg_plato', 'sg', 'plato', 'ph', 't_real', 't_set', 'bar', 'diacetyl', 'qc_report',
                  'dry_hop', 'slag', 'notes', 'cell_mml', 'recorder', 'recorded', 'created_by']
        widgets = {
            'brew': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'recorded': DateTimeInput(attrs={'class': 'form-control',
                                             'value': str(timezone.now())[:19], 'type': 'datetime'}),
            'sg_plato': NumberInput(attrs={'class': 'form-control',
                                           'placeholder': _('自动识别')}),
            'ph': NumberInput(attrs={'class': 'form-control'}),
            't_real': NumberInput(attrs={'class': 'form-control'}),
            't_set': NumberInput(attrs={'class': 'form-control'}),
            'bar': NumberInput(attrs={'class': 'form-control'}),
            'diacetyl': NumberInput(attrs={'class': 'form-control'}),
            'qc_report': FileInput(attrs={'class': 'form-control'}),
            'cell_mml': NumberInput(attrs={'class': 'form-control',
                                           'placeholder': _('million/ml')}),
            'recorder': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'created_by': HiddenInput(),
        }


class BrewMonitorForm(ModelForm):
    class Meta:
        model = BrewMonitor
        exclude = ['datetime_created', 'datetime_updated']
        widgets = {
            'brew_monitor_code': TextInput(attrs={'class': 'form-control'}),
            'brewer': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'brew': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'brew_date': DateInput(attrs={'class': 'form-control', 'type': 'date',
                                          'value': str(timezone.localdate()), }),
            'batch_volume': NumberInput(attrs={'class': 'form-control'}),
            'initial_water': NumberInput(attrs={'class': 'form-control'}),
            'sparge_water': NumberInput(attrs={'class': 'form-control'}),
            'mash_volume': NumberInput(attrs={'class': 'form-control'}),
            'after_boiling_add_water': NumberInput(attrs={'class': 'form-control'}),
            'enter_fermenter_volume': NumberInput(attrs={'class': 'form-control'}),
            'initial_tem': NumberInput(attrs={'class': 'form-control'}),
            'sparge_tem': NumberInput(attrs={'class': 'form-control'}),
            'boiling_full_tem': NumberInput(attrs={'class': 'form-control'}),
            'boiling_full_volume': NumberInput(attrs={'class': 'form-control'}),
            'enter_fermenter_tem': NumberInput(attrs={'class': 'form-control'}),
            'ph_mash_0': NumberInput(attrs={'class': 'form-control'}),
            'ph_mash_1': NumberInput(attrs={'class': 'form-control'}),
            'brix_0': NumberInput(attrs={'class': 'form-control'}),
            'ph_0': NumberInput(attrs={'class': 'form-control'}),
            'brix_1': NumberInput(attrs={'class': 'form-control'}),
            'ph_1': NumberInput(attrs={'class': 'form-control'}),
            'brix_2': NumberInput(attrs={'class': 'form-control'}),
            'ph_2': NumberInput(attrs={'class': 'form-control'}),
            'brix_3': NumberInput(attrs={'class': 'form-control'}),
            'ph_3': NumberInput(attrs={'class': 'form-control'}),
            'og_wort': NumberInput(attrs={'class': 'form-control'}),
            'ph_wort': NumberInput(attrs={'class': 'form-control'}),
            'malt_add_start': TimeInput(attrs={'class': 'form-control timepicker-24'}),
            'malt_add_end': TimeInput(attrs={'class': 'form-control timepicker-24'}),
            'recycle_start': TimeInput(attrs={'class': 'form-control timepicker-24'}),
            'into_boiling': TimeInput(attrs={'class': 'form-control timepicker-24'}),
            'boiling_full': TimeInput(attrs={'class': 'form-control timepicker-24'}),
            'boiling_start': TimeInput(attrs={'class': 'form-control timepicker-24'}),
            'boiling_end': TimeInput(attrs={'class': 'form-control timepicker-24'}),
            'whirlpool_end': TimeInput(attrs={'class': 'form-control timepicker-24'}),
            'enter_fermenter_start': TimeInput(attrs={'class': 'form-control timepicker-24'}),
            'enter_fermenter_end': TimeInput(attrs={'class': 'form-control timepicker-24'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'created_by': HiddenInput(),
        }


class BrewMonitorUpdateForm(ModelForm):
    class Meta:
        model = BrewMonitor
        exclude = ['datetime_created', 'datetime_updated']
        widgets = {
            'brew_monitor_code': TextInput(attrs={'class': 'form-control'}),
            'brewer': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'brew': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'brew_date': DateInput(attrs={'class': 'form-control'}),
            'batch_volume': NumberInput(attrs={'class': 'form-control'}),
            'initial_water': NumberInput(attrs={'class': 'form-control'}),
            'sparge_water': NumberInput(attrs={'class': 'form-control'}),
            'mash_volume': NumberInput(attrs={'class': 'form-control'}),
            'after_boiling_add_water': NumberInput(attrs={'class': 'form-control'}),
            'enter_fermenter_volume': NumberInput(attrs={'class': 'form-control'}),
            'initial_tem': NumberInput(attrs={'class': 'form-control'}),
            'sparge_tem': NumberInput(attrs={'class': 'form-control'}),
            'boiling_full_tem': NumberInput(attrs={'class': 'form-control'}),
            'boiling_full_volume': NumberInput(attrs={'class': 'form-control'}),
            'enter_fermenter_tem': NumberInput(attrs={'class': 'form-control'}),
            'ph_mash_0': NumberInput(attrs={'class': 'form-control'}),
            'ph_mash_1': NumberInput(attrs={'class': 'form-control'}),
            'brix_0': NumberInput(attrs={'class': 'form-control'}),
            'ph_0': NumberInput(attrs={'class': 'form-control'}),
            'brix_1': NumberInput(attrs={'class': 'form-control'}),
            'ph_1': NumberInput(attrs={'class': 'form-control'}),
            'brix_2': NumberInput(attrs={'class': 'form-control'}),
            'ph_2': NumberInput(attrs={'class': 'form-control'}),
            'brix_3': NumberInput(attrs={'class': 'form-control'}),
            'ph_3': NumberInput(attrs={'class': 'form-control'}),
            'og_wort': NumberInput(attrs={'class': 'form-control'}),
            'ph_wort': NumberInput(attrs={'class': 'form-control'}),
            'malt_add_start': TimeInput(attrs={'class': 'form-control timepicker-24'}),
            'malt_add_end': TimeInput(attrs={'class': 'form-control timepicker-24'}),
            'recycle_start': TimeInput(attrs={'class': 'form-control timepicker-24'}),
            'into_boiling': TimeInput(attrs={'class': 'form-control timepicker-24'}),
            'boiling_full': TimeInput(attrs={'class': 'form-control timepicker-24'}),
            'boiling_start': TimeInput(attrs={'class': 'form-control timepicker-24'}),
            'boiling_end': TimeInput(attrs={'class': 'form-control timepicker-24'}),
            'whirlpool_end': TimeInput(attrs={'class': 'form-control timepicker-24'}),
            'enter_fermenter_start': TimeInput(attrs={'class': 'form-control timepicker-24'}),
            'enter_fermenter_end': TimeInput(attrs={'class': 'form-control timepicker-24'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'created_by': HiddenInput(),
        }


class FermentMonitorUpdateForm(ModelForm):
    class Meta:
        model = FermentMonitor
        fields = ['brew', 'sg_plato', 'sg', 'plato', 'ph', 't_real', 't_set', 'bar', 'diacetyl', 'qc_report',
                  'dry_hop', 'slag', 'notes', 'cell_mml', 'recorder', 'recorded', 'created_by']
        widgets = {
            'brew': Select(attrs={'class': 'form-control', 'readonly': 'True'}),
            'recorded': DateTimeInput(attrs={'class': 'form-control',
                                             'value': str(timezone.now())[:19], 'type': 'datetime'}),
            'sg_plato': NumberInput(attrs={'class': 'form-control',
                                           'placeholder': _('1.001至1.199之间自动识别为比重')}),
            'ph': NumberInput(attrs={'class': 'form-control'}),
            't_real': NumberInput(attrs={'class': 'form-control'}),
            't_set': NumberInput(attrs={'class': 'form-control'}),
            'bar': NumberInput(attrs={'class': 'form-control'}),
            'diacetyl': NumberInput(attrs={'class': 'form-control'}),
            'qc_report': FileInput(attrs={'class': 'form-control'}),
            'cell_mml': NumberInput(attrs={'class': 'form-control', 'placeholder': _('百万每毫升')}),
            'recorder': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'created_by': HiddenInput(),
        }


class PackForm(ModelForm):
    class Meta:
        model = Pack
        fields = ['pack_batch_code', 'brew', 'product', 'pack_date', 'pack_start', 'pack_end',
                  'pack_num', 'employee', 'notes', 'created_by']
        widgets = {
            'pack_batch_code': TextInput(attrs={'class': 'form-control'}),
            'brew': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'product': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'pack_date': DateInput(attrs={'class': 'form-control',
                                          'value': str(timezone.localdate()), 'type': 'date'}),
            'pack_start': TimeInput(attrs={'class': 'form-control',
                                           'value': str(timezone.localtime())[11:16], 'type': 'datetime'}),
            'pack_end': TimeInput(attrs={'class': 'form-control',
                                         'value': str(timezone.localtime())[11:16], 'type': 'datetime'}),
            'pack_num': NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'employee': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'created_by': HiddenInput(),
        }


class PackUpdateForm(ModelForm):
    class Meta:
        model = Pack
        fields = ['pack_batch_code', 'pack_date', 'pack_start', 'pack_end', 'state',
                  'pack_num', 'employee', 'notes', 'created_by']
        labels = {
            'state': _('可出库'),
        }
        widgets = {
            'pack_batch_code': TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),
            'pack_date': DateInput(attrs={'class': 'form-control'}),
            'pack_start': TimeInput(attrs={'class': 'form-control timepicker-24'}),
            'pack_end': TimeInput(attrs={'class': 'form-control timepicker-24'}),
            'pack_num': NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'employee': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'created_by': HiddenInput(),
        }


class ReportForm(ModelForm):
    class Meta:
        model = Report
        exclude = ['datetime_created', 'datetime_updated']
        widgets = {
            'report_code': TextInput(attrs={'class': 'form-control'}),
            'pack': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'report_date': DateInput(attrs={'class': 'form-control',
                                            'value': str(timezone.localdate()), 'type': 'date'}),
            'employee': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'ebc': NumberInput(attrs={'class': 'form-control', 'placeholder': _('色度/EBC')}),
            'turbidity': NumberInput(attrs={'class': 'form-control', 'placeholder': _('浊度/EBC')}),
            'foam': NumberInput(attrs={'class': 'form-control', 'placeholder': _('泡持性/s')}),
            'abv': NumberInput(attrs={'class': 'form-control', 'placeholder': _('酒精度/%')}),
            'plato': NumberInput(attrs={'class': 'form-control', 'placeholder': _('原麦汁度/°P')}),
            'total_acid': NumberInput(attrs={'class': 'form-control', 'placeholder': _('总酸含量/(mL/100mL)')}),
            'co2': NumberInput(attrs={'class': 'form-control', 'placeholder': _('二氧化碳/%(质量分数)')}),
            'diacetyl': NumberInput(attrs={'class': 'form-control', 'placeholder': _('双乙酰/mg/L')}),
            'enzyme': CheckboxInput(attrs={'class': 'form-control'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'is_active': CheckboxInput(attrs={'class': 'form-control'}),
            'is_confirmed': CheckboxInput(attrs={'class': 'form-control'}),
            'created_by': HiddenInput(),
        }


class SaleOrderForm(ModelForm):

    class Meta:
        model = SaleOrder
        exclude = ['datetime_created', 'datetime_updated', 'is_active', 'order_state', 'is_delivered', 'fee_received']
        widgets = {
            'sale_order_code': TextInput(attrs={'class': 'form-control'}),
            'sale_order_date': DateInput(attrs={'class': 'form-control',
                                                'value': str(timezone.localdate()), 'type': 'date'}),
            'employee': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'client': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'created_by': HiddenInput(),
        }


class SaleOrderUpdateForm(ModelForm):

    class Meta:
        model = SaleOrder
        exclude = ['datetime_created', 'datetime_updated', 'is_delivered', 'fee_received', 'is_from_wx']
        widgets = {
            'sale_order_code': TextInput(attrs={'class': 'form-control'}),
            'sale_order_date': DateInput(attrs={'class': 'form-control'}),
            'employee': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'client': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'order_state': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'is_active': CheckboxInput(attrs={'class': 'form-control'}),
            'created_by': HiddenInput(),
        }


class SaleOrderStateUpdateForm(ModelForm):

    class Meta:
        model = SaleOrder
        fields = ['sale_order_code', 'sale_order_date', 'order_state', 'notes', 'is_active', 'created_by']
        widgets = {
            'sale_order_code': TextInput(attrs={'class': 'form-control'}),
            'sale_order_date': DateInput(attrs={'class': 'form-control'}),
            'order_state': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'is_active': CheckboxInput(attrs={'class': 'form-control'}),
            'created_by': HiddenInput(),
        }


class SaleForm(ModelForm):

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
        widgets = {
            'sale_order': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'sale_date': DateInput(attrs={'class': 'form-control', 'value': str(timezone.localdate()), 'type': 'date'}),
            'pack': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'sale_num': NumberInput(attrs={'class': 'form-control'}),
            'sale_price': NumberInput(attrs={'class': 'form-control'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'is_sale': CheckboxInput(attrs={'class': 'form-control'}),
            'is_active': CheckboxInput(attrs={'class': 'form-control'}),
            'created_by': HiddenInput(),
        }


class SaleUpdateForm(ModelForm):

    class Meta:
        model = Sale
        fields = ['sale_order', 'sale_date', 'pack', 'sale_num', 'sale_price', 'notes', 'is_sale', 'is_active',
                  'created_by']
        widgets = {
            'sale_order': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true',
                                        'required': 'true'}),
            'sale_date': DateInput(attrs={'class': 'form-control'}),
            'pack': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'sale_num': NumberInput(attrs={'class': 'form-control'}),
            'sale_price': NumberInput(attrs={'class': 'form-control'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'is_sale': CheckboxInput(attrs={'class': 'form-control'}),
            'is_active': CheckboxInput(attrs={'class': 'form-control'}),
            'created_by': HiddenInput(),
        }


class TankStateUpdateForm(ModelForm):
    class Meta:
        model = TankSateUpdate
        fields = ['tank', 'tank_state_now', 'created_by']
        widgets = {
            'tank': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'tank_state_now': Select(attrs={'class': 'selectpicker show-tick form-control',
                                            'data-live-search': 'true'}),
            'created_by': HiddenInput(),
        }


class MaterialForm(ModelForm):
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
            'material_category': Select(attrs={'class': 'selectpicker show-tick form-control',
                                               'data-live-search': 'true'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'created_by': HiddenInput(),
        }


class MaterialBatchForm(ModelForm):
    class Meta:
        model = MaterialBatch
        fields = ['material_batch_code', 'material', 'material_pack_size_unit', 'expire_date', 'qc_report',
                  'para', 'notes', 'created_by']
        widgets = {
            'material_batch_code': TextInput(attrs={'class': 'form-control', 'placeholder': _('必填且不得重复')}),
            'material': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'material_pack_size_unit': Select(attrs={'class': 'selectpicker show-tick form-control',
                                                     'data-live-search': 'true'}),
            'para': TextInput(attrs={'class': 'form-control', 'placeholder': _('参数')}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'expire_date': DateInput(attrs={'class': 'form-control',
                                            'value': str(timezone.localdate()), 'type': 'date'}),
            'created_by': HiddenInput(),
            'qc_report': FileInput(attrs={'class': 'form-control'}),
        }


class MaterialBatchUpdateForm(ModelForm):
    class Meta:
        model = MaterialBatch
        fields = ['material_batch_code', 'material', 'material_pack_size_unit', 'expire_date', 'state', 'qc_report',
                  'para', 'notes', 'modified_by']
        labels = {
            'state': _('显示'),
        }
        widgets = {
            'material_batch_code': TextInput(attrs={'class': 'form-control', 'placeholder': _('必填且不得重复')}),
            'material': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'material_pack_size_unit': Select(attrs={'class': 'selectpicker show-tick form-control',
                                                     'data-live-search': 'true'}),
            'para': TextInput(attrs={'class': 'form-control', 'placeholder': _('参数')}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'expire_date': DateInput(attrs={'class': 'form-control'}),
            'modified_by': HiddenInput(),
            'qc_report': FileInput(attrs={'class': 'form-control'}),
        }


class MaterialInForm(ModelForm):
    class Meta:
        model = MaterialIn
        fields = ['material_in_date', 'material_batch', 'warehouse', 'supplier',
                  'amount', 'material_cost', 'material_cost_link', 'recorder', 'notes', 'created_by', 'is_confirmed']
        widgets = {
            'material_in_date': DateInput(attrs={'class': 'form-control',
                                                 'value': str(timezone.localdate()), 'type': 'date'}),
            'material_batch': Select(attrs={'class': 'selectpicker show-tick form-control',
                                            'data-live-search': 'true'}),
            'warehouse': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'supplier': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'amount': NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'material_cost': NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'recorder': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'created_by': HiddenInput(),
        }


class MaterialInUpdateForm(ModelForm):
    class Meta:
        model = MaterialIn
        fields = ['material_in_date', 'material_batch', 'warehouse', 'supplier',
                  'amount', 'material_cost', 'recorder', 'notes', 'created_by', 'is_confirmed']
        widgets = {
            'material_in_date': DateInput(attrs={'class': 'form-control'}),
            'material_batch': Select(attrs={'class': 'selectpicker show-tick form-control',
                                            'data-live-search': 'true'}),
            'warehouse': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'supplier': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'amount': NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'material_cost': NumberInput(attrs={'class': 'form-control'}),
            'recorder': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'created_by': HiddenInput(),
        }


class MaterialOutForm(ModelForm):

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
            'material_out_date': DateInput(attrs={'class': 'form-control',
                                                  'value': str(timezone.localdate()), 'type': 'date'}),
            'material_batch': Select(attrs={'class': 'selectpicker show-tick form-control',
                                            'data-live-search': 'true'}),
            'brew': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'amount': NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'recorder': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'created_by': HiddenInput(),
        }


class MaterialOutUpdateForm(ModelForm):
    class Meta:
        model = MaterialOut
        fields = ['material_out_date', 'material_batch', 'brew', 'amount',
                  'recorder', 'notes', 'created_by']
        widgets = {
            'material_out_date': DateInput(attrs={'class': 'form-control'}),
            'material_batch': Select(
                attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'brew': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'amount': NumberInput(attrs={'class': 'form-control', 'placeholder': _('数量')}),
            'recorder': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'created_by': HiddenInput(),
        }


class MoneyInOutTypeForm(ModelForm):
    class Meta:
        model = MoneyInOutType
        exclude = ['is_auto']
        widgets = {
            'money_in_out_type_cn': TextInput(attrs={'class': 'form-control'}),
            'money_in_out_type_en': TextInput(attrs={'class': 'form-control'}),
        }


class MoneyInOutForm(ModelForm):
    class Meta:
        model = MoneyInOut
        fields = ['money_in_out', 'money_in_out_date', 'money_in_out_type', 'notes', 'recorded_by', 'created_by',
                  'is_confirmed']
        widgets = {
            'money_in_out': NumberInput(attrs={'class': 'form-control', 'placeholder': _('金额')}),
            'money_in_out_date': DateInput(attrs={'class': 'form-control',
                                                  'value': str(timezone.localdate()), 'type': 'date'}),
            'money_in_out_type': Select(attrs={'class': 'selectpicker show-tick form-control',
                                               'data-live-search': 'true'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'recorded_by': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'created_by': HiddenInput(),
        }


class MoneyInOutUpdateForm(ModelForm):
    class Meta:
        model = MoneyInOut
        fields = ['money_in_out', 'money_in_out_date', 'money_in_out_type', 'notes', 'recorded_by', 'created_by',
                  'is_confirmed']
        widgets = {
            'money_in_out': NumberInput(attrs={'class': 'form-control', 'placeholder': _('金额')}),
            'money_in_out_date': DateInput(attrs={'class': 'form-control'}),
            'money_in_out_type': Select(attrs={'class': 'selectpicker show-tick form-control',
                                               'data-live-search': 'true'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'recorded_by': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'created_by': HiddenInput(),
        }


class MoneyInOutStateUpdateForm(ModelForm):
    class Meta:
        model = MoneyInOut
        fields = ['money_in_out_date', 'notes', 'recorded_by', 'created_by']
        widgets = {
            'money_in_out_date': DateInput(attrs={'class': 'form-control'}),
            'notes': Textarea(attrs={'class': 'form-control'}),
            'recorded_by': Select(attrs={'class': 'selectpicker show-tick form-control', 'data-live-search': 'true'}),
            'created_by': HiddenInput(),
        }


class MaterialPackSizeUnitForm(ModelForm):
    class Meta:
        model = MaterialPackSizeUnit
        fields = '__all__'
        widgets = {
            'material_pack_size': NumberInput(attrs={'class': 'form-control', 'placeholder': '10'}),
            'material_pack_unit': Select(attrs={'class': 'selectpicker show-tick form-control',
                                                'data-live-search': 'true'}),
        }


class WarehouseForm(ModelForm):
    class Meta:
        model = Warehouse
        fields = '__all__'
        widgets = {
            'place_code': TextInput(attrs={'class': 'form-control', 'placeholder': _('位置编号')}),
            'place_desc': TextInput(attrs={'class': 'form-control', 'placeholder': _('位置描述')}),
        }


class CompanyTypeForm(ModelForm):
    class Meta:
        model = CompanyType
        fields = '__all__'
        widgets = {
            'company_type_en': TextInput(attrs={'class': 'form-control', 'placeholder': _('类型英文名')}),
            'company_type_cn': TextInput(attrs={'class': 'form-control', 'placeholder': _('类型中文名')}),
        }


class HandBookForm(ModelForm):
    class Meta:
        model = HandBook
        exclude = ['datetime_created', 'datetime_updated']
        widgets = {
            'chapter': NumberInput(attrs={'class': 'form-control', 'min': '0'}),
            'chapter_code': TextInput(attrs={'class': 'form-control'}),
            'chapter_name_cn': TextInput(attrs={'class': 'form-control'}),
            'chapter_name_en': TextInput(attrs={'class': 'form-control'}),
            'chapter_content_cn': Textarea(attrs={'class': 'summernote'}),
            'chapter_content_en': Textarea(attrs={'class': 'summernote'}),
        }


class UserUpdateForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['groups'] = ModelMultipleChoiceField(
            queryset=Group.objects.filter(permissions__content_type__app_label=app_name).distinct(),
            required=True,
            label=_('权限分组'),
            error_messages={'required': "以下是必填项"},
            widget=SelectMultiple(
                attrs={'class': 'form-control'}),
        )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'groups', 'is_active']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'first_name': TextInput(attrs={'class': 'form-control'}),
            'last_name': TextInput(attrs={'class': 'form-control'}),
            'email': TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'email': 'E-mail',
        }


class GroupForm(ModelForm):

    def __init__(self, *args, **kwargs):
        super(self.__class__, self).__init__(*args, **kwargs)
        self.fields['permissions'] = ModelMultipleChoiceField(
            queryset=Permission.objects.all(),
            required=True,
            label=_('权限'),
            error_messages={'required': "以下是必填项"},
            widget=SelectMultiple(attrs={'class': 'form-control'}),
        )

    class Meta:
        model = Group
        fields = ['name', 'permissions']
        widgets = {
            'name': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': _('分组名称')})
        }
