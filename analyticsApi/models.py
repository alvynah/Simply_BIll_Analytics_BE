from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField
from django.db.models.fields import related
from phonenumber_field.modelfields import PhoneNumberField
import uuid
import random

# Create your models here.
class User(AbstractUser):
	userId = models.AutoField(primary_key=True)
	first_name=models.CharField(max_length=255)
	last_name=models.CharField(max_length=255)
	phone_number=models.IntegerField(unique=True,null=True)
	email=models.EmailField(unique=True)
	password=models.CharField(max_length=255)
	is_customer=models.BooleanField(default=False)
	is_admin=models.BooleanField(default=False)
	is_valid=models.BooleanField(default=False)


	REQUIRED_FIELDS=[]


def upload_image(instance, filename):
    return "/".join(['images', str(instance.user.phone_number), filename])

class Activation(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE,  related_name="activation", null=True)
	passport_photo=CloudinaryField('passport_photo')
	identification_number=models.CharField(max_length=255)
	identification_doc=CloudinaryField('passport/nationalID')
	driving_license_picture=CloudinaryField('driving_license', blank=True)
	residence=models.CharField(max_length=255)
	KRA_pin=models.CharField(max_length=255)

	def __str__(self):
		return str(self.user.username)

class Account(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE, related_name="account")
	account_number= models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
	account_name=models.CharField(max_length=250)
	account_balance=models.IntegerField(default=0)

	def __str__(self):
		return self.account_number



def create_new_ref_number():
	not_unique=True
	while not_unique:
		unique_ref=random.randint(1000000000, 9999999999)
		if not Account.objects.filter(account_number=unique_ref):
			not_unique=False
			return str(unique_ref)	
class Account(models.Model):
	user=models.OneToOneField(User, on_delete=models.CASCADE, related_name="account")
	account_name=models.CharField(max_length=255, null=True)
	account_number=models.CharField(max_length=10, blank=True, editable=True,default=create_new_ref_number, null=True)
	account_balance=models.IntegerField()


	def __str__(self):
		return self.account_name


	


	
