from django.db import models
from django.db.models import Sum, Count, Q
from django.contrib import admin
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from .storage import ImageStorage
from .apps import GeneralConfig
from django.utils import timezone
from django.contrib.auth.models import User
import hashlib

app_name = GeneralConfig.name


class BankAccount(models.Model):
    bank = models.CharField(_('银行'), max_length=200, null=True, blank=True)
    account_owner = models.CharField(_('账户名'), max_length=200, null=True, blank=True)
    bank_account = models.CharField(_('银行卡号'), max_length=50, null=True, blank=True)
    bank_address = models.CharField(_('银行地址'), max_length=400, null=True, blank=True)
    desc = models.TextField(_('备注'), max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(_('可用'), default=True)

    objects = models.Manager()

    class Meta:
        ordering = ['id']
        verbose_name = _('收款帐号')
        verbose_name_plural = _('收款帐号')

    def __str__(self):
        return '{0} {1}'.format(self.bank, self.bank_account)


@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('bank_account', 'bank', 'bank_address', 'desc')
    search_fields = ['bank_account']


class EmployeeState(models.Model):
    employee_state_cn = models.CharField(_('员工状态-中文'), max_length=100, null=True, unique=True)
    employee_state_en = models.CharField(_('员工状态-英文'), max_length=100, null=True, unique=True, blank=True)

    objects = models.Manager()

    def get_absolute_url(self):
        if self.pk:
            pass
        return reverse('{0}:employee_state_list'.format(app_name))

    class Meta:
        ordering = ['id']
        verbose_name = _('员工状态')
        verbose_name_plural = _('员工状态')

    def __str__(self):
        return '{0}'.format(self.employee_state_cn)


@admin.register(EmployeeState)
class EmployeeStateAdmin(admin.ModelAdmin):
    list_display = ('pk', 'employee_state_cn', 'employee_state_en')


class Employee(models.Model):
    first_name = models.CharField(_('名字'), max_length=30)
    last_name = models.CharField(_('姓氏'), max_length=50)
    email = models.EmailField(_('邮箱'), null=True, blank=True)
    birth = models.DateField(_('生日'), null=True, blank=True)
    mobile = models.CharField(_('电话'), max_length=100, null=True)
    wechat = models.CharField(_('微信'), max_length=100, null=True, blank=True)
    desc = models.TextField(_('介绍'), max_length=1000, null=True, blank=True)
    gender = models.CharField(_('性别'), choices=(('0', '未知'), ('1', '男'), ('2', '女')), max_length=10,
                              null=True, blank=True)
    title = models.CharField(_('头衔'), max_length=100, null=True, blank=True)
    department = models.CharField(_('部门'), max_length=100, null=True, blank=True)
    employee_state = models.ForeignKey(
        EmployeeState,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name=_('员工状态')
    )
    is_brewer = models.BooleanField(_('是酿酒师'), default=False)
    is_salesman = models.BooleanField(_('是销售员'), default=False)
    working = models.BooleanField(_('在职'), default=True)
    joined = models.DateField(_('加入日期'), null=True, blank=True)
    created_by = models.IntegerField(_('创建人'), null=True, blank=True)
    linked_account = models.IntegerField(_('关联账号'), null=True, blank=True, unique=True)
    datetime_created = models.DateTimeField(_('添加时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    def get_absolute_url(self):
        if self.pk:
            pass
        return reverse('{0}:employee_list'.format(app_name))

    def name_cn(self):
        if self.first_name and self.last_name:
            return '{0}{1}'.format(self.last_name, self.first_name)
        return 'N/A'

    def linked_account_info(self):
        linked_account_info = None
        if self.linked_account:
            linked_account_info = User.objects.filter(pk=self.linked_account)
            if linked_account_info.exists():
                linked_account_info = linked_account_info.first()
            else:
                linked_account_info = None
        return linked_account_info

    class Meta:
        ordering = ['id']
        verbose_name = _('员工')
        verbose_name_plural = _('员工')

    def __str__(self):
        return '{0}{1}'.format(self.last_name, self.first_name)


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email', 'mobile', 'wechat', 'title', 'is_brewer', 'is_salesman',
                    'datetime_created', 'datetime_updated')
    list_filter = ('is_brewer', 'is_salesman')
    search_fields = ['first_name', 'last_name']


class CompanyType(models.Model):
    company_type_en = models.CharField(_('公司类型英文'), max_length=100, null=True, unique=True, blank=True)
    company_type_cn = models.CharField(_('公司类型中文'), max_length=100, null=True, unique=True)

    objects = models.Manager()

    def get_absolute_url(self):
        if self.pk:
            pass
        return reverse('{0}:company_type_list'.format(app_name))

    class Meta:
        ordering = ['id']
        verbose_name = _('公司类型')
        verbose_name_plural = _('公司类型')

    def __str__(self):
        return '{0}'.format(self.company_type_cn)


@admin.register(CompanyType)
class CompanyTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'company_type_en', 'company_type_cn')


class Company(models.Model):
    company_name_en = models.CharField(_('公司英文名'), max_length=100, unique=True, null=True, blank=True)
    company_name_cn = models.CharField(_('公司中文名'), max_length=100, unique=True, null=True, blank=True)
    company_address = models.CharField(_('公司地址'), max_length=200, null=True, blank=True)
    china_district = models.CharField(_('地区编号'), max_length=100, null=True, blank=True)
    company_tel = models.CharField(_('公司电话'), max_length=100, null=True, blank=True)
    email = models.EmailField(_('公司邮箱'), max_length=100, null=True, blank=True)
    tax_code = models.CharField(_('税号'), max_length=100, null=True, blank=True)
    bank = models.CharField(_('银行'), max_length=200, null=True, blank=True)
    bank_account = models.CharField(_('银行卡号'), max_length=50, null=True, blank=True)
    desc = models.TextField(_('公司介绍'), max_length=1000, null=True, blank=True)
    company_type = models.ForeignKey(
        CompanyType,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('公司类型')
    )
    company_share = models.BooleanField(_('是否共享'), default=False)
    created_by = models.IntegerField(_('创建人'), null=True, blank=True)
    datetime_created = models.DateTimeField(_('添加时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    def get_absolute_url(self):
        if self.pk:
            pass
        return reverse('{0}:company_list'.format(app_name))

    class Meta:
        ordering = ['id']
        verbose_name = _('公司')
        verbose_name_plural = _('公司')

    def __str__(self):
        return '{0} {1}'.format(self.company_name_cn, self.company_name_en)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('pk', 'company_name_cn', 'company_name_en', 'email', 'company_tel', 'company_type', 'desc')
    list_filter = ('company_type',)
    search_fields = ['company_name_cn', 'company_name_en']


class ClientLevel(models.Model):
    level_code = models.SmallIntegerField(_('等级编号'), null=True, unique=True, blank=True)
    level_cn = models.CharField(_('中文级别'), max_length=100, null=True, unique=True)
    level_en = models.CharField(_('英文级别'), max_length=100, null=True, blank=True)
    level_desc_cn = models.TextField(_('中文级别描述'), max_length=1000, null=True, blank=True)
    level_desc_en = models.TextField(_('英文级别描述'), max_length=1000, null=True, blank=True)
    datetime_created = models.DateTimeField(_('记录时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    def get_absolute_url(self):
        if self.pk:
            pass
        return reverse('{0}:client_level_list'.format(app_name))

    class Meta:
        ordering = ['id']
        verbose_name = _('客户级别')
        verbose_name_plural = _('客户级别')

    def __str__(self):
        return "{0}".format(self.level_cn)


@admin.register(ClientLevel)
class ClientLevelAdmin(admin.ModelAdmin):
    list_display = ('level_code', 'level_cn', 'level_en')


class Client(models.Model):
    name = models.CharField(_('姓名'), max_length=100, null=True)
    gender = models.CharField(_('性别'), choices=(('0', '未知'), ('1', '男'), ('2', '女')), max_length=10,
                              null=True, blank=True)
    mobile = models.CharField(_('手机'), max_length=100, null=True, blank=True)
    wechat = models.CharField(_('微信'), max_length=100, null=True, blank=True)
    email = models.EmailField(_('邮箱'), max_length=100, null=True, blank=True)
    client_company = models.ForeignKey(
        Company,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('所属公司')
    )
    desc = models.TextField(_('介绍'), max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(_('有效客户'), default=True)
    created_by = models.IntegerField(_('创建人'), null=True, blank=True)
    openid = models.CharField(max_length=100, unique=True, null=True, blank=True)
    avatar = models.URLField(_('头像'), null=True, blank=True)
    nickname = models.CharField(_('昵称'), max_length=100, null=True, blank=True, unique=True)
    language = models.CharField(_('语言'), max_length=100, null=True, blank=True)
    city = models.CharField(_('城市'), max_length=200, null=True, blank=True)
    province = models.CharField(_('省份'), max_length=200, null=True, blank=True)
    country = models.CharField(_('国家'), max_length=200, null=True, blank=True)
    date_of_birth = models.DateField(_('出生日期'), null=True, blank=True)
    client_level = models.ForeignKey(
        ClientLevel,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('客户级别'),
    )
    current_address_id = models.IntegerField(_('当前地址id'), null=True, blank=True)
    datetime_created = models.DateTimeField(_('记录时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('{0}:client_detail'.format(app_name), kwargs={'pk': str(self.pk)})

    class Meta:
        ordering = ['id']
        verbose_name = _('客户')
        verbose_name_plural = _('客户')

    def __str__(self):
        return '{0} {1}'.format(self.name, self.client_company)


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'mobile', 'wechat', 'client_company', 'is_active')
    search_fields = ['name', 'desc']


class Supplier(models.Model):
    name = models.CharField(_('姓名'), max_length=100)
    gender = models.CharField(_('性别'), choices=(('0', '未知'), ('1', '男'), ('2', '女')), max_length=10,
                              null=True, blank=True)
    mobile = models.CharField(_('手机'), max_length=100, null=True, blank=True)
    wechat = models.CharField(_('微信'), max_length=100, null=True, blank=True)
    email = models.EmailField(_('邮箱'), max_length=100, null=True, blank=True)
    supplier_company = models.ForeignKey(
        Company,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('所属公司')
    )
    desc = models.TextField(_('介绍'), max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(_('交往中'), default=True)
    created_by = models.IntegerField(_('创建人'), null=True, blank=True)
    datetime_created = models.DateTimeField(_('添加时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    def get_absolute_url(self):
        return reverse('{0}:supplier_detail'.format(app_name), kwargs={'pk': str(self.pk)})

    class Meta:
        ordering = ['id']
        verbose_name = _('供应商')
        verbose_name_plural = _('供应商')

    def __str__(self):
        return '{0} {1}'.format(self.name, self.supplier_company)


@admin.register(Supplier)
class SupplierAdmin(admin.ModelAdmin):
    list_display = ('name', 'mobile', 'wechat', 'supplier_company', 'desc')
    search_fields = ['name', 'desc']


class TankState(models.Model):
    tank_state_en = models.CharField(_('发酵罐状态英文'), max_length=200, null=True, blank=True)
    tank_state_cn = models.CharField(_('发酵罐状态中文'), max_length=200, null=True)
    with_product = models.BooleanField(_('是否生产'), default=True)

    objects = models.Manager()

    class Meta:
        ordering = ['id']
        verbose_name = _('发酵罐状态')
        verbose_name_plural = _('发酵罐状态')

    def __str__(self):
        return "{0}".format(self.tank_state_cn)


@admin.register(TankState)
class TankStateAdmin(admin.ModelAdmin):
    list_display = ('pk', 'tank_state_en', 'tank_state_cn', 'with_product')


class Tank(models.Model):
    tank_code = models.CharField(_('发酵罐编号 '), max_length=30, unique=True)
    tank_name = models.CharField(_('发酵罐名'), max_length=100, null=True)
    tank_state = models.ForeignKey(
        TankState,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('发酵罐状态')
    )
    tank_standard_volume = models.CharField(_('发酵罐容量'), max_length=100, null=True)
    volume_init = models.PositiveIntegerField(_('起始容量'), default=0, null=True, blank=True)
    volume_left = models.PositiveSmallIntegerField(_('剩余容量'), default=0, null=True, blank=True)
    # tem_s = models.DecimalField(max_digits=3, decimal_places=1, null=True)
    # jkm_tank_id = models.CharField(max_length=30, unique=True, null=True)
    # jkm_plc_id = models.SmallIntegerField(null=True)
    # jkm_n_type = models.SmallIntegerField(null=True)
    # jkm_t_no = models.SmallIntegerField(null=True)
    jkm_t_real = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    jkm_t_set = models.DecimalField(max_digits=3, decimal_places=1, null=True, blank=True)
    jkm_updated = models.DateTimeField(_('温度更新于'), null=True, blank=True)
    tank_info_updated = models.DateTimeField(_('更新于'), auto_now=True)
    current_brew_code = models.CharField(_('当前批次'), max_length=30, null=True, blank=True)
    # current_product_info = models.CharField(_('当前产品信息'), max_length=100, null=True)
    notes = models.TextField(_('备注'), max_length=1000, null=True, blank=True)
    datetime_created = models.DateTimeField(_('添加时间'), auto_now_add=True)

    objects = models.Manager()

    @property
    def current_brew(self):
        if Brew:
            brew = Brew.objects.get(brew_batch_code=self.current_brew_code)
            if brew:
                return brew
        return None

    class Meta:
        ordering = ['id']
        verbose_name = _('发酵罐')
        verbose_name_plural = _('发酵罐')

    def __str__(self):
        return "{0} {1}".format(self.tank_name, self.tank_state)


@admin.register(Tank)
class TankAdmin(admin.ModelAdmin):
    list_display = ('tank_code', 'tank_name', 'tank_state', 'tank_standard_volume',
                    'current_brew_code', 'notes', 'tank_info_updated')
    list_filter = ('tank_standard_volume', 'tank_state',)
    search_fields = ['tank_name', 'tank_code', 'notes', 'current_brew_code']


class TankSateUpdate(models.Model):
    tank = models.ForeignKey(
        Tank,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('设备编号')
    )
    tank_state_pre = models.IntegerField(_('更改前状态'), null=True, blank=True)
    tank_state_now = models.ForeignKey(
        TankState,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('状态更改为')
    )
    tank_state_updated = models.DateTimeField(_('更改时间'), auto_now_add=True)
    created_by = models.IntegerField(_('操作人员'), null=True, blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = _('发酵罐状态更新')
        verbose_name_plural = _('发酵罐状态更新')

    def __str__(self):
        return "{0} {1} {2} {3}".format(self.tank_state_updated, self.tank, self.tank_state_pre, self.tank_state_now)


class Warehouse(models.Model):
    place_code = models.CharField(_('位置编号'), max_length=10, null=True, unique=True)
    place_desc = models.CharField(_('位置描述'), max_length=200, null=True, unique=True)

    objects = models.Manager()

    class Meta:
        verbose_name = _('存储位置')
        verbose_name_plural = _('存储位置')

    def get_absolute_url(self):
        if self.pk:
            pass
        return reverse('{0}:warehouse_list'.format(app_name))

    def __str__(self):
        return "{0} {1}".format(self.place_code, self.place_desc)


@admin.register(Warehouse)
class WarehouseAdmin(admin.ModelAdmin):
    list_display = ('pk', 'place_code', 'place_desc')


class MoneyInOutType(models.Model):
    money_in_out_type_cn = models.CharField(_('收支类型中文'), max_length=200, null=True, unique=True)
    money_in_out_type_en = models.CharField(_('收支类型英文'), max_length=200, null=True, blank=True)
    is_negative = models.BooleanField(_('是否为支出'), default=True)
    is_auto = models.BooleanField(_('自动记录'), default=False)

    objects = models.Manager()

    def get_absolute_url(self):
        if self.pk:
            pass
        return reverse('{0}:money_inout_types'.format(app_name))

    class Meta:
        ordering = ['id']
        verbose_name = _('收支类型')
        verbose_name_plural = _('收支类型')

    def __str__(self):
        return '{0}'.format(self.money_in_out_type_cn)


admin.site.register(MoneyInOutType)


class MoneyInOut(models.Model):
    money_in_out = models.DecimalField(_('金额'), max_digits=12, decimal_places=2, null=True)
    money_in_out_date = models.DateField(_('日期'), null=True)
    money_in_out_type = models.ForeignKey(
        MoneyInOutType,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('收支类型')
    )
    notes = models.TextField(_('备注'), max_length=1000, null=True, blank=True)
    recorded_by = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('经手人'),
    )
    created_by = models.IntegerField(_('创建人员'), null=True, blank=True)
    confirmed_by = models.IntegerField(_('确认人员'), null=True, blank=True)
    is_confirmed = models.BooleanField(_('确认到账'), default=False)
    is_active = models.BooleanField(_('记录有效'), default=True)
    datetime_created = models.DateTimeField(_('添加时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    def get_absolute_url(self):
        if self.pk:
            pass
        return reverse('{0}:moneyinout_list'.format(app_name))

    @property
    def money_left_before(self):
        m_s = MoneyInOut.objects.filter(pk__lte=self.pk).aggregate(money_left_b=Sum('money_in_out'))
        if m_s:
            return m_s['money_left_b']
        else:
            return None

    @property
    def linked_sale(self):
        linked_sale = Sale.objects.filter(sale_price_link_id=self.pk)
        if linked_sale.exists():
            return linked_sale.first()
        return None

    class Meta:
        ordering = ['-id']
        verbose_name = _('资金流水')
        verbose_name_plural = _('资金流水')
        permissions = (
            ("confirm_moneyinout", _("可以确认资金到账")),
        )

    def __str__(self):
        return '{0} 元'.format(self.money_in_out)


@admin.register(MoneyInOut)
class MoneyInOutAdmin(admin.ModelAdmin):
    list_display = ('datetime_created', 'money_in_out', 'money_in_out_type', 'notes', 'recorded_by', 'confirmed_by',
                    'datetime_updated')
    list_filter = ('money_in_out_type', 'recorded_by', 'is_confirmed', 'is_active')
    search_fields = ['notes', ]


class MaterialCategory(models.Model):
    material_category_code = models.CharField(_('原料分类编号'), max_length=10, null=True, unique=True)
    material_category_en = models.CharField(_('原料分类英文名'), max_length=100, null=True, unique=True, blank=True)
    material_category_cn = models.CharField(_('原料分类中文名'), max_length=100, null=True, unique=True)

    objects = models.Manager()

    class Meta:
        ordering = ['id']
        verbose_name = _('原料分类')
        verbose_name_plural = _('原料分类')

    def __str__(self):
        return "{0} {1}".format(
            self.material_category_code,
            self.material_category_cn,
        )


@admin.register(MaterialCategory)
class MaterialCategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'material_category_code', 'material_category_en', 'material_category_cn',)
    search_fields = ['material_category_code', 'material_category_en', 'material_category_cn']


class MaterialPackSizeUnit(models.Model):
    material_pack_size = models.DecimalField(_('包装规格'), max_digits=9, decimal_places=3, null=True)
    material_pack_unit = models.CharField(_('包装单位'), max_length=100, null=True,
                                          choices=(('g', 'g'), ('kg', 'kg'), ('mL', 'mL'), ('L', 'L')))

    objects = models.Manager()

    def get_absolute_url(self):
        if self.pk:
            pass
        return reverse('{0}:material_pack_list'.format(app_name))

    class Meta:
        ordering = ['id']
        verbose_name = _('原料包装')
        verbose_name_plural = _('原料包装')

    def __str__(self):
        return "{0} {1}".format(str(self.material_pack_size).rstrip('0').rstrip('.'), self.material_pack_unit)


@admin.register(MaterialPackSizeUnit)
class MaterialPackSizeUnitCategoryAdmin(admin.ModelAdmin):
    list_display = ('material_pack_size', 'material_pack_unit')
    list_filter = ('material_pack_size', 'material_pack_unit',)
    search_fields = ['material_pack_size', 'material_pack_unit']


class Material(models.Model):
    material_code = models.CharField(_('原料编号'), max_length=100, null=True, unique=True, blank=True)
    material_en = models.CharField(_('原料英文名'), max_length=200, null=True, blank=True)
    material_cn = models.CharField(_('原料中文名'), max_length=200, null=True, unique=True)
    material_category = models.ForeignKey(
        MaterialCategory,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('原料分类')
    )
    notes = models.TextField(_('备注'), max_length=1000, null=True, blank=True)
    account_code = models.CharField(_('财务编号'), max_length=100, null=True, blank=True)
    shared_material = models.IntegerField(_('导入于'), null=True, blank=True)
    created_by = models.IntegerField(_('创建人'), null=True, blank=True)
    datetime_created = models.DateTimeField(_('添加时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    def get_absolute_url(self):
        if self.pk:
            pass
        return reverse('{0}:material_list'.format(app_name))

    class Meta:
        ordering = ['id']
        verbose_name = _('原料')
        verbose_name_plural = _('原料')

    def __str__(self):
        return '[{0}] {1}'.format(self.material_code, self.material_cn)


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('material_code', 'material_en', 'material_cn', 'material_category', 'notes',
                    'account_code', 'datetime_updated')
    list_filter = ('material_category',)
    search_fields = ['material_code', 'material_en', 'material_cn', 'notes']


class MaterialBatch(models.Model):
    material_batch_code = models.CharField(_('批号'), max_length=100, unique=True, null=True)
    material = models.ForeignKey(
        Material,
        on_delete=models.CASCADE,
        verbose_name=_('原料')
    )
    material_pack_size_unit = models.ForeignKey(
        MaterialPackSizeUnit,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('包装规格')
    )
    expire_date = models.DateField(_('保质期'), null=True)
    para = models.CharField(_('参数'), max_length=100, null=True, blank=True)
    notes = models.TextField(_('备注'), max_length=1000, null=True, blank=True)
    state = models.BooleanField(_('状态'), default=True)
    created_by = models.IntegerField(_('创建人'), null=True, blank=True)
    datetime_created = models.DateTimeField(_('添加时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    @property
    def material_batch_total_in(self):
        _('入库总量')
        if MaterialIn:
            material_batch_in_sum = MaterialIn.objects.filter(material_batch_id=self.pk).aggregate(Sum("amount"))
            if material_batch_in_sum:
                if material_batch_in_sum['amount__sum']:
                    return material_batch_in_sum['amount__sum']
        return 0

    @property
    def material_batch_total_out(self):
        _('出库总量')
        if MaterialOut:
            material_batch_out_sum = MaterialOut.objects.filter(material_batch_id=self.pk).aggregate(Sum("amount"))
            if material_batch_out_sum:
                if material_batch_out_sum['amount__sum']:
                    return material_batch_out_sum['amount__sum']
        return 0

    @property
    def material_batch_total_left(self):
        if self.material_batch_total_in or self.material_batch_total_out:
            if self.material_batch_total_out:
                return self.material_batch_total_in - self.material_batch_total_out
            return self.material_batch_total_in
        return 0

    @property
    def material_cost_each(self):
        cost_each = None
        total_price = MaterialIn.objects.filter(material_batch_id=self.pk).aggregate(
            total_price=Sum("material_cost_link__money_in_out"))
        if total_price:
            if total_price['total_price'] and self.material_batch_total_in:
                cost_each = float(total_price['total_price']) / float(self.material_batch_total_in)
        return cost_each

    def get_absolute_url(self):
        if self.pk:
            pass
        return reverse('{0}:material_batch_list'.format(app_name))

    class Meta:
        ordering = ['-id']
        verbose_name = _('原料批次')
        verbose_name_plural = _('原料批次')

    def __str__(self):
        return '[{0}] {1} ({2}) 剩余:{3}'.format(
            self.material_batch_code,
            self.material,
            self.material_pack_size_unit,
            str(self.material_batch_total_left).rstrip('0').rstrip('.'),
        )


@admin.register(MaterialBatch)
class MaterialBatchAdmin(admin.ModelAdmin):
    list_display = ('material_batch_code', 'material', 'material_pack_size_unit', 'expire_date',
                    'para', 'datetime_updated', 'notes', 'state')
    list_filter = ('material_pack_size_unit', 'material')
    search_fields = ['material_batch_code', 'notes', 'para']


class ProductType(models.Model):
    product_type_code = models.CharField(_('类型编号'), max_length=10, unique=True)
    product_type_name_cn = models.CharField(_('类型中文名'), max_length=100, unique=True)
    product_type_name_en = models.CharField(_('类型英文名'), max_length=100, unique=True)
    is_show = models.BooleanField(_('类型显示'), default=False)

    objects = models.Manager()

    class Meta:
        ordering = ['id']
        verbose_name = _('产品类型')
        verbose_name_plural = _('产品类型')

    def __str__(self):
        return "{0}".format(self.product_type_name_cn)


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product_type_code', 'product_type_name_cn', 'product_type_name_en', 'is_show')


class ProductCategory(models.Model):
    product_category_cn = models.CharField(_('归类中文'), max_length=200, null=True, unique=True)
    product_category_en = models.CharField(_('归类英文'), max_length=200, null=True, blank=True)
    product_category_desc_cn = models.TextField(_('中文介绍'), max_length=2000, null=True, blank=True)
    product_category_desc_en = models.TextField(_('英文介绍'), max_length=2000, null=True, blank=True)
    is_show = models.BooleanField(_('是否显示'), default=True)
    datetime_created = models.DateTimeField(_('记录时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    def get_absolute_url(self):
        if self.pk:
            pass
        return reverse('{0}:product_category_list'.format(app_name))

    @property
    def product_amount(self):
        _('产品数量')
        if Product:
            amount = Product.objects.filter(product_category__id__exact=self.pk).count()
            return amount
        return 0

    class Meta:
        ordering = ['id']
        verbose_name = _('产品归类')
        verbose_name_plural = _('产品归类')

    def __str__(self):
        return '{0}'.format(self.product_category_cn)


@admin.register(ProductCategory)
class ProductCategoryAdmin(admin.ModelAdmin):
    list_display = ('product_category_cn', 'product_category_en', 'product_category_desc_cn',
                    'product_category_desc_en', 'is_show', 'datetime_created', 'datetime_updated')
    search_fields = ['product_category_cn', 'product_category_en',
                     'product_category_desc_cn', 'product_category_desc_en']


class ProductName(models.Model):
    product_name_code = models.CharField(_('名称编号'), max_length=30, unique=True, null=True)
    product_name_cn = models.CharField(_('产品中文名'), max_length=200, unique=True, null=True)
    product_name_cn_pre = models.CharField(_('产品中文名-曾用名'), max_length=200, null=True, blank=True)
    product_name_en = models.CharField(_('产品英文名'), max_length=200, null=True, blank=True)
    product_name_en_pre = models.CharField(_('产品英文名-曾用名'), max_length=200, null=True, blank=True)
    brewer = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('酿酒师'),
        limit_choices_to={'is_brewer': True},
    )
    client = models.ForeignKey(
        Client,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('关联客户')
    )
    current_recipe = models.IntegerField(_('当前配方编号'), null=True, blank=True)
    desc_en = models.TextField(_('英文介绍'), max_length=4000, null=True, blank=True)
    desc_cn = models.TextField(_('中文介绍'), max_length=4000, null=True, blank=True)
    notes = models.TextField(_('备注'), max_length=1000, null=True, blank=True)
    product_type = models.ForeignKey(
        ProductType,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('产品类型')
    )
    is_show = models.BooleanField(_('是否显示'), default=True)
    created_by = models.IntegerField(_('创建人'), null=True, blank=True)
    datetime_created = models.DateTimeField(_('创建时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    def get_absolute_url(self):
        if self.pk:
            pass
        return reverse('{0}:product_name_list'.format(app_name))

    class Meta:
        ordering = ['id']
        verbose_name = _('产品名称')
        verbose_name_plural = _('产品名称')

    def __str__(self):
        return "[{0}] {1}".format(self.product_name_code, self.product_name_cn)


@admin.register(ProductName)
class ProductNameAdmin(admin.ModelAdmin):
    list_display = ('product_name_code', 'product_name_cn', 'product_name_en', 'brewer', 'client',
                    'current_recipe', 'product_type', 'notes', 'is_show', 'datetime_updated')
    list_filter = ('brewer', 'client', 'product_type')
    search_fields = ['product_name_code', 'product_name_cn', 'product_name_en',
                     'product_name_cn_pre', 'product_name_en_pre', 'notes']


class Recipe(models.Model):
    recipe_code = models.CharField(_('配方编号'), max_length=50, unique=True, null=True)
    recipe_name = models.CharField(_('配方名称'), max_length=50, null=True, blank=True)
    recipe_product_name = models.ForeignKey(
        ProductName,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('产品名称')
    )
    brewer = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('酿酒师'),
        limit_choices_to={'is_salesman': True},
    )
    materials = models.TextField(_('原材料'), max_length=1000, null=True)
    mashing = models.TextField(_('糖化工艺'), max_length=1000, null=True)
    fermentation = models.TextField(_('发酵工艺'), max_length=1000, null=True)
    yeast = models.CharField(_('酵母'), max_length=50, null=True, blank=True)
    og = models.DecimalField(_('原麦汁度'), max_digits=4, decimal_places=3, null=True)
    abv = models.DecimalField(_('酒精度'), max_digits=4, decimal_places=2, null=True)
    ibu = models.DecimalField(_('苦度'), max_digits=4, decimal_places=1, null=True)
    notes = models.TextField(_('备注'), max_length=1000, null=True)
    style = models.CharField(_('风格'), max_length=50, null=True, blank=True)
    related_recipes = models.ManyToManyField('self', verbose_name='关联配方')
    current_use = models.BooleanField(_('正在使用'), default=True)
    created_by = models.IntegerField(_('创建人'), null=True, blank=True)
    datetime_created = models.DateTimeField(_('创建时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    class Meta:
        ordering = ['id']
        verbose_name = _('配方')
        verbose_name_plural = _('配方')

    def __str__(self):
        return '{0} {1}'.format(self.recipe_code, self.recipe_name)


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe_code', 'recipe_name', 'datetime_created', 'datetime_updated')


class Brew(models.Model):
    brew_batch_code = models.CharField(_('酿造批次'), max_length=30, unique=True, null=True, blank=True)
    product_name = models.ForeignKey(
        ProductName,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('产品名称')
    )
    recipe = models.ForeignKey(
        Recipe,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('配方编号')
    )
    tank = models.ForeignKey(
        Tank,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('设备编号')
    )
    date_start = models.DateField(_('开始日期'), null=True)
    operator = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('操作人员')
    )
    notes = models.TextField(_('备注'), max_length=1000, null=True, blank=True)
    is_share = models.BooleanField(_('可访问'), default=True)
    created_by = models.IntegerField(_('创建人'), null=True, blank=True)
    datetime_created = models.DateTimeField(_('创建时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    @property
    def brew_key(self):
        if self.datetime_created and self.brew_batch_code:
            access_key = hashlib.md5()
            access_key_c = '{0}{1}{2}'.format(GeneralConfig.order_key_generate, self.brew_batch_code,
                                              self.datetime_created).encode("utf8")
            access_key.update(access_key_c)
            return str(access_key.hexdigest())
        return None

    @property
    def delta_days(self):
        delta_days = None
        if self.date_start:
            delta_days = (timezone.localdate() - self.date_start).days
        return delta_days

    @property
    def sale_incomes(self):
        sale_incomes = Sale.objects.filter(pack__brew_id=self.pk).aggregate(
            sale_incomes=Sum("sale_price_link__money_in_out"))
        if sale_incomes:
            if sale_incomes['sale_incomes']:
                return sale_incomes['sale_incomes']
        return 0

    @property
    def material_costs(self):
        material_costs = MaterialOut.objects.filter(brew_id=self.pk)
        cost = 0
        if material_costs:
            for m in material_costs:
                if m.material_out_cost:
                    cost += round(m.material_out_cost, 2)
        return cost

    def get_absolute_url(self):
        return reverse('{0}:brew_detail'.format(app_name), kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-id']
        verbose_name = _('酿造批次')
        verbose_name_plural = _('酿造批次')
        permissions = (
            ("can_export_brew_data", _("可以导出酿造记录")),
        )

    def __str__(self):
        return '{0} {1} [{2}]'.format(
            self.brew_batch_code,
            self.product_name,
            self.tank
        )


@admin.register(Brew)
class BrewAdmin(admin.ModelAdmin):
    list_display = ('brew_batch_code', 'product_name', 'recipe', 'tank', 'date_start', 'operator', 'notes')
    list_filter = ('tank', 'product_name')
    search_fields = ['brew_batch_code', 'notes']


class BrewMonitor(models.Model):
    brew_monitor_code = models.CharField(_('糖化批次号'), max_length=30, unique=True, null=True, blank=True)
    brew = models.ForeignKey(
        Brew,
        on_delete=models.CASCADE,
        null=True,
        verbose_name=_('酿造批次'),
    )
    brew_date = models.DateField(_('糖化日期'), null=True)
    # The Volume of water or wort, Liter
    batch_volume = models.PositiveIntegerField(_('批次容量'), null=True)
    initial_water = models.PositiveIntegerField(_('起始水量'), null=True)
    sparge_water = models.PositiveIntegerField(_('洗糟水量'), null=True)
    mash_volume = models.PositiveIntegerField(_('糖化体积'), null=True, blank=True)
    after_boiling_add_water = models.IntegerField(_('煮沸后加水量'), default=0, blank=True)
    boiling_full_volume = models.PositiveIntegerField(_('煮沸锅满锅液位'), null=True, blank=True)
    enter_fermenter_volume = models.PositiveIntegerField(_('入发酵罐容量'), null=True, blank=True)
    # The temperature, Celsius
    initial_tem = models.DecimalField(_('糖化起始温度'), max_digits=3, decimal_places=1, null=True)
    sparge_tem = models.DecimalField(_('洗糟水温度'), max_digits=3, decimal_places=1, null=True)
    boiling_full_tem = models.DecimalField(_('煮沸锅满锅温度'), max_digits=4, decimal_places=1, null=True, blank=True)
    enter_fermenter_tem = models.DecimalField(_('入发酵罐温度'), max_digits=3, decimal_places=1, null=True, blank=True)
    # The pH and gravity
    ph_mash_0 = models.DecimalField(_('投料结束 pH'), max_digits=3, decimal_places=1, null=True, blank=True)
    ph_mash_1 = models.DecimalField(_('糖化第一步 pH'), max_digits=3, decimal_places=1, null=True, blank=True)
    brix_0 = models.DecimalField(_('头道麦汁 Brix'), max_digits=3, decimal_places=1, null=True, blank=True)
    ph_0 = models.DecimalField(_('头道麦汁 pH'), max_digits=3, decimal_places=2, null=True, blank=True)
    brix_1 = models.DecimalField(_('过滤1/2 Brix'), max_digits=3, decimal_places=1, null=True, blank=True)
    ph_1 = models.DecimalField(_('过滤1/2 pH'), max_digits=3, decimal_places=2, null=True, blank=True)
    brix_2 = models.DecimalField(_('末道麦汁 Brix'), max_digits=3, decimal_places=1, null=True, blank=True)
    ph_2 = models.DecimalField(_('末道麦汁 pH'), max_digits=3, decimal_places=2, null=True, blank=True)
    brix_3 = models.DecimalField(_('煮沸开始 Brix'), max_digits=3, decimal_places=1, null=True, blank=True)
    ph_3 = models.DecimalField(_('煮沸开始 pH'), max_digits=3, decimal_places=2, null=True, blank=True)
    og_wort = models.DecimalField(_('煮沸结束 Brix'), max_digits=3, decimal_places=1, null=True, blank=True)
    ph_wort = models.DecimalField(_('煮沸结束 pH'), max_digits=3, decimal_places=2, null=True, blank=True)
    # Time of important points
    malt_add_start = models.TimeField(_('投料开始'), null=True, blank=True)
    malt_add_end = models.TimeField(_('投料结束'), null=True, blank=True)
    recycle_start = models.TimeField(_('回流开始'), null=True, blank=True)
    into_boiling = models.TimeField(_('入煮沸锅'), null=True, blank=True)
    boiling_full = models.TimeField(_('煮沸锅满'), null=True, blank=True)
    boiling_start = models.TimeField(_('煮沸开始'), null=True, blank=True)
    boiling_end = models.TimeField(_('煮沸结束'), null=True, blank=True)
    whirlpool_end = models.TimeField(_('旋沉结束'), null=True, blank=True)
    enter_fermenter_start = models.TimeField(_('入罐开始'), null=True, blank=True)
    enter_fermenter_end = models.TimeField(_('入罐结束'), null=True, blank=True)
    brewer = models.ManyToManyField(
        Employee,
        verbose_name=_('酿酒师'),
    )
    created_by = models.IntegerField(_('创建人'), null=True, blank=True)
    notes = models.TextField(_('备注'), max_length=1000, null=True, blank=True)
    datetime_created = models.DateTimeField(_('创建时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    def get_absolute_url(self):
        if self.brew:
            return reverse('{0}:brew_detail'.format(app_name), kwargs={'pk': self.brew.pk})
        return reverse('{0}:ferment_monitor_list'.format(app_name))

    class Meta:
        ordering = ['-id']
        verbose_name = _('酿造监控')
        verbose_name_plural = _('酿造监控')

    def __str__(self):
        return '{0} {1} {2}'.format(
            self.brew_date,
            self.brew,
            self.brew_monitor_code
        )


@admin.register(BrewMonitor)
class BrewMonitorAdmin(admin.ModelAdmin):
    list_display = ('brew_monitor_code', 'brew', 'brew_date', 'og_wort',
                    'ph_mash_1', 'malt_add_start', 'enter_fermenter_start')
    list_filter = ('brewer',)
    search_fields = ['brew_monitor_code']


class FermentMonitor(models.Model):
    brew = models.ForeignKey(
        Brew,
        on_delete=models.CASCADE,
        verbose_name=_('酿造批次'),
    )
    sg_plato = models.DecimalField(_('糖度或比重'), max_digits=5, decimal_places=3, null=True,
                                   blank=True, validators=[MaxValueValidator(50), MinValueValidator(0)])
    sg = models.DecimalField(_('比重'), max_digits=4, decimal_places=3, null=True,
                             blank=True, validators=[MaxValueValidator(1.2), MinValueValidator(1.0)])
    plato = models.DecimalField(_('糖度'), max_digits=3, decimal_places=1, null=True,
                                blank=True, validators=[MaxValueValidator(43), MinValueValidator(0)])
    ph = models.DecimalField(_('pH'), max_digits=4, decimal_places=2, null=True,
                             blank=True, validators=[MaxValueValidator(8), MinValueValidator(1)])
    t_real = models.DecimalField(_('真实温度'), max_digits=3, decimal_places=1, null=True,
                                 blank=True, validators=[MaxValueValidator(35), MinValueValidator(-5)])
    t_set = models.DecimalField(_('设置温度'), max_digits=3, decimal_places=1, null=True,
                                blank=True, validators=[MaxValueValidator(35), MinValueValidator(-5)])
    bar = models.DecimalField(_('压力(Bar)'), max_digits=3, decimal_places=2, null=True,
                              blank=True, validators=[MaxValueValidator(3), MinValueValidator(0)])
    dry_hop = models.DecimalField(_('酒花干投量'), max_digits=5, decimal_places=2, null=True,
                                  blank=True)
    slag = models.DecimalField(_('排渣量'), max_digits=4, decimal_places=2, null=True, blank=True)
    notes = models.TextField(_('备注'), max_length=1000, null=True, blank=True)
    cell_mml = models.DecimalField(_('酵母数'), max_digits=6, decimal_places=2, null=True, blank=True)
    recorded = models.DateTimeField(_('记录于'), null=True)
    recorder = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('记录人员')
    )
    created_by = models.IntegerField(_('创建人'), null=True, blank=True)
    datetime_created = models.DateTimeField(_('记录时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    @property
    def delta_days(self):
        delta_days = None
        if self.recorded:
            delta_days = (self.recorded.date() - self.brew.date_start).days
        return delta_days

    def get_absolute_url(self):
        if self.brew:
            return reverse('{0}:brew_detail'.format(app_name), kwargs={'pk': self.brew_id})
        return reverse('{0}:ferment_monitor_list'.format(app_name))

    class Meta:
        ordering = ['-id']
        verbose_name = _('发酵监控')
        verbose_name_plural = _('发酵监控')

    def __str__(self):
        return '{0} {1} {2}'.format(
            self.brew,
            self.plato,
            self.ph
        )


@admin.register(FermentMonitor)
class FermentMonitorAdmin(admin.ModelAdmin):
    list_display = ('brew', 'sg', 'plato', 'ph', 't_real', 't_set', 'bar', 'notes', 'delta_days')
    list_filter = ('brew',)
    search_fields = ['notes']


class ProductPackSizeUnit(models.Model):
    product_pack_size = models.DecimalField(_('包装规格'), max_digits=6, decimal_places=1, null=True)
    product_pack_unit = models.CharField(_('规格单位'), max_length=20, null=True, choices=(('mL', 'mL'), ('L', 'L')))
    product_pack_type_en = models.CharField(_('包装类型-英文'), max_length=100, null=True, blank=True)
    product_pack_type_cn = models.CharField(_('包装类型-中文'), max_length=100, null=True)
    product_pack_code = models.CharField(_('包装编号'), max_length=5, unique=True, null=True)
    datetime_created = models.DateTimeField(_('记录时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    @property
    def product_pack_size_unit_en(self):
        return "{0}{1} {2}".format(
            str(self.product_pack_size).rstrip('0').rstrip('.'),
            self.product_pack_unit, self.product_pack_type_en)

    @property
    def product_pack_size_unit_cn(self):
        return "{0}{1} {2}".format(
            str(self.product_pack_size).rstrip('0').rstrip('.'),
            self.product_pack_unit, self.product_pack_type_cn)

    objects = models.Manager()

    def get_absolute_url(self):
        if self.pk:
            pass
        return reverse('{0}:product_pack_list'.format(app_name))

    class Meta:
        ordering = ['id']
        verbose_name = _('产品包装')
        verbose_name_plural = _('产品包装')

    def __str__(self):
        return "[{3}] {0} {1} {2}".format(
            str(self.product_pack_size).rstrip('0').rstrip('.'),
            self.product_pack_unit,
            self.product_pack_type_cn,
            self.product_pack_code
        )


@admin.register(ProductPackSizeUnit)
class ProductPackSizeUnitAdmin(admin.ModelAdmin):
    list_display = ('product_pack_code', 'product_pack_size', 'product_pack_unit', 'product_pack_type_en',
                    'product_pack_type_cn', 'datetime_updated')
    list_filter = ('product_pack_size',)
    search_fields = ['product_pack_code', 'product_pack_size', 'product_pack_unit',
                     'product_pack_type_en', 'product_pack_type_cn']


class ProductStyle(models.Model):
    product_style_cn = models.CharField(_('中文名称'), max_length=200, null=True)
    product_style_en = models.CharField(_('英文名称'), max_length=200, null=True, blank=True)
    product_style_desc_cn = models.TextField(_('中文描述'), max_length=2000, null=True, blank=True)
    product_style_desc_en = models.TextField(_('英文描述'), max_length=2000, null=True, blank=True)
    datetime_created = models.DateTimeField(_('记录时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    def get_absolute_url(self):
        if self.pk:
            pass
        return reverse('{0}:product_style_create'.format(app_name))

    class Meta:
        ordering = ['id']
        verbose_name = _('产品风格')
        verbose_name_plural = _('产品风格')

    def __str__(self):
        return '{0}'.format(self.product_style_cn)


@admin.register(ProductStyle)
class ProductStyleAdmin(admin.ModelAdmin):
    list_display = ('product_style_cn', 'product_style_en', 'product_style_desc_cn', 'product_style_desc_en',
                    'datetime_created', 'datetime_updated')
    search_fields = ['product_style_cn', 'product_style_en', 'product_style_desc_cn', 'product_style_desc_en']


class Product(models.Model):
    product_code = models.CharField(_('产品编号'), max_length=30, unique=True, null=True)
    product_name = models.ForeignKey(
        ProductName,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('产品名称')
    )
    product_pack = models.ForeignKey(
        ProductPackSizeUnit,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('产品包装')
    )
    logo = models.FileField(_('logo'), upload_to='{0}/product/logos'.format(app_name),
                            null=True, blank=True, storage=ImageStorage())
    image = models.FileField(_('图片'), upload_to='{0}/product/image'.format(app_name),
                             null=True, blank=True, storage=ImageStorage())
    image_banner = models.FileField(
        _('Banner图片'), upload_to='{0}/product/image'.format(app_name),
        null=True, blank=True, storage=ImageStorage())
    files = models.FileField(_('资料'), upload_to='{0}/product/files'.format(app_name),
                             null=True, blank=True, storage=ImageStorage())
    product_category = models.ManyToManyField(
        ProductCategory,
        blank=True,
        verbose_name=_('产品归类')
    )
    product_style = models.ForeignKey(
        ProductStyle,
        on_delete=models.SET_NULL,
        null=True,
        verbose_name=_('产品风格')
    )
    abv = models.DecimalField(_('酒精度'), max_digits=4, decimal_places=2, null=True, blank=True)
    plato = models.DecimalField(_('麦汁度'), max_digits=3, decimal_places=1, null=True, blank=True)
    ibu = models.PositiveSmallIntegerField(_('苦度'), null=True, blank=True)
    barcode = models.CharField(_('条码'), max_length=200, null=True, blank=True)
    index = models.IntegerField(_('排序编号'), default=99)
    is_show = models.BooleanField(_('是否显示'), default=True)
    is_banner = models.BooleanField(_('是Banner'), default=False)
    desc_en = models.TextField(_('英文介绍'), max_length=4000, null=True, blank=True)
    desc_cn = models.TextField(_('中文介绍'), max_length=4000, null=True, blank=True)
    supplier_price = models.DecimalField(_('经销商价'), max_digits=10, decimal_places=2, null=True)
    bar_price = models.DecimalField(_('酒吧报价'), max_digits=10, decimal_places=2, null=True)
    public_price = models.DecimalField(_('终端价格'), max_digits=10, decimal_places=2, null=True)
    created_by = models.IntegerField(_('创建人'), null=True, blank=True)
    datetime_created = models.DateTimeField(_('创建时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    @property
    def product_pack_sum(self):
        _('生产总量')
        if Pack:
            pps = Pack.objects.filter(product_id=self.pk).aggregate(Sum("pack_num"))
            if pps:
                if pps['pack_num__sum']:
                    return pps['pack_num__sum']
        return 0

    @property
    def product_pack_count(self):
        _('生产次数')
        if Pack:
            ppc = Pack.objects.filter(product_id=self.pk).aggregate(Count("pack_num"))
            if ppc:
                if ppc['pack_num__count']:
                    return ppc['pack_num__count']
        return 0

    @property
    def product_sale_sum(self):
        _('销售总量')
        if Sale:
            pss = Sale.objects.filter(Q(pack__product_id=self.pk) & Q(is_active=True)).aggregate(Sum("sale_num"))
            if pss:
                if pss['sale_num__sum']:
                    return pss['sale_num__sum']
        return 0

    @property
    def product_sale_count(self):
        _('销售次数')
        if Sale:
            psc = Sale.objects.filter(Q(pack__product_id=self.pk) & Q(is_active=True)).aggregate(Count("sale_num"))
            if psc:
                if psc['sale_num__count']:
                    return psc['sale_num__count']
        return 0

    @property
    def product_left_sum(self):
        _('库存')
        if self.product_pack_sum and self.product_sale_sum:
            return self.product_pack_sum - self.product_sale_sum
        return self.product_pack_sum

    @property
    def product_sale_price(self):
        _('销售总价')
        if Sale:
            psp = Sale.objects.filter(Q(pack__product_id=self.pk) & Q(is_active=True)).aggregate(Sum("sale_price"))
            if psp:
                if psp['sale_price__sum']:
                    return psp['sale_price__sum']
        return 0

    def get_absolute_url(self):
        if self.pk:
            pass
        return reverse('{0}:product_list'.format(app_name))

    class Meta:
        ordering = ['index']
        verbose_name = _('产品')
        verbose_name_plural = _('产品')

    def __str__(self):
        return "{0} ({1})".format(
            self.product_name,
            self.product_pack
        )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('pk', 'product_code', 'product_name', 'is_show', 'is_banner', 'supplier_price', 'bar_price', 'public_price')


class MaterialIn(models.Model):
    material_in_date = models.DateField(_('日期'), null=True)
    material_batch = models.ForeignKey(
        MaterialBatch,
        on_delete=models.CASCADE,
        verbose_name=_('原料批次')
    )
    warehouse = models.ForeignKey(
        Warehouse,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('存储位置')
    )
    amount = models.DecimalField(_('数量'), max_digits=10, decimal_places=3, null=True)
    material_cost_link = models.OneToOneField(
        MoneyInOut,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('流水链接')
    )
    material_cost = models.DecimalField(_('采购价'), max_digits=10, decimal_places=2, null=True)
    recorder = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('记录人员')
    )
    supplier = models.ForeignKey(
        Supplier,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('供应商')
    )
    notes = models.TextField(_('备注'), max_length=1000, null=True, blank=True)
    is_confirmed = models.BooleanField(_('已确认'), default=True)
    created_by = models.IntegerField(_('创建人'), null=True, blank=True)
    datetime_created = models.DateTimeField(_('记录时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    def get_absolute_url(self):
        if self.pk:
            pass
        return reverse('{0}:material_in_list'.format(app_name))

    class Meta:
        ordering = ['-id']
        verbose_name = _('原料入库')
        verbose_name_plural = _('原料入库')

    def __str__(self):
        return '{0} {1}'.format(
            self.material_batch,
            self.warehouse)


@admin.register(MaterialIn)
class MaterialInAdmin(admin.ModelAdmin):
    list_display = ('material_batch', 'warehouse', 'amount', 'recorder', 'notes', 'is_confirmed')
    list_filter = ('warehouse', 'is_confirmed')
    search_fields = ['notes', ]


class MaterialOut(models.Model):
    material_out_date = models.DateField(_('日期'), null=True)
    material_batch = models.ForeignKey(
        MaterialBatch,
        on_delete=models.CASCADE,
        null=True,
        verbose_name=_('原料批次')
    )
    brew = models.ForeignKey(
        Brew,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('酿造批次')
    )
    amount = models.DecimalField(_('数量'), max_digits=10, decimal_places=3)
    recorder = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('记录人')
    )
    notes = models.TextField(_('备注'), max_length=1000, null=True, blank=True)
    confirmed = models.BooleanField(_('已确认'), default=False)  # 参数暂时没有调用
    checked = models.BooleanField(_('已检查'), default=False)  # 参数暂时没有调用
    created_by = models.IntegerField(_('创建人'), null=True, blank=True)
    datetime_created = models.DateTimeField(_('记录时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    @property
    def material_out_cost(self):
        cost = 0
        if self.material_batch and self.amount:
            if self.material_batch.material_cost_each:
                cost = float(self.amount) * float(self.material_batch.material_cost_each)
        return round(cost, 2)

    def get_absolute_url(self):
        if self.pk:
            pass
        return reverse('{0}:material_out_list'.format(app_name))

    class Meta:
        ordering = ['-id']
        verbose_name = _('原料出库')
        verbose_name_plural = _('原料出库')

    def __str__(self):
        return '{0} {1} {2} {3} {4}'.format(
            self.material_batch,
            self.brew,
            self.amount,
            self.recorder,
            self.datetime_created
        )


@admin.register(MaterialOut)
class MaterialOutAdmin(admin.ModelAdmin):
    list_display = ('material_batch', 'brew', 'amount', 'recorder', 'notes', 'confirmed', 'checked')
    list_filter = ('brew', 'confirmed', 'checked')
    search_fields = ['notes', ]


class Pack(models.Model):
    pack_batch_code = models.CharField(_('灌装批次'), max_length=30, unique=True, null=True)
    brew = models.ForeignKey(
        Brew,
        on_delete=models.CASCADE,
        verbose_name=_('酿造批次'),
        related_name='packs'
    )
    product = models.ForeignKey(
        Product,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('产品')
    )
    pack_date = models.DateField(_('灌装日期'), null=True)
    pack_start = models.TimeField(_('灌装开始'), null=True, blank=True)
    pack_end = models.TimeField(_('灌装结束'), null=True, blank=True)
    pack_num = models.PositiveIntegerField(_('数量'), null=True)
    state = models.BooleanField(_('状态'), default=True)
    employee = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('操作员')
    )
    notes = models.TextField(_('备注'), max_length=1000, null=True, blank=True)
    confirmed = models.BooleanField(_('是否确认'), default=False)
    created_by = models.IntegerField(_('创建人'), null=True, blank=True)
    datetime_created = models.DateTimeField(_('创建时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    @property
    def delta_days(self):
        delta_days = None
        if self.pack_date:
            delta_days = (timezone.localdate() - self.pack_date).days
        return delta_days

    @property
    def pack_sale_num(self):
        _('销售数量')

        if Sale:
            pack_sale_sum = Sale.objects.filter(Q(pack_id=self.pk) & Q(is_active=True)).aggregate(Sum("sale_num"))
            if pack_sale_sum:
                return pack_sale_sum['sale_num__sum']
        return 0

    @property
    def pack_sale_count(self):
        _('销售次数')
        if Sale:
            pack_sale_c = Sale.objects.filter(Q(pack_id=self.pk) & Q(is_active=True)).aggregate(Count("sale_num"))
            if pack_sale_c:
                return pack_sale_c['sale_num__count']
        return 0

    @property
    def pack_num_left(self):
        _('库存')
        if self.pack_sale_num and self.pack_num:
            return self.pack_num - int(self.pack_sale_num)
        return self.pack_num

    @property
    def pack_sale_price(self):
        _('销售总额')
        if Sale:
            pack_sale_p_sum = Sale.objects.filter(Q(pack_id=self.pk) & Q(is_active=True)).aggregate(Sum("sale_price"))
            if pack_sale_p_sum:
                if pack_sale_p_sum['sale_price__sum']:
                    return pack_sale_p_sum['sale_price__sum']
        return 0

    def get_absolute_url(self):
        if self.pk:
            pass
        return reverse('{0}:pack_list'.format(app_name))

    class Meta:
        ordering = ['pk']
        verbose_name = _('产品入库')
        verbose_name_plural = _('产品入库')
        permissions = (
            ("can_export_pack_data", _("可以导出入库记录")),
        )

    def __str__(self):
        return '{0} {1} {2}{3}'.format(
            self.pack_batch_code,
            self.product,
            _('剩余: '),
            self.pack_num_left
        )


@admin.register(Pack)
class PackAdmin(admin.ModelAdmin):
    list_display = ('pack_batch_code', 'brew', 'product', 'pack_date', 'pack_num', 'confirmed', 'datetime_updated')
    list_filter = ('product', 'employee', 'confirmed')
    search_fields = ['notes', ]


class Report(models.Model):
    report_code = models.CharField(_('报告编号'), max_length=30, unique=True, null=True, blank=True)
    pack = models.ForeignKey(
        Pack,
        on_delete=models.CASCADE,
        verbose_name=_('灌装批次'),
        related_name='report'
    )
    report_date = models.DateField(_('报告日期'), null=True)
    employee = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('检验人员'),
    )
    ebc = models.PositiveIntegerField(_('色度'), null=True, blank=True)
    turbidity = models.PositiveIntegerField(_('浊度'), null=True, blank=True)
    foam = models.PositiveIntegerField(_('泡持性'), null=True, blank=True)
    abv = models.DecimalField(_('酒精度'), max_digits=3, decimal_places=1, null=True, blank=True)
    plato = models.DecimalField(_('原麦汁度'), max_digits=3, decimal_places=1, null=True, blank=True)
    total_acid = models.DecimalField(_('总酸'), max_digits=2, decimal_places=1, null=True, blank=True)
    co2 = models.DecimalField(_('二氧化碳'), max_digits=3, decimal_places=2, null=True, blank=True)
    diacetyl = models.DecimalField(_('双乙酰'), max_digits=3, decimal_places=2, null=True, blank=True)
    enzyme = models.BooleanField(_('蔗糖转化酶'), default=True)
    notes = models.TextField(_('备注'), max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(_('有效'), default=True)
    is_confirmed = models.BooleanField(_('是否确认'), default=False)
    created_by = models.IntegerField(_('创建人'), null=True, blank=True)
    datetime_created = models.DateTimeField(_('创建时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    def get_absolute_url(self):
        if self.pack:
            return reverse('{0}:brew_detail'.format(app_name), kwargs={'pk': self.pack.brew.pk})
        else:
            return None

    class Meta:
        ordering = ['-pk']
        verbose_name = _('产品检验报告')
        verbose_name_plural = _('产品检验报告')

    def __str__(self):
        return '{0} {1}'.format(
            self.report_code, self.report_date
        )


@admin.register(Report)
class ReportAdmin(admin.ModelAdmin):
    list_display = ('report_code', 'pack', 'report_date', 'employee', 'ebc', 'foam', 'abv', 'plato', 'total_acid',
                    'co2', 'diacetyl', 'notes', 'is_active', 'is_confirmed', 'datetime_updated')
    list_filter = ('employee', 'is_active', 'is_confirmed')
    search_fields = ['notes', ]


class ClientAddress(models.Model):
    client = models.ForeignKey(
        Client,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('客户'),
    )
    user_name = models.CharField(_('收货人'), max_length=200, null=True, blank=True)
    postal_code = models.CharField(_('邮政编码'), max_length=20, null=True, blank=True)
    province_name = models.CharField(_('省份'), max_length=200, null=True, blank=True)
    city_name = models.CharField(_('城市'), max_length=200, null=True, blank=True)
    county_name = models.CharField(_('辖区'), max_length=200, null=True, blank=True)
    detail_info = models.CharField(_('街道'), max_length=200, null=True, blank=True)
    national_code = models.CharField(_('国家码'), max_length=200, null=True, blank=True)
    tel_number = models.CharField(_('手机号'), max_length=20, null=True, blank=True)
    is_active = models.BooleanField(_('是否有效'), default=True)
    datetime_created = models.DateTimeField(_('记录时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    class Meta:
        ordering = ['id']
        verbose_name = _('收货地址')
        verbose_name_plural = _('收货地址')

    def __str__(self):
        return "{0} {1}".format(
            self.pk,
            self.client,
        )


@admin.register(ClientAddress)
class ClientAddressAdmin(admin.ModelAdmin):
    list_display = ('client', 'province_name', 'city_name', 'county_name', 'detail_info', 'user_name', 'tel_number')
    search_fields = ['detail_info', 'user_name']


class OrderState(models.Model):
    order_state_cn = models.CharField(_('订单状态中文'), max_length=40, unique=True, null=True, blank=True)
    order_state_en = models.CharField(_('订单状态英文'), max_length=40, null=True, blank=True)
    order_state_desc_cn = models.TextField(_('订单状态中文介绍'), max_length=1000, null=True, blank=True)
    order_state_desc_en = models.TextField(_('订单状态英文介绍'), max_length=1000, null=True, blank=True)
    datetime_created = models.DateTimeField(_('创建时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    @property
    def order_num(self):
        sale_orders = SaleOrder.objects.filter(order_state_id=self.pk)
        if sale_orders.exists():
            return sale_orders.count()
        return 0

    @property
    def next_order_state_cn(self):
        if self.pk < 4:
            next_state = OrderState.objects.filter(pk=self.pk + 1)
            if next_state.exists():
                return next_state.first().order_state_cn
        return None

    class Meta:
        ordering = ['id']
        verbose_name = _('订单状态')
        verbose_name_plural = _('订单状态')

    def __str__(self):
        return "{0}".format(self.order_state_cn)


@admin.register(OrderState)
class OrderStateAdmin(admin.ModelAdmin):
    list_display = ('order_state_cn', 'order_state_en')


class SaleOrder(models.Model):
    sale_order_code = models.CharField(_('订单编号'), max_length=30, unique=True, null=True, blank=True)
    sale_order_date = models.DateField(_('订单日期'), null=True, blank=True)
    order_state = models.ForeignKey(
        OrderState,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('订单状态')
    )
    employee = models.ForeignKey(
        Employee,
        null=True,
        on_delete=models.SET_NULL,
        verbose_name=_('销售员'),
        limit_choices_to={'is_salesman': True},
    )
    client = models.ForeignKey(
        Client,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        verbose_name=_('购买客户'),
    )
    created_by = models.IntegerField(_('创建人'), null=True, blank=True)
    notes = models.TextField(_('备注'), max_length=1000, null=True, blank=True)
    is_active = models.BooleanField(_('是否有效'), default=True)
    is_delivered = models.BooleanField(_('已发货'), default=False)
    fee_received = models.BooleanField(_('款结清'), default=False)
    is_from_wx = models.BooleanField(_('来自微信'), default=False)
    datetime_created = models.DateTimeField(_('创建时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    @property
    def total_price(self):
        price = 0
        sales = Sale.objects.filter(sale_order=self.pk).filter(is_active=True).aggregate(Sum("sale_price"))
        if sales:
            if sales['sale_price__sum']:
                price = float(sales['sale_price__sum'])
        return round(price, 2)

    @property
    def product_items(self):
        sales = Sale.objects.filter(sale_order=self.pk)
        if sales:
            return sales
        return None

    def get_absolute_url(self):
        return reverse('{0}:sale_order_detail'.format(app_name), kwargs={'pk': self.pk})

    class Meta:
        ordering = ['-id']
        verbose_name = _('销售订单')
        verbose_name_plural = _('销售订单')

    def __str__(self):
        return "{0}".format(self.sale_order_code)


@admin.register(SaleOrder)
class SaleOrderAdmin(admin.ModelAdmin):
    list_display = ('sale_order_code', 'sale_order_date', 'order_state', 'employee', 'client',
                    'created_by', 'notes', 'is_active', 'datetime_created', 'datetime_updated')
    list_filter = ('order_state', 'employee', 'client', 'is_active')
    search_fields = ['notes', ]


class Sale(models.Model):
    sale_order = models.ForeignKey(
        SaleOrder,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('销售订单')
    )
    sale_date = models.DateField(_('出库日期'), null=True, blank=True)
    pack = models.ForeignKey(
        Pack,
        on_delete=models.CASCADE,
        verbose_name=_('灌装批次'),
        related_name='sales'
    )
    sale_num = models.PositiveIntegerField(_('订单数量'), null=True)
    sale_price_link = models.OneToOneField(
        MoneyInOut,
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        verbose_name=_('出售价格'),
    )
    sale_price = models.DecimalField(_('出售价'), max_digits=10, decimal_places=2, null=True)
    notes = models.TextField(_('备注'), max_length=1000, null=True, blank=True)
    is_sale = models.BooleanField(_('正常出售'), default=True)
    is_active = models.BooleanField(_('订单有效'), default=True)
    is_confirmed = models.BooleanField(_('已出库'), default=False)
    fee_received = models.BooleanField(_('已收款'), default=False)
    created_by = models.IntegerField(_('创建人'), null=True, blank=True)
    datetime_created = models.DateTimeField(_('创建时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    def get_absolute_url(self):
        if self.sale_order:
            return reverse('{0}:sale_order_detail'.format(app_name), kwargs={'pk': self.sale_order.pk})
        return reverse('{0}:sale_list'.format(app_name))

    class Meta:
        ordering = ['-pk']
        verbose_name = _('产品出库')
        verbose_name_plural = _('产品出库')
        permissions = (
            ("confirm_sale", _("可以确认出库")),
            ("confirm_fee_receive", _("可以确认收款")),
            ("can_export_sale_data", _("可以导出出库记录"))
        )

    def __str__(self):
        return '{0} {1} {2}'.format(self.pk, self.pack, self.sale_num)


@admin.register(Sale)
class SaleAdmin(admin.ModelAdmin):
    list_display = ('sale_order', 'pack', 'sale_num', 'sale_price', 'notes', 'is_sale', 'is_active', 'is_confirmed',
                    'fee_received', 'datetime_created', 'datetime_updated')
    list_filter = ('sale_order', 'pack', 'is_sale', 'is_active', 'is_confirmed', 'fee_received')
    search_fields = ['notes', ]


class HandBook(models.Model):
    chapter = models.IntegerField(_('编号'), null=True)
    chapter_code = models.CharField(_('章节标签'), max_length=30, null=True)
    chapter_name_cn = models.CharField(_('章节中文名'), max_length=200, null=True)
    chapter_content_cn = models.TextField(_('中文内容'), max_length=10000, null=True, blank=True)
    chapter_name_en = models.CharField(_('章节英文名'), max_length=200, null=True, blank=True)
    chapter_content_en = models.TextField(_('英文内容'), max_length=10000, null=True, blank=True)
    datetime_created = models.DateTimeField(_('记录时间'), auto_now_add=True)
    datetime_updated = models.DateTimeField(_('更新时间'), auto_now=True)

    objects = models.Manager()

    def get_absolute_url(self):
        if self.pk:
            pass
        return reverse('{0}:handbook'.format(app_name))

    class Meta:
        ordering = ['id']
        verbose_name = _('使用说明')
        verbose_name_plural = _('使用说明')

    def __str__(self):
        return "{0} {1}".format(
            self.chapter,
            self.chapter_name_cn,
        )


@admin.register(HandBook)
class HandBookAdmin(admin.ModelAdmin):
    list_display = ('chapter', 'chapter_code', 'chapter_name_cn', 'chapter_name_en',
                    'datetime_created', 'datetime_updated')
