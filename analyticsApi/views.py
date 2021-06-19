from django.shortcuts import render


from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import filters
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse,Http404
from analyticsApi.serializers import SignUpSerializer, AdminSignUpSerializer,ActivationSerializer, ActivateSerializer
from rest_framework import serializers,status
from .models import *
import datetime
import jwt
from django.core.checks import messages


# Create your views here.
class RegisterApiView(generics.CreateAPIView):
  serializer_class = SignUpSerializer
  def post(self, request):
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      user_data =serializer.data
      response={
        "data":{
            "user":dict(user_data),
            "status":"success",
            "message":"user added successfully",
        }
      }
      return Response(response, status=status.HTTP_201_CREATED)
    else:
      return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


# admin registration
class AdminRegisterApiView(generics.CreateAPIView):
  serializer_class = AdminSignUpSerializer
  def post(self, request):
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save()
      user_data =serializer.data
      response={
        "data":{
            "user":dict(user_data),
            "status":"success",
            "message":"admin added successfully",
        }
      }
      return Response(response, status=status.HTTP_201_CREATED)
    else:
      return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

# user login
class LoginApiView(APIView):
  def post(self, request):
    phone_number = request.data['phone_number']
    password =request.data['password']
    user = User.objects.filter(phone_number=phone_number).first()
    if user is None:
      raise AuthenticationFailed("User not Found")
    if not user.check_password(password):
      raise AuthenticationFailed("incorrect password ")
    payload = {
      'id':user.userId,
      'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
      'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    response = Response()
    response.set_cookie(key='jwt',value=token,httponly=True)
    response.data = {"jwt": token}
    return response

# fetching one user instance
class UserAPIView(APIView):
  def get(self, request):
    token = request.COOKIES.get('jwt')
    if not token:
      raise AuthenticationFailed("Unauthenticated")
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed("Unauthenticated")
    user = User.objects.filter(userId=payload['id']).first()
    serializer = SignUpSerializer(user)
    return Response(serializer.data)

#Logout view
class LogoutAPIView(APIView):
  def post(self, request):
    response = Response()
    response.delete_cookie('jwt')
    response.data = {"message":"successfully logged out"}

    return response


class ActivationApiView(generics.CreateAPIView):
  serializer_class = ActivationSerializer

  def post(self,request, phone_number,format=None):
    user = User.objects.get(phone_number=phone_number)
    
    serializer = self.serializer_class(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save(user = user)
      Activation_data= serializer.data
      response={
        "data":{
            "User Documents":dict(serializer.data),
            "status":"success",
            "message":"Documents  added successfully",
        }
      }
      return Response(response, status=status.HTTP_201_CREATED)
    else:
      return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)

class ActivateUserApiView(APIView):
  def get_user(self, phone_number):
        try:
            return User.objects.get(phone_number=phone_number)
        except:
            return Http404

  def get(self, request, phone_number, format=None):
    user=self.get_user(phone_number)
    serializers=ActivateSerializer(user)
    return Response(serializers.data)

  # update user to a valid user
  def patch(self, request, phone_number, format=None):
    user=self.get_user(phone_number)
    serializers=ActivateSerializer(user, request.data, partial=True)
    if serializers.is_valid(raise_exception=True):
      serializers.save(is_valid=True)
      valid_user=serializers.data

      return Response(valid_user)
    return Response(status.errors, status=status.HTTP_400_BAD_REQUEST)




