from django.urls import path,re_path
from django.urls.resolvers import URLPattern
from . import views


urlpatterns = [
path('api/register/', views.RegisterApiView.as_view(), name="register"),


]