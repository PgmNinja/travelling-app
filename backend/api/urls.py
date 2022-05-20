
from django.urls import path
from . import views

urlpatterns = [
    path('packages/', views.PackageAPI.as_view())
]