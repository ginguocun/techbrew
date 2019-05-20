from django.contrib import admin
from .models import *
from django.utils.safestring import mark_safe
from django.utils.translation import gettext_lazy as _
from django.conf import settings

admin.site.site_header = '管理界面'
admin.site.site_title = '管理界面'
admin.site.index_title = '管理界面'


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('bank_account', 'bank', 'bank_address', 'desc')
    search_fields = ['bank_account']


@admin.register(EmployeeState)
class EmployeeStateAdmin(admin.ModelAdmin):
    list_display = ('pk', 'employee_state_cn', 'employee_state_en')


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'mobile', 'wechat', 'title', 'is_brewer', 'is_salesman',
                    'datetime_created', 'datetime_updated')
    list_filter = ('is_brewer', 'is_salesman')
    search_fields = ['first_name', 'last_name']


@admin.register(CompanyType)
class CompanyTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'company_type_en', 'company_type_cn')


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'company_name_cn', 'company_name_en', 'email', 'company_tel', 'company_type', 'desc')
    list_filter = ('company_type',)
    search_fields = ['company_name_cn', 'company_name_en']


@admin.register(ClientLevel)
class ClientLevelAdmin(admin.ModelAdmin):
    list_display = ('level_code', 'level_cn', 'level_en')


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'mobile', 'wechat', 'client_company', 'is_active')
    search_fields = ['name', 'desc']


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'wechat', 'supplier_company', 'desc')
    search_fields = ['name', 'desc']


@admin.register(TankState)
class TankStateAdmin(admin.ModelAdmin):
    list_display = ('pk', 'tank_state_en', 'tank_state_cn', 'with_product')


@admin.register(Tank)
class TankAdmin(admin.ModelAdmin):
    list_display = ('tank_code', 'tank_name', 'tank_state', 'tank_standard_volume',
                    'current_brew_code', 'notes', 'tank_info_updated')
    list_filter = ('tank_standard_volume', 'tank_state',)
    search_fields = ['tank_name', 'tank_code', 'notes', 'current_brew_code']


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'place_code', 'place_desc')


admin.site.register(MoneyInOutType)


@admin.register(MoneyInOut)
class MoneyInOutAdmin(admin.ModelAdmin):
    list_display = ('datetime_created', 'money_in_out', 'money_in_out_type', 'notes', 'recorded_by', 'confirmed_by',
                    'datetime_updated')
    list_filter = ('money_in_out_type', 'recorded_by', 'is_confirmed', 'is_active')
    search_fields = ['notes', ]


@admin.register(MaterialCategory)
class MaterialCategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'material_category_code', 'material_category_en', 'material_category_cn',)
    search_fields = ['material_category_code', 'material_category_en', 'material_category_cn']


@admin.register(MaterialPackSizeUnit)
class MaterialPackSizeUnitCategoryAdmin(admin.ModelAdmin):
    list_display = ('material_pack_size', 'material_pack_unit')
    list_filter = ('material_pack_size', 'material_pack_unit',)
    search_fields = ['material_pack_size', 'material_pack_unit']


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('material_code', 'material_en', 'material_cn', 'material_category', 'notes',
                    'account_code', 'datetime_updated')
    list_filter = ('material_category',)
    search_fields = ['material_code', 'material_en', 'material_cn', 'notes']


@admin.register(MaterialBatch)
class MaterialBatchAdmin(admin.ModelAdmin):
    list_display = ('material_batch_code', 'material', 'material_pack_size_unit', 'expire_date',
                    'para', 'datetime_updated', 'notes', 'state')
    list_filter = ('material_pack_size_unit', 'material')
    search_fields = ['material_batch_code', 'notes', 'para']


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product_type_code', 'product_type_name_cn', 'product_type_name_en', 'is_show')


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('product_category_cn', 'product_category_en', 'product_category_desc_cn',
                    'product_category_desc_en', 'is_show', 'datetime_created', 'datetime_updated')
    search_fields = ['product_category_cn', 'product_category_en',
                     'product_category_desc_cn', 'product_category_desc_en']


