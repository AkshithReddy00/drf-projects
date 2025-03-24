from django.db import models
from django.contrib.auth.models import User
import uuid
# Create your models here.

class BaseModel(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4,editable=False,primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    class Meta:
        abstract = True

class Blog(BaseModel):
    blog_title = models.CharField(max_length=100)
    blog_description = models.TextField()
    is_paid = models.BooleanField(default=False)
    blog_owner = models.ForeignKey(User,on_delete=models.SET_NULL,null = True,blank=True)

class Subscription(BaseModel):
    subscription_name = models.CharField(max_length=100)
    subscription_days = models.IntegerField(default=30)
    subscription_price = models.IntegerField()

class SubscriptionOrder(BaseModel):
    user = models.ForeignKey(User,on_delete=models.SET_NULL,null = True,blank=True)
    subscription = models.ForeignKey(Subscription,on_delete=models.CASCADE)
    subscription_end_date = models.DateField()
    is_paid = models.BooleanField(default=False)