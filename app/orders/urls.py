from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orders import views

router =DefaultRouter()
router.register('Table', views.TableViewSet)
router.register('Status', views.StatusViewSet)
router.register('ServicePercentage', views.ServicePercentageViewSet)
router.register('Order', views.OrderViewSet)
router.register('Checks', views.ChecksViewSet)

app_name = 'orders'

urlpatterns = [
    path('', include(router.urls)),
    path('MealsToOrder', views.MealsToOrderListView.as_view()),
]
