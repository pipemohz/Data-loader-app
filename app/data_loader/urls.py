from django.urls import path
from . import views

app_name = "data_loader"

urlpatterns = [
    path('', views.index),
    path("index/", views.index, name="index"),
    path("upload/", views.upload, name="upload"),
    path("process/", views.process, name="process")
]