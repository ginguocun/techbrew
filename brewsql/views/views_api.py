from rest_framework import generics
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework.permissions import IsAuthenticated, DjangoObjectPermissions

from ..serializers import *

app_name = '{0}_api'.format(GeneralConfig.name)


class PackList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, DjangoObjectPermissions)
    queryset = Pack.objects.all()
    serializer_class = PackSerializer


class PackDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, DjangoObjectPermissions)
    queryset = Pack.objects.all()
    serializer_class = PackSerializer


class SaleList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, DjangoObjectPermissions)
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


class SaleDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, DjangoObjectPermissions)
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer


class BrewList(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated, DjangoObjectPermissions)
    queryset = Brew.objects.all()
    serializer_class = BrewSerializer


class BrewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, DjangoObjectPermissions)
    queryset = Brew.objects.all()
    serializer_class = BrewSerializer


@api_view(['GET'])
def api_root(request, api_format=None):
    return Response({
        'sales': reverse('{0}-api:sale-list'.format(GeneralConfig.name), request=request, format=api_format),
        'packs': reverse('{0}-api:pack-list'.format(GeneralConfig.name), request=request, format=api_format),
        'brews': reverse('{0}-api:brew-list'.format(GeneralConfig.name), request=request, format=api_format),
        'brew_excel': reverse('{0}-api:brew-xls'.format(GeneralConfig.name), request=request, format=api_format),
        'sale_excel': reverse('{0}-api:sale-xls'.format(GeneralConfig.name), request=request, format=api_format),
    })
