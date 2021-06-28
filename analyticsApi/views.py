from django.shortcuts import render


from rest_framework.exceptions import AuthenticationFailed
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import filters
from rest_framework.parsers import JSONParser
from django.http.response import JsonResponse,Http404
from analyticsApi.serializers import *
from rest_framework import serializers,status
from .models import *
import datetime
import jwt
from django.core.checks import messages
from .email import *



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
    activation = Activation.objects.filter(user=user).first()
   
    if user is None:
      raise AuthenticationFailed("User not Found")
    name=user.first_name
    email=user.email
    if activation is None and user.is_admin == False:
      send_notify_email(name,email,phone_number)
      raise AuthenticationFailed("Please Submit documents")  
    elif user.is_valid == False:
      raise AuthenticationFailed("Please wait for your documents to be approved") 
    if not user.check_password(password):
      raise AuthenticationFailed("incorrect password ")
    payload = {
      'id':user.userId,
      'exp':datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
      'iat': datetime.datetime.utcnow()
    }
    token = jwt.encode(payload, 'secret', algorithm='HS256')
    response = Response()
    response.set_cookie(key='jwt',value=token,httponly=True, samesite="none",secure=True)
    response.data = {"jwt": token}
    return response

class LoginAdminApiView(APIView):
  def post(self, request):
    phone_number = request.data['phone_number']
    password =request.data['password']
    user = User.objects.filter(phone_number=phone_number).first()
    if user is None:
      raise AuthenticationFailed("User not Found")
    if  user.is_admin == False:
      raise AuthenticationFailed("You have no admin rights!")  
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
      raise AuthenticationFailed("Unauthenticated Not Token")
    try:
        payload = jwt.decode(token, 'secret', algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
      raise AuthenticationFailed("Unauthenticated")
    user = User.objects.filter(userId=payload['id']).first()
    serializer = CurrentUserSerializer(user)
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
    user=self.get_user(phone_number=phone_number)
    name=user.first_name
    email=user.email
    serializers=ActivateSerializer(user, request.data, partial=True)
    
    if serializers.is_valid(raise_exception=True):
      serializers.save(is_valid=True)
      send_success_email(name,email)
      valid_user=serializers.data 

      return Response(valid_user)
    return Response(status.errors, status=status.HTTP_400_BAD_REQUEST)


class GetAllUsers(APIView):
  serializer_class=CurrentUserSerializer

  def get(self, request, format=None):
    customer_users=User.objects.filter(is_valid=False, is_customer=True)
    serializers=self.serializer_class(customer_users, many=True)
    return Response(serializers.data)


class GetOneUserDocuments(APIView):
  serializers_class=ApprovalSerializer

  def get (self, request, phone_number, format=None):
    user = User.objects.filter(phone_number=phone_number).first()
    activation = Activation.objects.filter(user=user).first()
    serializer =self.serializers_class(activation)
    return Response(serializer.data)

class NotifyUserToUpload(APIView):
   def post(self,request, phone_number,format=None):
    user = User.objects.get(phone_number=phone_number)

    name=user.first_name
    email=user.email
    phone_number=user.phone_number

    send_notify_email(name,email,phone_number)

    response={
        "data":{
            "status":"success",
            "message":"email sent successfully",
        }
      }
    return Response(response, status=status.HTTP_201_CREATED)

class NotifyUserToReupload(APIView):
   def post(self,request, phone_number,format=None):
    user = User.objects.get(phone_number=phone_number)
    activation = Activation.objects.filter(user=user).first()
    activation.delete()

    name=user.first_name
    email=user.email
    phone_number=user.phone_number

    send_notifyandDelete_email(name,email,phone_number)

    response={
        "data":{
            "status":"success",
            "message":"email sent successfully",
        }
      }
    return Response(response, status=status.HTTP_201_CREATED)

class CreateNewAccount(generics.CreateAPIView):
  serializer_class=CreateUserAccountSerializer

  def post(self, request, phone_number, format=None):
    user=User.objects.get(phone_number=phone_number)

    serializer=self.serializer_class(data=request.data)
    if serializer.is_valid(raise_exception=True):
      serializer.save(user=user)

      response={
        "data":{
            "Account_data":dict(serializer.data),
            "status":"success",
            "message":"Account created successfully",
        }
      }
      return Response(response, status=status.HTTP_201_CREATED)
    else:
      return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)


class GetUserAccountDetails(generics.CreateAPIView):
  serializer_class=UserAccountSerializer

  def get (self, request, phone_number, format=None):
    user = User.objects.filter(phone_number=phone_number).first()
    account = Account.objects.filter(user=user).first()
    serializer =self.serializer_class(account)
    return Response(serializer.data)


class MakeTransactions(generics.CreateAPIView):
  serializer_class=MakePaymentSerializer

  def post(self,request, phone_number,format=None):
    user=User.objects.get(phone_number=phone_number)
    senderUser=Account.objects.get(user=user)

    serializer=self.serializer_class(data=request.data)

    user=User.objects.get(phone_number=phone_number)
    senderUser=Account.objects.get(user=user)
    current_balance=senderUser.account_balance

    transaction_amount=int(request.data['amount'])

    if current_balance < transaction_amount:
      return Response('You do not have enough funds to make this transaction', status=status.HTTP_400_BAD_REQUEST)
    else:
      new_balance=current_balance-transaction_amount
      senderUser.account_balance=new_balance
      senderUser.save()
    if serializer.is_valid(raise_exception=True):

      serializer.save(account=senderUser)

      transaction_data =serializer.data
      response={
        "data":{
            "transaction":dict(transaction_data),
            "status":"success",
            "message":"transaction done successfully",
        }
      }
      
   
      return Response(response, status=status.HTTP_201_CREATED)
    else:
      return Response(serializers.errors, status=status.HTTP_400_BAD_REQUEST)



class DepositApiView(APIView):

  def patch(self, request,phone_number, format=None):
    user=User.objects.get(phone_number=phone_number)
    sendUser=Account.objects.get(user=user)
    current_bal=sendUser.account_balance
    new_bal = current_bal + int(request.data['account_balance'])


    serializers=DepositSerializer(sendUser,request.data,partial=True)

    if serializers.is_valid(raise_exception=True):
      serializers.save(account_balance=new_bal)

      return Response(serializers.data)
    return Response(status.errors, status=status.HTTP_400_BAD_REQUEST)  
















    

  





