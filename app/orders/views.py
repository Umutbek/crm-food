from rest_framework import viewsets, mixins, status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core import models

from rest_framework.views import APIView
from orders import serializers
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django_filters import FilterSet
from django_filters import rest_framework as filters

class TableViewSet(viewsets.ModelViewSet):
    """Manage department in the db"""
    queryset = models.Table.objects.all()
    serializer_class = serializers.TableSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return object for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self,serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class StatusViewSet(viewsets.ModelViewSet):
    """Manage meal category in the db"""
    queryset = models.Status.objects.all()
    serializer_class = serializers.StatusSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        """Return object for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self,serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class ServicePercentageViewSet(viewsets.ModelViewSet):
    """Manage meals in the db"""
    serializer_class = serializers.ServicePercentageSerializer
    queryset = models.ServicePercentage.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return object for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-percentage')

    def perform_create(self,serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    """Manage meal category in the db"""
    queryset = models.Order.objects.all()
    serializer_class = serializers.OrderSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    def get_queryset(self):
        """Return object for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self,serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class ChecksViewSet(viewsets.ModelViewSet):
    """Manage meals in the db"""
    serializer_class = serializers.CheckSerializer
    queryset = models.Checks.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return object for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user)

    def perform_create(self,serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class MealsToOrderListView(APIView):
    def get(self, request):
        order = models.Order.objects.filter(id=request.data['orderid'])
        serializer = serializers.OrdersSerializer(order, many=True)
        return Response(serializer.data)

    def post(self, request):
        order = models.Order.objects.filter(id=request.data['orderid'])
        data = request.data['meals']
        meal = models.MealsToOrder.objects.filter(id=data['id'])
        models.MealsToOrder.objects.create(order=order, meal=meal, count=data['count'])

    def delete(self, request):
        data = request.data
        order = models.Order.objects.filter(id=request.data['orderid'])
        meal = models.Order.objects.filter(id=data['meaidid'])
