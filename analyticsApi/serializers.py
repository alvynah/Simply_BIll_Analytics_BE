from rest_framework import serializers
from .models import User
from django import forms


class SignUpSerializer(serializers.ModelSerializer):
  email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
  password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
  confirm_password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
  class Meta:
    model = User
    fields = ['first_name',  'last_name',  'phone_number', 'email','password', 'confirm_password']
    extra_kwargs = {
      "password": {'write_only': True}
    }
  def save(self):
    user = User(
            username = self.validated_data['username'],
            email = self.validated_data['email'],
        )
    password = self.validated_data['password']
    confirm_password = self.validated_data['confirm_password']
    if password != confirm_password:
      raise serializers.ValidationError({'password': 'Passwords must match'})
    user.set_password(password)
    user.save()
    return user


