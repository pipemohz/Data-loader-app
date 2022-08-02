from django.urls import path
from . import views

app_name = "data_loader"

urlpatterns = [
    path('', views.index),
    path("index/", views.index, name="index"),
    path("process_file/", views.process_file, name="process_file"),
    path("process_group/", views.process_group, name="process_group")
]
