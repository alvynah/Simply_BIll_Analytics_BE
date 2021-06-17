from rest_framework import serializers
from .models import User
from django import forms


class SignUpSerializer(serializers.ModelSerializer):
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
          instance.save()   
          return instance
















  # def save(self):
  #   user = User(
  #           username = self.validated_data['username'],
  #           email = self.validated_data['email'],
  #       )
  #   password = self.validated_data['password']
  #   confirm_password = self.validated_data['confirm_password']
  #   if password != confirm_password:
  #     raise serializers.ValidationError({'password': 'Passwords must match'})
  #   user.set_password(password)
  #   user.save()
  #   return user