@admin.register(ProductName)
class ProductNameAdmin(admin.ModelAdmin):
    list_display = ('product_name_code', 'product_name_cn', 'product_name_en', 'brewer', 'client',
                    'current_recipe', 'product_type', 'notes', 'is_show', 'datetime_updated')
    list_filter = ('brewer', 'client', 'product_type')
    search_fields = ['product_name_code', 'product_name_cn', 'product_name_en',
                     'product_name_cn_pre', 'product_name_en_pre', 'notes']


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe_code', 'recipe_name', 'datetime_created', 'datetime_updated')


@admin.register(Brew)
class BrewAdmin(admin.ModelAdmin):
    list_display = ('brew_batch_code', 'product_name', 'recipe', 'tank', 'date_start', 'operator', 'notes')
    list_filter = ('tank', 'product_name')
    search_fields = ['brew_batch_code', 'notes']


@admin.register(BrewMonitor)
class BrewMonitorAdmin(admin.ModelAdmin):
    list_display = ('brew_monitor_code', 'brew', 'brew_date', 'og_wort',
                    'ph_mash_1', 'malt_add_start', 'enter_fermenter_start')
    list_filter = ('brewer',)
    search_fields = ['brew_monitor_code']


@admin.register(FermentMonitor)
class FermentMonitorAdmin(admin.ModelAdmin):
    list_display = ('brew', 'sg', 'plato', 'ph', 't_real', 't_set', 'bar', 'notes', '_delta_days', '_qc_report')
    list_filter = ('brew',)
    search_fields = ['brew__brew_batch_code', 'notes']

    @mark_safe
    def _qc_report(self, obj):
        if obj.qc_report:
            return '<a href="{0}{1}">{0}{1}</a>'.format(settings.MEDIA_URL, obj.qc_report.name)
        return None

    _qc_report.short_description = _('质检报告')

    @mark_safe
    def _delta_days(self, obj):
        if obj.delta_days:
            return obj.delta_days
        return None

    _delta_days.short_description = _('入罐天数 ')


@admin.register(ProductPackSizeUnit)
class ProductPackSizeUnitAdmin(admin.ModelAdmin):
    list_display = ('product_pack_code', 'product_pack_size', 'product_pack_unit', 'product_pack_type_en',
                    'product_pack_type_cn', 'datetime_updated')
    list_filter = ('product_pack_size',)
    search_fields = ['product_pack_code', 'product_pack_size', 'product_pack_unit',
                     'product_pack_type_en', 'product_pack_type_cn']


