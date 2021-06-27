from django.shortcuts import render
from django.http import HttpResponse
import requests
from requests.auth import HTTPBasicAuth
import json
from . mpesa_credentials import MpesaAccessToken, LipanaMpesaPassword
from .models import MpesaPayment
from django.views.decorators.csrf import csrf_exempt
from mpesa_api.serializers import *
from mpesa_api.models import *
# from rest_framework.views import APIView
from rest_framework.views import APIView
from rest_framework import generics
from datetime import datetime
import pytz

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
        "CallBackURL":"https://mpesa-payments.herokuapp.com/api/v1/c2b/confirmation",
        "AccountReference":"Alice",
        "TransactionDesc":"Testing stk push"
    }
    response=requests.post(api_url, json=request, headers=headers)
    # print(request)
    return HttpResponse('success')

@csrf_exempt
def register_urls(request):
    access_token=MpesaAccessToken.validated_mpesa_access_token
    api_url="https://sandbox.safaricom.co.ke/mpesa/c2b/v1/registerurl"
    headers={"Authorization": "Bearer %s" % access_token}
    options={"ShortCode":LipanaMpesaPassword.Test_c2b_shortcode,
             "ResponseType":"Completed",
             "ConfirmationURL":"https://mpesa-payments.herokuapp.com/api/v1/c2b/confirmation",
             "ValidationURL":"https://mpesa-payments.herokuapp.com/api/v1/c2b/validation"}

    response=requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)


@csrf_exempt
def call_back(request):
    pass

@csrf_exempt
def validation(request):

    context={
        "ResultCode":0,
        "ResultDesc":"Accepted"
    }
    return JsonResponse(dict(context))

@csrf_exempt
def confirmation(request):
    mpesa_body=request.body.decode('utf-8')
    mpesa_payment=json.loads(mpesa_body)

    print(mpesa_payment)

    def post(self, request):
        # save the data
        request_data = json.dumps(request.data)
        request_data = json.loads(request_data)
        body = request_data.get('Body')
        resultcode = body.get('stkCallback').get('ResultCode')
        # Perform your processing here e.g. print it out...
        if resultcode == 0:
            print('Payment successful')
            requestId = body.get('stkCallback').get('CheckoutRequestID')
            metadata = body.get('stkCallback').get('CallbackMetadata').get('Item')
            for data in metadata:
                if data.get('Name') == "MpesaReceiptNumber":
                    receipt_number = data.get('Value')
                if data.get('Name')=="Amount":
                    amount=data.get('Value')
                if data.get('Name')=="TransactionDate":
                    transaction_date=data.get('Value')

                    str_transaction_date = str(transaction_date)
                    print(str_transaction_date, "this should be an str_transaction_date")

                    transaction_datetime = datetime.strptime(str_transaction_date, "%Y%m%d%H%M%S")
                    print(transaction_datetime, "this should be an transaction_datetime")

                    aware_transaction_datetime = pytz.utc.localize(transaction_datetime)
                    print(aware_transaction_datetime, "this should be an aware_transaction_datetime")

                if data.get('Name')=="PhoneNumber":
                    phone_number=data.get('Value')

            payment=MpesaPayment(
                amount=amount,
                receipt_number=receipt_number,
                transaction_date=aware_transaction_datetime,
                phone_number=phone_number,
            )
            payment.save()
                
        else:
            print('unsuccessfull')

    context={
        "ResultCode":0,
        "ResultDesc":"Accepted"
    }
    return JsonResponse(dict(context))

@csrf_exempt
def simulate_transaction_c2b(request):
    access_token=MpesaAccessToken.validated_mpesa_access_token
    api_url="https://sandbox.safaricom.co.ke/mpesa/c2b/v1/simulate"
    headers={"Authorization": "Bearer %s" % access_token}
    options={"ShortCode":LipanaMpesaPassword.Test_c2b_shortcode,
            "CommandID":"CustomerPayBillOnline",
            "Amount":1,
            "Msisdn":254708374149,
            "BillRefNumber":"12345678"
            }

    response=requests.post(api_url, json=options, headers=headers)
    return HttpResponse(response.text)

