from django.urls import path,include
from home.views import BlogView
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'blog', BlogView, basename='blog')

urlpatterns = [
    path('',include(router.urls))
]

