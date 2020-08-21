from django.urls import path, include
from rest_framework.routers import DefaultRouter

from meals import views

router =DefaultRouter()
router.register('Department', views.DepartmentViewSet)
router.register('MealCategory', views.MealCategoryViewSet)
router.register('Meals', views.MealsViewSet)


app_name = 'meals'

urlpatterns = [
    path('', include(router.urls))
]
