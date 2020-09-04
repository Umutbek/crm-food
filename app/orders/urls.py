from django.urls import path, include
from rest_framework.routers import DefaultRouter

from orders import views

router =DefaultRouter()
router.register('Table', views.TableViewSet)
router.register('Status', views.StatusViewSet)
router.register('ServicePercentage', views.ServicePercentageViewSet)
router.register('Order', views.OrderViewSet)
router.register('MealsToOrder', views.MealsToOrderViewSet)
router.register('Checks', views.ChecksViewSet)

app_name = 'orders'

urlpatterns = [
    path('', include(router.urls)),
    path('ActiveOrders/', views.ActiveOrdersView.as_view(), name='ActiveOrders')
]
