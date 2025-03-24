from rest_framework import serializers
from home.models import *

class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = ["blog_title","uuid"]

class BlogDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        exclude = ["updated_at"]



    
