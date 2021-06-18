from django.urls import path,re_path
from django.urls.resolvers import URLPattern
from . import views


urlpatterns = [
path('api/user/register/', views.RegisterApiView.as_view(), name="register"),
path('api/admin/register/', views.AdminRegisterApiView.as_view(), name="admin-register"),
path('api/user/login/', views.LoginApiView.as_view(), name="user-login"),
path('api/user/current-user/', views.UserAPIView.as_view(), name="fetch-user"),
path('logout/', views.LogoutAPIView.as_view(), name="logout"),
path('api/activation-post/<int:phone_number>/', views.ActivationApiView.as_view(), name="ActivationPost"),



]