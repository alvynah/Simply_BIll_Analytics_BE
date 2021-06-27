from rest_framework import serializers
from mpesa_api.models import *

class lipaNaMpesaOnline(serializers.ModelSerializer):
    class Meta:
        model=MpesaPayment
        fields="id"