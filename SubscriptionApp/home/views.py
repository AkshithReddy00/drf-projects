from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework import viewsets
from home.models import Blog
from home.serializers import BlogSerializer,BlogDetailSerializer
from .mixins import BlogMixin
# Create your views here.

class BlogView(viewsets.ModelViewSet,BlogMixin):
    queryset = Blog.objects.all()
    serializer_class = BlogDetailSerializer

    def list(self, request, *args, **kwargs):
        return Response({
            'status':'True',
            'message':'blogs fetched',
            'data':{
            'count':self.queryset.count(),
            'blogs':BlogSerializer(self.queryset,many=True).data}
        })