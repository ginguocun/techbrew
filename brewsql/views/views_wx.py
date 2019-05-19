from django.http import HttpResponse, HttpRequest, JsonResponse
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status, response
from django.conf import settings
from django.core.paginator import Paginator
from django_filters.rest_framework import DjangoFilterBackend
import json
import logging
import jwt
from weixin import WXAPPAPI
from ..serializers import *


logger = logging.getLogger('django')


def tid_maker():
    return '{0:%Y%m%d%H%M%S%f}'.format(timezone.localtime())


def create_user_by_openid(openid=None):
    if openid:
        account_check = Client.objects.filter(openid=openid)
        if account_check.exists():
            return account_check.first()
        else:
            account = Client(openid=openid)
            account.save()
            return account
    return None


def token_generate(payload):
    jwt_token = jwt.encode(payload, settings.JWT_SIGNING_KEY, algorithm='HS256')
    return jwt_token.decode('utf-8')


def token_verify(token):
    try:
        payload = jwt.decode(token, settings.JWT_SIGNING_KEY, algorithms=['HS256'])
        logger.info("token verified success")
        logger.info("payload: {0}".format(payload))
        pk = payload.get('pk')
        client = Client.objects.filter(pk=pk)
        if client.exists():
            user = client.first()
            return user
        return None
    except jwt.exceptions.InvalidTokenError:
        logger.info("token verified failed")
        return None


def jwt_required(view_func):
    @csrf_exempt
    def decorator(request, *args, **kwargs):
        if request.content_type == 'application/json':
            jwt_token = request.META.get('HTTP_JWT')
            logger.info("jwt_token: {0}".format(jwt_token))
            if jwt_token:
                user = token_verify(jwt_token.encode('utf-8'))
                if user:
                    return view_func(request, *args, **kwargs)
        return HttpResponse(json.dumps({'err': 'token not verified'}),
                            content_type="application/json",
                            status=status.HTTP_400_BAD_REQUEST)
    return decorator


