from rest_framework import serializers
from core import models
from meals.serializers import MealsSerializer

class TableSerializer(serializers.ModelSerializer):
    """Serializer for table objects"""

    class Meta:
        model = models.Table
        fields = ('id', 'name')

        read_only_fields = ('id',)


class StatusSerializer(serializers.ModelSerializer):
    """Serializer for table objects"""

    class Meta:
        model = models.Status
        fields = ('id', 'name')

        read_only_fields = ('id',)


class ServicePercentageSerializer(serializers.ModelSerializer):
    """Serializer for table objects"""

    class Meta:
        model = models.ServicePercentage
        fields = ('id', 'percentage')

        read_only_fields = ('id',)

class MealsToOrderSerializer(serializers.ModelSerializer):
    mealsid = serializers.PrimaryKeyRelatedField(queryset=models.Meal.objects.all(), source='mealsid.id')
    name = serializers.CharField(source='mealsid.name', read_only=True)

    class Meta:
        model = models.MealsToOrder
        fields = ('mealsid', 'name', 'count')


class OrderMealSerializer(serializers.ModelSerializer):
    id = serializers.PrimaryKeyRelatedField(queryset=models.Meal.objects.all(), source='meal.id', )
    name = serializers.CharField(source='meal.name', read_only=True)
    price = serializers.CharField(source='meal.price', read_only=True)
    total = serializers.FloatField(source='get_sum', read_only=True)

    class Meta:
        model = models.MealsToOrder
        fields = ('id', 'name', 'count', 'price', 'total')

class OrderSerializer(serializers.ModelSerializer):
    """Serializer for table objects"""
    mealsid = MealsToOrderSerializer(many=True, required=False, source='orderid')
    tableid = serializers.PrimaryKeyRelatedField(queryset=models.Table.objects.all())
    tablename = serializers.CharField(source='tableid.name', read_only=True)
    class Meta:
        model = models.Order
        fields = ('id', 'waiterid', 'tableid', 'tablename', 'date', 'is_open', 'mealsid')

        read_only_fields = ('id',)


class CheckMealsSerializer(serializers.ModelSerializer):
    meals_order = OrderMealSerializer(many=True)

    class Meta:
        model = models.Order
        fields = ('meals_order',)


class CheckSerializer(serializers.ModelSerializer):
    orderid = serializers.PrimaryKeyRelatedField(queryset= models.Order.objects.all())
    servicefee = serializers.FloatField(read_only=True)
    meals = CheckMealsSerializer(many=True, read_only=True)
    totalsum = serializers.FloatField(source='get_total', read_only=True)

    class Meta:
        model = models.Checks
        fields = ['id', 'orderid', 'date', 'servicefee', 'totalsum', 'meals']
        read_only_fields = ('id',)
