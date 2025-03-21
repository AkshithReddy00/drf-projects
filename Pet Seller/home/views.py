from rest_framework.views import APIView
from rest_framework.response import Response
from .models import (Animal)
from .serializers import (AnimalSerializer,RegisterSerializer,LoginSerializer)
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from rest_framework.authtoken.models import Token
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from .permissions import IsPetOwnerPermission
from rest_framework.pagination import PageNumberPagination
import uuid

class AnimalPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class AnimalView(APIView):
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        queryset = Animal.objects.all()
        search = request.GET.get('search', '').strip()
        print(search)
        if search:
            queryset = queryset.filter(
                Q(animal_name__icontains=search) |
                Q(animal_description__icontains=search) |
                Q(animal_color__animal_color__icontains=search) |
                Q(animal_breed__animal_breed__icontains=search) |
                Q(animal_gender__iexact=search)
            ).distinct()

        paginator = AnimalPagination()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = AnimalSerializer(result_page, many=True)
        return paginator.get_paginated_response({
            'status': True,
            'message': "Animals fetched successfully",
            'data': serializer.data
        })
    
class RegisterAPI(APIView):
    
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = RegisterSerializer(data = data)
            
            if serializer.is_valid():
                user = serializer.save()

                return Response({
                    'status':True,
                    'message':'account created',
                    'data':{}
                })
            return Response({
                'status':False,
                'message':'account not created',
                'data':serializer.errors
            })            

        except Exception as e:
            return Response({
                'status':False,
                'message':'account not created',
                'data':serializer.errors
            })  

class loginAPI(APIView):
    permission_classes = [AllowAny]
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            serializer = LoginSerializer(data = data)

            if serializer.is_valid():
                username = serializer.validated_data['username']
                password = serializer.validated_data['password']
                user = authenticate(username=username,password=password)
                token,_ = Token.objects.get_or_create(user = user)
                if user:
                    return Response({
                        'message':'login success',
                        'status':True,
                        'data':{
                            'token':str(token)
                        }
                    })
                
            return Response({
                    'status':False,
                    'message':'Invalid credentials',
                    'data':serializer.errors
                })
        except Exception as e:
            return Response({
                'status':False,
                'message':'something went wrong',
                'data':{}
            })  
        
class AnimalCreateAPI(APIView):
    permission_classes = [IsAuthenticated,IsPetOwnerPermission]
    authentication_classes = [TokenAuthentication]

    def get(self, request, *args, **kwargs):
        queryset = Animal.objects.filter(animal_owner = request.user)

        if request.GET.get('search'):
            search = request.GET.get('search')
            queryset = queryset.filter(Q(animal_name__icontains = search)|
                                       Q(animal_description__icontains = search)|
                                       Q(animal_color__animal_color__icontains = search)|
                                       Q(animal_breed__animal_breed__icontains = search)|
                                       Q(animal_gender__iexact = search))
        serializer = AnimalSerializer(queryset,many = True)
        return Response({
            'status':True,
            'message':"animals fetched",
            'data': serializer.data
        })
    
    def post(self, request, *args, **kwargs):
        try:
            data = request.data
            data['animal_owner'] = request.user.id
            serializer = AnimalSerializer(data = data)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status':True,
                    'message':'animal Created',
                    'data':serializer.data
                })
            return Response({
                'status':False,
                'message':'invalid data',
                'data':serializer.errors
            })
        except Exception as e:
            print(e)
            return Response({
                'status': False,
                'message': 'Something went wrong. Please try again later.',
                'data': {}
            })
        
    def patch(self, request, *args, **kwargs):
        try:
            data = request.data

            # Validate UUID
            if 'uuid' not in data:
                return Response({
                    'status': False,
                    'message': 'Animal ID (uuid) is required',
                    'data': {}
                }, status=status.HTTP_400_BAD_REQUEST)

            try:
                # Validate UUID format
                uuid.UUID(data['uuid'])
            except ValueError:
                return Response({
                    'status': False,
                    'message': 'Invalid UUID format',
                    'data': {}
                }, status=status.HTTP_400_BAD_REQUEST)

            # Fetch the Animal object
            animal_obj = Animal.objects.filter(uuid=data['uuid'])
            if not animal_obj.exists():
                return Response({
                    'status': False,
                    'message': 'Invalid animal ID',
                    'data': {}
                }, status=status.HTTP_404_NOT_FOUND)
            
            animal_obj = animal_obj.first()
            
            self.check_object_permissions(request,animal_obj)

            # Update the Animal object
            serializer = AnimalSerializer(instance=animal_obj, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'status': True,
                    'message': 'Animal updated successfully',
                    'data': serializer.data
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': False,
                    'message': 'Invalid data',
                    'data': serializer.errors
                }, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            # Log the error (replace print with proper logging)
            print(f"Error: {e}")
            return Response({
                'status': False,
                'message': 'Something went wrong or you do not have permission to perofrm this action',
                'data': {}
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request, *args, **kwargs):
        data = request.data
            # Validate UUID
        if 'uuid' not in data:
            return Response({
                'status': False,
                'message': 'Animal ID (uuid) is required',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Validate UUID format
            uuid.UUID(data['uuid'])
        except ValueError:
            return Response({
                'status': False,
                'message': 'Invalid UUID format',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)

        
        animal_obj = Animal.objects.filter(uuid=data['uuid']).delete()
        return Response({
                'status': False,
                'message': 'Animal object Deleted Successfully',
                'data': {}
            }, status=status.HTTP_200_OK)