@csrf_exempt
@require_http_methods(["POST"])
def wechat_login(request):
    if request.method == "POST":
        if request.body:
            received_data = json.loads(request.body.decode('utf-8'))
            code = received_data.get('code', None)
            logger.info("Code: {0}".format(code))
            user_info = received_data.get('user_info', None)
            logger.info("user_info: {0}".format(user_info))
            if code:
                api = WXAPPAPI(appid=GeneralConfig.wx_app_id, app_secret=GeneralConfig.wx_app_secret)
                try:
                    session_info = api.exchange_code_for_session_key(code=code)
                    openid = session_info.get('openid', None)
                    logger.info("openid: {0}".format(openid))
                    if openid:
                        queryset = Client.objects.filter(openid=openid)
                        if queryset.exists():
                            account = queryset.first()
                        else:
                            account = create_user_by_openid(openid=openid)
                        logger.info("account: {0}".format(account))
                        if account:
                            if user_info:
                                account.nickname = user_info['nickName']
                                account.gender = user_info['gender']
                                account.language = user_info['language']
                                account.city = user_info['city']
                                account.province = user_info['province']
                                account.country = user_info['country']
                                account.avatar = user_info['avatarUrl']
                                account.save()
                                logger.info("Account saved: pk={0}".format(account.pk))
                            # 基于 Client 生成 jwt 的 token
                            is_sync = False
                            if account.nickname:
                                is_sync = True
                            return JsonResponse(
                                {'jwt': token_generate(payload={"pk": account.pk}), 'is_sync': is_sync},
                                status=status.HTTP_200_OK)
                        return JsonResponse({'err': '数据库连接失败'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                    return JsonResponse({'err': '提供的数据验证失败'}, status=status.HTTP_400_BAD_REQUEST)
                except Exception as err:
                    return JsonResponse({'err': str(err)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    return JsonResponse({'err': '访问方式不对'}, status=status.HTTP_400_BAD_REQUEST)


def product_to_dict(p, level=None):
    d = dict()
    d['pk'] = p.pk
    d['product_name'] = p.product_name.product_name_cn
    d['product_name_en'] = p.product_name.product_name_en
    if p.product_pack:
        d['product_pack'] = p.product_pack.product_pack_size_unit_cn
    else:
        d['product_pack'] = None
    d['product_left'] = float(p.product_left_sum)
    d['product_desc'] = p.desc_cn
    if p.abv:
        d['abv'] = '{0} %'.format(p.abv)
    else:
        d['abv'] = None
    if p.ibu:
        d['ibu'] = '{0} IBU'.format(p.ibu)
    else:
        d['ibu'] = None
    if p.plato:
        d['plato'] = '{0} P'.format(p.plato)
    else:
        d['plato'] = None
    if p.product_style:
        d['style'] = p.product_style.product_style_cn
    else:
        d['style'] = None
    if p.image:
        d['image'] = 'http://{0}{1}'.format(settings.MEDIA_URL, p.image)
    else:
        d['image'] = None
    if p.public_price:
        d['price'] = float(p.public_price)
    else:
        d['price'] = 8888
    if level == 1:
        if p.bar_price:
            d['price'] = float(p.bar_price)
    if level == 2:
        if p.supplier_price:
            d['price'] = float(p.supplier_price)
    return d


def product_to_array(queryset, level=None):
    ob = []
    if queryset:
        for item in queryset:
            if item.product_left_sum >= 0:
                ob.append(product_to_dict(item, level))
        return ob
    else:
        return None


def page_data(request, queryset=None, url_reverse=None, per_page_count=4):
    page = request.GET.get('page')
    c_id = request.GET.get('c_id')
    c_id_url = None
    if c_id:
        if c_id.isdigit():
            queryset = queryset.filter(product_category__id__exact=c_id)
            c_id_url = 'c_id={0}'.format(c_id)
    if not page:
        page = 1
    if queryset and url_reverse:
        paginator = Paginator(queryset, per_page_count)
        current_page_data = paginator.get_page(page)
        next_page = None
        if current_page_data.has_next():
            if c_id_url:
                next_page = '?page={0}&{1}'.format(current_page_data.next_page_number(), c_id_url)
            else:
                next_page = '?page={0}'.format(current_page_data.next_page_number())
            next_page = HttpRequest.build_absolute_uri(request, next_page)
        return current_page_data, next_page
    else:
        return None, None


@jwt_required
@require_http_methods(["GET"])
def category_list(request):
    c_list = list()
    c_list.append({'c_id': 0, 'category': '全部'})
    queryset = ProductCategory.objects.filter(is_show=True)
    if request.content_type == 'application/json' and queryset.exists():
        for c in queryset:
            if c.product_amount:
                c_list.append({'c_id': c.pk, 'category': c.product_category_cn})
        return JsonResponse({'results': c_list}, status=status.HTTP_200_OK)
    return JsonResponse({'results': c_list}, status=status.HTTP_200_OK)


@jwt_required
@require_http_methods(["GET"])
def product_list(request):
    """
    返回有库存的产品列表，并且判断是否有下一页
    """
    queryset = Product.objects.filter(is_show=True).order_by('index')
    jwt_token = request.META.get('HTTP_JWT')
    logger.info("jwt_token: {0}".format(jwt_token))
    if jwt_token:
        client = token_verify(jwt_token.encode('utf-8'))
        if client:
            # TODO 查询用户的权限，根据不同的权限返回不同的信息
            current_page_data, next_page = page_data(
                request, queryset=queryset, url_reverse='{0}-api:products_api'.format(app_name))
            return JsonResponse(
                {
                    'results': product_to_array(current_page_data, level=client.client_level_id),
                    'next': next_page
                },
                status=status.HTTP_200_OK
            )
    current_page_data, next_page = page_data(request, queryset=Product.objects.none(),
                                             url_reverse='{0}-api:products_api'.format(app_name))
    return JsonResponse(
        {'results': product_to_array(current_page_data, level=None), 'next': next_page},
        status=status.HTTP_200_OK
    )


@require_http_methods(["GET"])
@jwt_required
def product_detail(request, pk):
    product = Product.objects.filter(pk=pk)
    if request.method == "GET":
        if product.exists():
            product = product.first()
            return JsonResponse({'results': product_to_dict(product)}, status=status.HTTP_200_OK)
    return JsonResponse({'results': None}, status=status.HTTP_200_OK)


@csrf_exempt
@require_http_methods(["POST"])
def submit(request):
    if request.method == "POST" and request.content_type == 'application/json':
        if request.body:
            received_data = json.loads(request.body.decode('utf-8'))
            logger.info("received_data: {0}".format(received_data))
            order_info = received_data.get('order_info')
            total_number = received_data.get('total_number')
            total_price = received_data.get('total_price')
            jwt_token = received_data.get('jwt')
            if jwt_token:
                user = token_verify(jwt_token.encode('utf-8'))
                if user:
                    if total_number is not None:
                        if total_number > 0:
                            sale_order_code = '{0}{1}'.format(tid_maker(), total_number)
                            notes = '微信小程序订单:数量:{0},金额:{1}元'.format(total_number, total_price)
                            sale_order = SaleOrder(
                                sale_order_code=sale_order_code,
                                sale_order_date=timezone.localdate(),
                                order_state_id=1,
                                client_id=user.pk,
                                notes=notes,
                                is_from_wx=True
                            )
                            sale_order.save()
                            packs_selected = list()
                            for od in order_info:
                                product_pk = od.get('pk')
                                product_amount = od.get('num')
                                price_each = od.get('price')
                                packs = Pack.objects.filter(
                                    product_id=product_pk).filter(state=True).order_by('-pk')
                                for p_b in packs:
                                    if product_amount <= p_b.pack_num_left:
                                        packs_selected.append(
                                            {'pack_id': p_b.pk,
                                             'sale_num': product_amount,
                                             'price_each': price_each
                                             })
                                        break
                                    else:
                                        if p_b.amount_left > 0:
                                            packs_selected.append(
                                                {'pack_id': p_b.pk,
                                                 'sale_num': p_b.amount_left,
                                                 'price_each': price_each
                                                 })
                                            product_amount = product_amount - p_b.amount_left
                            logger.info("packs_selected: {0}".format(packs_selected))
                            total_price_new = 0
                            if len(packs_selected) > 0:
                                for s in packs_selected:
                                    sale_price = s.get('price_each') * s.get('sale_num')
                                    money_io = MoneyInOut(
                                        money_in_out=sale_price,
                                        money_in_out_date=timezone.localdate(),
                                        money_in_out_type_id=2,  # TODO check money_io_type
                                    )
                                    money_io.save()
                                    sale = Sale(
                                        sale_order=sale_order,
                                        sale_date=timezone.localdate(),
                                        pack_id=s.get('pack_id'),
                                        sale_num=s.get('sale_num'),
                                        sale_price=sale_price,
                                        sale_price_link=money_io,
                                    )
                                    sale.save()
                                    total_price_new += sale_price
                                    logger.info("sale saved: {0}".format(sale))
                            logger.info("total_price_new: {0}".format(total_price_new))
                            return HttpResponse(
                                json.dumps({'price': total_price_new}),
                                content_type="application/json",
                                status=status.HTTP_200_OK)
    return HttpResponse(json.dumps({'data': 'request method wrong', 'price': 0}),
                        content_type="application/json",
                        status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
@require_http_methods(["POST"])
def add_address(request):
    if request.method == "POST" and request.content_type == 'application/json':
        if request.body:
            received_data = json.loads(request.body.decode('utf-8'))
            logger.info("received_data: {0}".format(received_data))
            address_info = received_data.get('address_info')
            jwt_token = received_data.get('jwt')
            if jwt_token and address_info:
                user = token_verify(jwt_token.encode('utf-8'))
                if user:
                    client_address = ClientAddress(
                        client=user,
                        user_name=address_info.get('userName'),
                        postal_code=address_info.get('postalCode'),
                        province_name=address_info.get('provinceName'),
                        city_name=address_info.get('cityName'),
                        county_name=address_info.get('countyName'),
                        detail_info=address_info.get('detailInfo'),
                        tel_number=address_info.get('telNumber'),
                    )
                    client_address.save()
                    logger.info("address saved: {0}".format(client_address.pk))
                    return HttpResponse(
                        json.dumps({'address': client_address.pk}),
                        content_type="application/json",
                        status=status.HTTP_200_OK)
    return HttpResponse(json.dumps({'data': 'request method wrong', 'price': 0}),
                        content_type="application/json",
                        status=status.HTTP_400_BAD_REQUEST)


class SaleNumberListView(generics.ListAPIView):
    serializer_class = SaleOrderSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_fields = ('order_state__id',)

    def get_queryset(self):
        jwt_token = self.request.META.get('HTTP_JWT')
        logger.info("jwt_token: {0}".format(jwt_token))
        if jwt_token:
            client = token_verify(jwt_token.encode('utf-8'))
            if client:
                queryset = SaleOrder.objects.filter(client=client)
                return queryset
        return SaleOrder.objects.none()


class BannerListView(generics.ListAPIView):
    serializer_class = BannerSerializer
    queryset = Product.objects.filter(is_banner=True).filter(is_show=True)

    @method_decorator([jwt_required])
    def dispatch(self, request, *args, **kwargs):
        return super(__class__, self).dispatch(request, *args, **kwargs)


class OrderStateView(generics.ListAPIView):
    serializer_class = OrderStateSerializer
    queryset = OrderState.objects.all()

    @method_decorator([jwt_required])
    def dispatch(self, request, *args, **kwargs):
        return super(__class__, self).dispatch(request, *args, **kwargs)


class ClientAddressView(generics.ListAPIView):
    serializer_class = ClientAddressSerializer

    def get_queryset(self):
        jwt_token = self.request.META.get('HTTP_JWT')
        logger.info("jwt_token: {0}".format(jwt_token))
        if jwt_token:
            client = token_verify(jwt_token.encode('utf-8'))
            if client:
                queryset = ClientAddress.objects.filter(client=client)
                return queryset
        return ClientAddress.objects.none()

    @method_decorator([jwt_required])
    def dispatch(self, request, *args, **kwargs):
        return super(__class__, self).dispatch(request, *args, **kwargs)
