from django.shortcuts import render
from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPassword

# Create your views here.
def getAccessToken(request):
    consumer_key="odPcEAcCk7PZBsBawM5rzbUYzGAaIgXB"
    consumer_secret="e9TcZocDxJ6eFgwh"
    api_URL='https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials'

    r=requests.get(api_URL, auth=HTTPBasicAuth(consumer_key, consumer_secret))
    mpesa_access_token=json.loads(r.text)
    validated_mpesa_access_token=mpesa_access_token['access_token']

    return HttpResponse(validated_mpesa_access_token)

def lipa_na_mpesa_online(request):
    access_token=MpesaAccessToken.validated_mpesa_access_token
    api_url="https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers={"Authorization":"Bearer %s" % access_token}
    request={
        "BusinessShortCode":LipanaMpesaPassword.Business_short_code,
        "Password":LipanaMpesaPassword.decode_password,
        "Timestamp":LipanaMpesaPassword.lipa_time,
        "TransactionType":"CustomerPayBillOnline",
        "Amount":1,
        "PartyA":254724053594,
        "PartyB":LipanaMpesaPassword.Business_short_code,
        "PhoneNumber":254724053594,
        "CallBackURL":"https://sandbox.safaricom.co.ke/mpesa/",
        "AccountReference":"Alice",
        "TransactionDesc":"Testing stk push"
    }
    response=requests.post(api_url, json=request, headers=headers)
    return HttpResponse('success')