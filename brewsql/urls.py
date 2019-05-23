from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path, path
from .apps import GeneralConfig
from .views import views, views_add, views_detail, views_edit

app_name = GeneralConfig.name

urlpatterns = [
    re_path(r'^$', views.home_overview, name='home'),
    # 酿造批次管理
    re_path(r'^brew_batch_list/$', views.BrewListView.as_view(), name='brew_list'),
    re_path(r'^brew/(?P<pk>\d+)/$', views_detail.brew_detail, name='brew_detail'),
    path('brew/<int:pk>/<slug:brew_key>/', views_detail.brew_detail_public, name='brew_detail_public'),
    re_path(r'^add_brew/$', views_add.BrewCreate.as_view(), name='add_brew'),
    re_path(r'^brew_update/(?P<pk>\d+)/$', views_edit.BrewUpdate.as_view(), name='brew_update'),
    # 酿造管理-糖化
    re_path(r'^add_brew_record/$', views_add.BrewMonitorCreate.as_view(), name='add_brewmonitor'),
    re_path(r'^change_brew_record/(?P<pk>\d+)/$', views_edit.BrewMonitorUpdate.as_view(), name='change_brewmonitor'),
    # 酿造管理-发酵监控
    re_path(r'^ferment_monitor_list/$', views.FermentMonitorListView.as_view(), name='ferment_monitor_list'),
    re_path(r'^new_ferment_record/$', views_add.add_ferment_monitor, name='new_ferment_record'),
    re_path(r'^new_ferment_record/(?P<pk>\d+)/$', views_add.add_ferment_monitor, name='new_ferment_record_2'),
    re_path(r'^ferment_monitor_delete/(?P<pk>\d+)/$', views_edit.FermentMonitorDelete.as_view(),
            name='ferment_monitor_delete'),
    # 酿造管理-检验报告
    re_path(r'^add_report/$', views_add.ReportCreate.as_view(), name='add_report'),
    re_path(r'^report_update/(?P<pk>\d+)/$', views_edit.ReportUpdate.as_view(), name='report_update'),
    # 发酵罐
    re_path(r'^tank_list/$', views.TankListView.as_view(), name='tank_list'),
    re_path(r'^tanks_overview/$', views.tanks_overview, name='tanks_overview'),
    re_path(r'^tank_update/$', views_edit.tank_update, name='tank_update'),
    # 员工管理
    re_path(r'^employee_list/$', views.EmployeeListView.as_view(), name='employee_list'),
    re_path(r'^add_employee/$', views_add.EmployeeCreate.as_view(), name='add_employee'),
    re_path(r'^employee_update/(?P<pk>\d+)/$', views_edit.EmployeeUpdate.as_view(), name='employee_update'),
    re_path(r'^employee_state_list/$', views_add.EmployeeStateCreate.as_view(), name='employee_state_list'),
    re_path(r'^employee_s_update/(?P<pk>\d+)/$', views_edit.EmployeeStateUpdate.as_view(), name='employee_s_update'),
    # 客户等级管理
    re_path(r'^client_level_list/$', views_add.ClientLevelCreate.as_view(), name='client_level_list'),
    re_path(r'^client_level_update/(?P<pk>\d+)/$', views_edit.ClientLevelUpdate.as_view(), name='client_level_update'),
    # 客户管理
    re_path(r'^client_list/$', views.ClientListView.as_view(), name='client_list'),
    re_path(r'^client/(?P<pk>\d+)/$', views_detail.client_detail, name='client_detail'),
    re_path(r'^add_client/$', views_add.ClientCreate.as_view(), name='add_client'),
    re_path(r'^client_update/(?P<pk>\d+)/$', views_edit.ClientUpdate.as_view(), name='client_update'),
    # 供应商管理
    re_path(r'^supplier_list/$', views.SupplierListView.as_view(), name='supplier_list'),
    re_path(r'^supplier/(?P<pk>\d+)/$', views_detail.supplier_detail, name='supplier_detail'),
    re_path(r'^add_supplier/$', views_add.SupplierCreate.as_view(), name='add_supplier'),
    re_path(r'^supplier_update/(?P<pk>\d+)/$', views_edit.SupplierUpdate.as_view(), name='supplier_update'),
    # 公司信息管理
    re_path(r'^company_list/$', views.CompanyListView.as_view(), name='company_list'),
    re_path(r'^add_company/$', views_add.CompanyCreate.as_view(), name='add_company'),
    re_path(r'^company_update/(?P<pk>\d+)/$', views_edit.CompanyUpdate.as_view(), name='company_update'),
    # 产品风格
    re_path(r'^product_style/$', views_add.ProductStyleCreateView.as_view(), name='product_style_create'),
    re_path(r'^product_style_update/(?P<pk>\d+)/$', views_edit.ProductStyleUpdateView.as_view(),
            name='product_style_update'),
    # 产品管理
    re_path(r'^product_inventory/$', views.product_inventory, name='product_inventory'),
    re_path(r'^product_list/$', views.ProductListView.as_view(), name='product_list'),
    re_path(r'^product_update/(?P<pk>\d+)/$', views_edit.ProductUpdate.as_view(), name='product_update'),
    # 产品包装管理
    re_path(r'^product_pack_list/$', views.ProductPackSizeUnitListView.as_view(), name='product_pack_list'),
    re_path(r'^add_product_pack/$', views_add.ProductPackSizeUnitCreate.as_view(), name='add_productpacksizeunit'),
    re_path(r'^product_pack_update/(?P<pk>\d+)/$', views_edit.ProductPackUpdate.as_view(), name='product_pack_update'),
    # 产品归类管理
    re_path(r'^product_category_list/$', views.ProductCategoryListView.as_view(), name='product_category_list'),
    re_path(r'^add_product_category/$', views_add.ProductCategoryCreate.as_view(), name='add_productcategory'),
    re_path(r'^product_category_update/(?P<pk>\d+)/$', views_edit.ProductCategoryUpdate.as_view(),
            name='product_category_update'),
    # 产品名称管理
    re_path(r'^product_name_list/$', views.ProductNameListView.as_view(), name='product_name_list'),
    re_path(r'^add_product_name/$', views_add.ProductNameCreate.as_view(), name='add_productname'),
    re_path(r'^product_name_update/(?P<pk>\d+)/$', views_edit.ProductNameUpdate.as_view(),
            name='product_name_update'),
    # 产品入库管理
    re_path(r'^pack_list/$', views.PackListView.as_view(), name='pack_list'),
    re_path(r'^add_pack/$', views_add.add_pack, name='add_pack'),
    re_path(r'^pack_update/(?P<pk>\d+)/$', views_edit.PackUpdate.as_view(), name='pack_update'),
    # 产品出库单号管理
    re_path(r'^sale_order_list/$', views.SaleOrderListView.as_view(), name='sale_order_list'),
    re_path(r'^sale_order_list_wx/$', views.SaleOrderWxListView.as_view(), name='sale_order_list_wx'),
    re_path(r'^add_sale_order/$', views_add.SaleOrderCreate.as_view(), name='add_saleorder'),
    re_path(r'^sale_order_update/(?P<pk>\d+)/$', views_edit.SaleOrderUpdate.as_view(), name='sale_order_update'),
    re_path(r'^order_state_update/(?P<pk>\d+)/$', views_edit.SaleOrderStateUpdate.as_view(), name='order_state_update'),
    re_path(r'^sale_order_delete/(?P<pk>\d+)/$', views_edit.delete_sale_order, name='sale_order_delete'),
    re_path(r'^sale_order_next/$', views_edit.sale_order_next, name='sale_order_next'),
    re_path(r'^sale_order_good_deliver/$', views_edit.sale_order_good_deliver, name='sale_order_good_deliver'),
    re_path(r'^sale_order_fee_receive/$', views_edit.sale_order_fee_receive, name='sale_order_fee_receive'),
    re_path(r'^sale_order_detail/(?P<pk>\d+)/$', views_detail.sale_order_detail, name='sale_order_detail'),
    # 产品出库管理
    re_path(r'^sale_list/$', views.SaleListView.as_view(), name='sale_list'),
    re_path(r'^add_sale/$', views_add.SaleCreate.as_view(), name='add_sale'),
    re_path(r'^sale_update/(?P<pk>\d+)/$', views_edit.SaleUpdate.as_view(), name='sale_update'),
    re_path(r'^sale_confirm/$', views_edit.sale_confirm, name='sale_confirm'),
    re_path(r'^sale_delete/(?P<pk>\d+)/$', views_edit.sale_delete, name='sale_delete'),
    re_path(r'^sale_pay/$', views_edit.sale_pay, name='sale_pay'),
    # 原料管理
    re_path(r'^material_list/$', views.MaterialListView.as_view(), name='material_list'),
    re_path(r'^add_material/$', views_add.MaterialCreate.as_view(), name='add_material'),
    re_path(r'^material_update/(?P<pk>\d+)/$', views_edit.MaterialUpdate.as_view(), name='material_update'),
    # 原料批次管理
    re_path(r'^material_batch_list/$', views.MaterialBatchListView.as_view(), name='material_batch_list'),
    re_path(r'^material_batch/(?P<pk>\d+)/$', views_detail.material_batch_detail, name='material_batch_detail'),
    re_path(r'^add_material_batch/$', views_add.MaterialBatchCreate.as_view(), name='add_material_batch'),
    re_path(r'^material_batch_update/(?P<pk>\d+)/$', views_edit.MaterialBatchUpdate.as_view(),
            name='material_batch_update'),
    # 原料入库管理
    re_path(r'^material_in_list/$', views.MaterialInListView.as_view(), name='material_in_list'),
    re_path(r'^add_materials_in/$', views_add.MaterialInCreate.as_view(), name='add_material_in'),
    re_path(r'^material_in_update/(?P<pk>\d+)/$',  views_edit.MaterialInUpdate.as_view(), name='material_in_update'),
    re_path(r'^material_in_delete/(?P<pk>\d+)/$',  views_edit.MaterialInDelete.as_view(), name='material_in_delete'),
    # 原料出库管理
    re_path(r'^material_out_list/$', views.MaterialOutListView.as_view(), name='material_out_list'),
    re_path(r'^add_materials_out/$', views_add.MaterialOutCreate.as_view(), name='add_material_out'),
    re_path(r'^material_out_update/(?P<pk>\d+)/$', views_edit.MaterialOutUpdate.as_view(), name='material_out_update'),
    re_path(r'^material_out_delete/(?P<pk>\d+)/$', views_edit.MaterialOutDelete.as_view(), name='material_out_delete'),
    # 原料包装规格
    re_path(r'^material_pack_list/$', views_add.MaterialPackSizeUnitCreate.as_view(), name='material_pack_list'),
    re_path(r'^material_pack_update/(?P<pk>\d+)/$', views_edit.MaterialPackUpdate.as_view(),
            name='material_pack_update'),
    # 仓库管理
    re_path(r'^warehouse_list/$', views_add.WarehouseCreate.as_view(), name='warehouse_list'),
    re_path(r'^warehouse_update/(?P<pk>\d+)/$', views_edit.WarehouseUpdate.as_view(), name='warehouse_update'),
    # 公司类型管理
    re_path(r'^company_type_list/$', views_add.CompanyTypeCreate.as_view(), name='company_type_list'),
    re_path(r'^company_type_update/(?P<pk>\d+)/$', views_edit.CompanyTypeUpdate.as_view(), name='company_type_update'),
    # 资金流水
    re_path(r'^money_io_types/$', views_add.MoneyInOutTypeCreate.as_view(), name='money_inout_types'),
    re_path(r'^money_iot_update/(?P<pk>\d+)/$', views_edit.MoneyInOutTypeUpdate.as_view(), name='money_iot_update'),
    re_path(r'^money_io_list/$', views.MoneyInOutListView.as_view(), name='moneyinout_list'),
    re_path(r'^money_io_update/(?P<pk>\d+)/$', views_edit.MoneyInOutUpdate.as_view(), name='moneyinout_update'),
    re_path(r'^money_ios_update/(?P<pk>\d+)/$', views_edit.MoneyInOutStateUpdate.as_view(), name='money_ios_update'),
    re_path(r'^add_money_io/$', views_add.MoneyInOutCreate.as_view(), name='add_moneyinout'),
    re_path(r'^confirm_moneyinout/$', views_edit.confirm_moneyinout, name='confirm_moneyinout'),
    re_path(r'^money_io_delete/(?P<pk>\d+)/$', views_edit.MoneyInOutDelete.as_view(), name='money_io_delete'),
    # 温度更新
    # re_path(r'^temp/update$', views.update_temp, name='tem_update'),
    # 用户管理
    re_path(r'^users/$', views_add.create_s_user, name='user_list'),
    re_path(r'^groups/$', views_add.GroupCreate.as_view(), name='group_list'),
    re_path(r'^user_update/(?P<pk>\d+)/$', views_edit.UserUpdate.as_view(), name='user_update'),
    re_path(r'^group_update/(?P<pk>\d+)/$', views_edit.GroupUpdate.as_view(), name='group_update'),
    re_path(r'^user_action_list/$', views.user_action_list, name='user_action_list'),
    re_path(r'^change_password/$', views_edit.password_change_own, name='change_password'),
    # 使用说明
    re_path(r'^handbook/$', views.handbook, name='handbook'),
    re_path(r'^add_handbook/$', views_add.HandBookCreate.as_view(), name='add_handbook'),
    re_path(r'^handbook_update/(?P<pk>\d+)/$', views_edit.HandBookUpdate.as_view(), name='change_handbook'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
