from django.contrib.auth.models import AbstractUser
from django.db import models


# Create your models here.
class User(AbstractUser):
	userId = models.AutoField(primary_key=True)
	first_name=models.CharField(max_length=50)
	last_name=models.CharField(max_length=50)
	phone_number=models.IntegerField(unique=True, null=True)
	email=models.EmailField()
	password=models.CharField(max_length=255)
	is_customer=models.BooleanField(default=False)
	is_banker=models.BooleanField(default=False)

