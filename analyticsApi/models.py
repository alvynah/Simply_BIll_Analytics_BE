from django.contrib.auth.models import AbstractUser
from django.db import models
from cloudinary.models import CloudinaryField
from django.db.models.fields import related


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
	user=models.OneToOneField(User, on_delete=models.CASCADE,  related_name="activation", primary_key=True)
	passport_photo=CloudinaryField('passport_photo')
	identification_number=models.CharField(max_length=255)
	identification_doc=CloudinaryField('passport/nationalID')
	driving_license_picture=CloudinaryField('driving_license', blank=True)
	residence=models.CharField(max_length=255)
	KRA_pin=models.CharField(max_length=255)

	def __str__(self):
		return str(self.user.first_name)

	
