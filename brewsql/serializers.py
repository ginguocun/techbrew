from django.utils.translation import gettext_lazy as _

from rest_framework import serializers

from .models import *


class BannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ('pk', 'product_name', 'image_banner')
        depth = 1


class SaleSerializer(serializers.ModelSerializer):

    class Meta:
        model = Sale
        fields = '__all__'


class PackSerializer(serializers.ModelSerializer):
    brew_info = serializers.CharField(source='brew', label=_('批次详情'))
    product_info = serializers.CharField(source='product', label=_('产品详情'))
    pack_sale_num = serializers.ReadOnlyField(label=_('已售数量'))
    pack_sale_count = serializers.ReadOnlyField(label=_('已售次数'))
    pack_num_left = serializers.ReadOnlyField(label=_('剩余库存'))
    sales = SaleSerializer(many=True, read_only=True)

    class Meta:
        model = Pack
        # read_only = True
        fields = ['id', 'pack_batch_code', 'pack_date', 'brew', 'brew_info', 'product', 'product_info', 'sales',
                  'state', 'notes',
                  'pack_num', 'pack_sale_num', 'pack_sale_count', 'pack_num_left']


class BrewSerializer(serializers.ModelSerializer):

    class Meta:
        model = Brew
        fields = '__all__'


class OrderStateSerializer(serializers.ModelSerializer):

    class Meta:
        model = OrderState
        fields = ('pk', 'order_state_cn')


class SaleOrderSerializer(serializers.ModelSerializer):
    # url = serializers.CharField(source='get_absolute_url', read_only=True)
    # total_price = serializers.CharField(source='total_price', read_only=True)

    class Meta:
        model = SaleOrder
        fields = ('pk', 'sale_order_code', 'sale_order_date', 'order_state', 'total_price', 'is_active')
        depth = 1
        read_only_fields = ('sale_order_code',)


class ClientAddressSerializer(serializers.ModelSerializer):

    class Meta:
        model = ClientAddress
        fields = ('client', 'user_name', 'province_name', 'city_name', 'county_name', 'detail_info', 'postal_code',
                  'tel_number')