@admin.register(ProductStyle)
class ProductStyleAdmin(admin.ModelAdmin):
    list_display = ('product_style_cn', 'product_style_en', 'product_style_desc_cn', 'product_style_desc_en',
                    'datetime_created', 'datetime_updated')
    search_fields = ['product_style_cn', 'product_style_en', 'product_style_desc_cn', 'product_style_desc_en']


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    fieldsets = (
        (_('文件'), {'fields': ('_logo_url', '_image_url', '_image_banner_url', '_files_url')}),
        (_('基础数据'), {'fields': [
            'index', 'product_code', ('product_name', 'product_pack'),
            ('logo', 'image'), ('image_banner', 'files')
        ]}),
        (_('归类信息'), {'fields': (('product_category', 'product_style'),)}),
        (_('参数信息'), {'fields': (('abv', 'plato', 'ibu'), 'barcode')}),
        (_('价格信息'), {'fields': ('supplier_price', 'bar_price', 'public_price')}),
        (_('More'), {'fields': ('is_show', 'is_banner', 'created_by')}),
    )
    readonly_fields = ['_logo_url', '_image_url', '_image_banner_url', '_files_url']
    list_display = ('pk', 'product_code', 'product_name', 'is_show', 'is_banner', 'supplier_price', 'bar_price',
                    'public_price')
    search_fields = ['product_code', 'product_name']
    list_filter = ('is_show', 'is_banner')

    @mark_safe
    def _logo_url(self, obj):
        if obj.logo:
            return '<a href="{0}{1}">{0}{1}</a>'.format(settings.MEDIA_URL, obj.logo.name)
        return None

    _logo_url.short_description = _('logo')

    @mark_safe
    def _image_url(self, obj):
        if obj.image:
            return '<a href="{0}{1}">{0}{1}</a>'.format(settings.MEDIA_URL, obj.image.name)
        return None

    _image_url.short_description = _('图片')

    @mark_safe
    def _image_banner_url(self, obj):
        if obj.image_banner:
            return '<a href="{0}{1}">{0}{1}</a>'.format(settings.MEDIA_URL, obj.image_banner.name)
        return None

    _image_banner_url.short_description = _('Banner图片')

    @mark_safe
    def _files_url(self, obj):
        if obj.files:
            return '<a href="{0}{1}">{0}{1}</a>'.format(settings.MEDIA_URL, obj.files.name)
        return None

    _files_url.short_description = _('资料')


@admin.register(MaterialIn)
class MaterialInAdmin(admin.ModelAdmin):
    list_display = ('material_batch', 'warehouse', 'amount', 'recorder', 'notes', 'is_confirmed')
    list_filter = ('warehouse', 'is_confirmed')
    search_fields = ['notes', ]


@admin.register(MaterialOut)
class MaterialOutAdmin(admin.ModelAdmin):
    list_display = ('material_batch', 'brew', 'amount', 'recorder', 'notes', 'confirmed', 'checked')
    list_filter = ('brew', 'confirmed', 'checked')
    search_fields = ['notes', ]


@admin.register(Pack)
class PackAdmin(admin.ModelAdmin):
    list_display = ('pack_batch_code', 'brew', 'product', 'pack_date', 'pack_num', 'confirmed', 'datetime_updated')
    list_filter = ('product', 'employee', 'confirmed')
    search_fields = ['notes', ]


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_code', 'pack', 'report_date', 'employee', 'ebc', 'foam', 'abv', 'plato', 'total_acid',
                    'co2', 'diacetyl', 'notes', 'is_active', 'is_confirmed', 'datetime_updated')
    list_filter = ('employee', 'is_active', 'is_confirmed')
    search_fields = ['notes', ]


@admin.register(ClientAddress)
class ClientAddressAdmin(admin.ModelAdmin):
    list_display = ('client', 'province_name', 'city_name', 'county_name', 'detail_info', 'user_name', 'tel_number')
    search_fields = ['detail_info', 'user_name']


@admin.register(OrderState)
class OrderStateAdmin(admin.ModelAdmin):
    list_display = ('order_state_cn', 'order_state_en')


@admin.register(SaleOrder)
class SaleOrderAdmin(admin.ModelAdmin):
    list_display = ('sale_order_code', 'sale_order_date', 'order_state', 'employee', 'client',
                    'created_by', 'notes', 'is_active', 'datetime_created', 'datetime_updated')
    list_filter = ('order_state', 'employee', 'client', 'is_active')
    search_fields = ['notes', ]


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('sale_order', 'pack', 'sale_num', 'sale_price', 'notes', 'is_sale', 'is_active', 'is_confirmed',
                    'fee_received', 'datetime_created', 'datetime_updated')
    list_filter = ('sale_order', 'pack', 'is_sale', 'is_active', 'is_confirmed', 'fee_received')
    search_fields = ['notes', ]


@admin.register(HandBook)
class HandBookAdmin(admin.ModelAdmin):
    list_display = ('chapter', 'chapter_code', 'chapter_name_cn', 'chapter_name_en',
                    'datetime_created', 'datetime_updated')
