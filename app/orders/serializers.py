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
    """Serializer for Status"""

    class Meta:
        model = models.Status
        fields = ('id', 'name')

        read_only_fields = ('id',)


class ServicePercentageSerializer(serializers.ModelSerializer):
    """Serializer for ServicePercentage"""

    class Meta:
        model = models.ServicePercentage
        fields = ('id', 'percentage')

        read_only_fields = ('id',)

class OrderedMealsSerializer(serializers.ModelSerializer):
    """Ordered meals with name and count, Used to get MealsToOrder"""
    meal = serializers.PrimaryKeyRelatedField(queryset=models.Meal.objects.all())
    name = serializers.CharField(source='meal.name', read_only=True)

    class Meta:
        model = models.OrderedMeals
        fields = ('meal', 'name', 'count')


class MealsToOrderSerializer(serializers.ModelSerializer):
    """Serializer for MealsToOrder objects"""
    ordid = serializers.PrimaryKeyRelatedField(queryset= models.Order.objects.all())
    mealss = OrderedMealsSerializer(many=True)

    class Meta:
        model = models.MealsToOrder
        fields = ('ordid', 'mealss')

    def create(self, validated_data):
        """create method for Order serializer"""
        mealss = validated_data.pop("mealss")
        mealstoorder= models.MealsToOrder.objects.create(**validated_data)

        for m in mealss:
            models.OrderedMeals.objects.create(mealstoorder=mealstoorder, **m)

        return mealstoorder

class OrderMealSerializer(serializers.ModelSerializer):
    """Serializer for ordered meals, Used to get Checks"""
    id = serializers.PrimaryKeyRelatedField(queryset=models.Meal.objects.all(), source='meal.id', )
    name = serializers.CharField(source='meal.name', read_only=True)
    price = serializers.CharField(source='meal.price', read_only=True)
    total = serializers.FloatField(source='get_sum', read_only=True)

    class Meta:
        model = models.OrderedMeals
        fields = ('id', 'name', 'count', 'price', 'total')

class OrderSerializer(serializers.ModelSerializer):
    """Serializer for Order"""
    tableid = serializers.PrimaryKeyRelatedField(queryset=models.Table.objects.all())
    tablename = serializers.CharField(source='tableid.name', read_only=True)
    meals = OrderedMealsSerializer(many=True)

    class Meta:
        model = models.Order
        fields = ('id', 'waiterid', 'tableid', 'tablename', 'date', 'is_open', 'meals')

        read_only_fields = ('id', 'waiterid', 'is_open')


    def create(self, validated_data):
        """create method for Order serializer"""
        meals = validated_data.pop("meals")
        order = models.Order.objects.create(**validated_data)

        for m in meals:
            models.OrderedMeals.objects.create(order=order, **m)

        return order


class CheckMealsSerializer(serializers.ModelSerializer):
    """Assign ordered meals to meals_order var to get checks"""
    meals_order = OrderMealSerializer(many=True)

    class Meta:
        model = models.Order
        fields = ('meals_order',)


class CheckSerializer(serializers.ModelSerializer):
    """Serializer for Checks"""
    orderid = serializers.PrimaryKeyRelatedField(queryset= models.Order.objects.all())
    servicefee = serializers.FloatField(source='servicefee.percentage', read_only=True)
    meals = CheckMealsSerializer(many=True, read_only=True)
    totalsum = serializers.FloatField(source='get_total', read_only=True)

    class Meta:
        model = models.Checks
        fields = ['orderid', 'date', 'servicefee', 'totalsum', 'meals']


    def create(self, validated_data):
        """create method for Order serializer"""
        checks = models.Order.objects.create(**validated_data)
        return checks
