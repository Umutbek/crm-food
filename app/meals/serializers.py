from rest_framework import serializers

from core.models import Department, MealCateg, Meal

class DepartmentSerializer(serializers.ModelSerializer):
    """Serializer for department objects"""

    class Meta:
        model = Department
        fields = ('id', 'name')

        read_only_fields = ('id',)


class MealCategSerializer(serializers.ModelSerializer):
    """Serializer for meal's category objects"""

    class Meta:
        model = MealCateg
        fields = ('id', 'name', 'depid')

        read_only_fields = ('id',)


class MealsSerializer(serializers.ModelSerializer):
    """Serializer for meals objects"""

    class Meta:
        model = Meal
        fields = ('id', 'name', 'category', 'price', 'description')

        read_only_fields = ('id',)
