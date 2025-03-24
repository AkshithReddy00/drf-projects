from rest_framework.response import Response
from rest_framework.decorators import action
from home.models import Blog
from home.serializers import BlogDetailSerializer
from .permissions import *
from rest_framework.authentication import TokenAuthentication

class BlogMixin:
    @action(detail=False,methods=['GET'])
    def blog_detail(self,request):
        try:
            blog_obj = Blog.objects.all()
            return Response({
                'status':True,
                'message':'blog details',
                'data': BlogDetailSerializer(blog_obj,many=True).data          
            })         
        except Exception as e:
            print(e)
            return Response({
                'status':False,
                'message':'invalid blog id'               
            })

    @action(detail=True,methods=['PATCH'],permission_classes = [IsOwner],authentication_classes = [TokenAuthentication])
    def blog_update(self,request,pk):
        try:
            blog_obj = self.get_object()
            data = request.data
            serializer = self.serializer_class(blog_obj,data = data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status':True,
                    'message':'blog update',
                    'data': serializer.data
                })    
            return Response({
                    'status':True,
                    'message':'blog not update',
                    'data': serializer.errors
                })   
        except Exception as e:
            print(e)
            return Response({
                'status':False,
                'message':'invalid blog id'               
            })