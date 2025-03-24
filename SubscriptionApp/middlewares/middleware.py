from home.models import Subscription,SubscriptionOrder
from rest_framework.response import Response
from django.http import JsonResponse
import datetime

class SubscriptionCheck(object):
    def __init__(self,get_response):
        self.get_response = get_response

    def __call__(self, request):
        url_path = set((request.path).split('/'))

        if 'blog_detail' in url_path:
            if not request.user.is_authenticated:
                return JsonResponse({
                    'status':False,
                    'message':'you are not authenticated',
                    'data':{}
                },content_type = "application/json")
            
            subscription_order = SubscriptionOrder.objects.filter(
                user = request.user,
                is_paid = True,
                subscription_end_date__gte = datetime.datetime.today().date())
            
            if not subscription_order.exists():
                return JsonResponse({
                    'status':False,
                    'message':'you have not purchased the subscription',
                    'data':{}
                },content_type = "application/json")           
        return self.get_response(request)