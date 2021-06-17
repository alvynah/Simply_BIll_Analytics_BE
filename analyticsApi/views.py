from django.shortcuts import render


from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import filters
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse
from analyticsApi.serializers import SignUpSerializer
from rest_framework import serializers,status

# Create your views here.
class RegisterApiView(APIView):
  def post(self, request):
    serializer = SignUpSerializer(data=request.data)
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