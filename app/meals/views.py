from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated

from core.models import Department, MealCateg, Meal

from meals import serializers

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from django_filters import FilterSet
from django_filters import rest_framework as filters

class DepartmentViewSet(viewsets.ModelViewSet):
    """Manage department in the db"""
    queryset = Department.objects.all()
    serializer_class = serializers.DepartmentSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        """Return object for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self,serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class MealCategoryFilter(FilterSet):
    """Filter for an item"""
    id = filters.CharFilter('depid__id')


    class Meta:
        models = MealCateg
        fields = ('id',)


class MealCategoryViewSet(viewsets.ModelViewSet):
    """Manage meal category in the db"""
    queryset = MealCateg.objects.all()
    serializer_class = serializers.MealCategSerializer

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_class = MealCategoryFilter


    def get_queryset(self):
        """Return object for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self,serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)


class MealFilter(FilterSet):
    """Filter for an item"""
    id = filters.CharFilter('category__id')


    class Meta:
        models = MealCateg
        fields = ('id',)


class MealsViewSet(viewsets.ModelViewSet):
    """Manage meals in the db"""
    serializer_class = serializers.MealsSerializer
    queryset = Meal.objects.all()

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    filter_backends = (DjangoFilterBackend, SearchFilter)
    filter_class = MealFilter

    def get_queryset(self):
        """Return object for the current authenticated user only"""
        return self.queryset.filter(user=self.request.user).order_by('-name')

    def perform_create(self,serializer):
        """Create a new object"""
        serializer.save(user=self.request.user)
