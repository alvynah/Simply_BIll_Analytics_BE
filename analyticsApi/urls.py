from django.urls import path,re_path
from django.urls.resolvers import URLPattern
from . import views


urlpatterns = [
path('api/user/register/', views.RegisterApiView.as_view(), name="register"),
path('api/admin/register/', views.AdminRegisterApiView.as_view(), name="admin-register"),

]