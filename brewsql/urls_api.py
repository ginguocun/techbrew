from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import views_wx, views_api, views_export
from .apps import GeneralConfig

app_name = GeneralConfig.name

# API endpoints
urlpatterns = format_suffix_patterns([
    url(r'^$', views_api.api_root),
    # 以下接口用于微信小程序
    url(r'^wechat_login/$', views_wx.wechat_login, name='wechat_login_api'),
    url(r'^categories/$', views_wx.category_list, name='categories_api'),
    url(r'^states/$', views_wx.OrderStateView.as_view(), name='states_api'),
    url(r'^products/$', views_wx.product_list, name='products_api'),
    url(r'^banners/$', views_wx.BannerListView.as_view(), name='banners_api'),
    url(r'^product/(?P<pk>[0-9]+)/$', views_wx.product_detail, name='product_detail'),
    url(r'^submit/$', views_wx.submit, name='submit_api'),
    url(r'^add_address/$', views_wx.add_address, name='add_address'),
    url(r'^address_list/$', views_wx.ClientAddressView.as_view(), name='address_list'),
    url(r'^sale_number_list/$', views_wx.SaleNumberListView.as_view(), name='sale_number_list'),
    # Excel 导出接口
    url(r'^brew-xls/$', views_export.brew_export, name='brew-xls'),
    url(r'^pack-xls/$', views_export.pack_export, name='pack-xls'),
    url(r'^sale-xls/$', views_export.sale_export, name='sale-xls'),
    #  以下有api由rest_framework创建，登录可用
    url(r'^packs/$', views_api.PackList.as_view(), name='pack-list'),
    url(r'^packs/(?P<pk>[0-9]+)/$', views_api.PackDetail.as_view(), name='pack-detail'),
    url(r'^sales/$', views_api.SaleList.as_view(), name='sale-list'),
    url(r'^sales/(?P<pk>[0-9]+)/$', views_api.SaleDetail.as_view(), name='sale-detail'),
    url(r'^brews/$', views_api.BrewList.as_view(), name='brew-list'),
    url(r'^brews/(?P<pk>[0-9]+)/$', views_api.BrewDetail.as_view(), name='brew-detail'),
])
