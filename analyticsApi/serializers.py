from django.db.models.base import Model
from rest_framework import serializers
from .models import *
from django import forms


class SignUpSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['userId','username','first_name', 'last_name', 'phone_number', 'email','password']
    extra_kwargs = {
      "password": {'write_only': True}
    }

  def create(self, validated_data):
          password =validated_data.pop('password', None)
          instance =self.Meta.model(**validated_data)
          if password is not None:
             instance.set_password(password)
          instance.is_customer=True  
          instance.is_active=False
          instance.save()   
          return instance


# admin sign up serializer
class AdminSignUpSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['username','first_name',  'last_name',  'phone_number', 'email','password']
    extra_kwargs = {
      "password": {'write_only': True}
    }

  def create(self, validated_data):
          password =validated_data.pop('password', None)
          instance =self.Meta.model(**validated_data)
          if password is not None:
             instance.set_password(password)
          instance.is_admin=True 
          instance.is_valid=True 
          instance.save()   
          return instance

# activation serializers 
class ActivationSerializer(serializers.ModelSerializer):
  class Meta:
    model=Activation
    exclude = ['user']

class ActivateSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = ['is_valid']

class CurrentUserSerializer(serializers.ModelSerializer):
  class Meta:
    model = User
    fields = "__all__"



class ApprovalSerializer(serializers.ModelSerializer):
  class Meta:
    model=Activation
    fields = "__all__"

  def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = CurrentUserSerializer(instance.user).data
        return response

class UserAccountSerializer(serializers.ModelSerializer):
  class Meta:
    model=Account
    fields="__all__"

  def to_representation(self, instance):
        response = super().to_representation(instance)
        response['user'] = CurrentUserSerializer(instance.user).data
        return response


class CreateUserAccountSerializer(serializers.ModelSerializer):
  class Meta:
    model=Account
    exclude = ['user', 'acc_number', 'account_balance']

class MakePaymentSerializer(serializers.ModelSerializer):
  class Meta:
    model=Transaction
    exclude=['account']

    # def to_representation(self, instance):
    #   response = super().to_representation(instance)
    #   response['user'] = CurrentUserSerializer(instance.user).data
    #   return response


class DepositSerializer(serializers.ModelSerializer):

  class Meta:
    model=Account
    fields= ["account_balance"] 