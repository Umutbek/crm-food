from django.urls import path
from user import views


app_name = 'user'

urlpatterns = [
    path('role/', views.RoleView.as_view(), name='role'),
    path('create/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('me/', views.ManageUserView.as_view(), name='me'),
    path('password-change/', views.PasswordChangeView.as_view()),
]
