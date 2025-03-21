
from django.contrib import admin
from django.urls import path,include
from home.views import *

urlpatterns = [
    path('animals/',AnimalView.as_view(),),
    path('register/',RegisterAPI.as_view(),),
    path('login/',loginAPI.as_view(),),
    path('crud/',AnimalCreateAPI.as_view(),)
]
