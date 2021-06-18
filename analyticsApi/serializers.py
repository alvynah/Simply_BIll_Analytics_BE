from rest_framework import serializers
from .models import User, Activation
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
          instance.save()   
          return instance

# activation serializers 
class ActivationSerializer(serializers.ModelSerializer):
  class Meta:
    model=Activation
    exclude = ['user']






