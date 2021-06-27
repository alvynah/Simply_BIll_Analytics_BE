from django.db import models

# Create your models here.
class BaseModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract=True

# mpesa payments models
class MpesaCalls(BaseModel):
    ip_address=models.TextField()
    caller=models.TextField()
    conversation_id=models.TextField()
    content=models.TextField()

    class Meta:
        verbose_name="Mpesa Call"
        verbose_name_plural="Mpesa Calls"

class MpesaCallBacks(BaseModel):
    ip_address=models.TextField()
    caller=models.TextField()
    conversation_id=models.TextField()
    content=models.TextField()

    class Meta:
        verbose_name="Mpesa Call Back"
        verbose_name_plural="Mpesa Call Backs"

class MpesaPayment(BaseModel):
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    receipt_number=models.CharField(max_length=50, default="")
    phone_number=models.IntegerField()
    transaction_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        verbose_name="Mpesa Payment"
        verbose_name_plural="Mpesa Payments"

    def __str__(self):
        return self.phone_number
