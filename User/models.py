from django.db import models
from django.contrib.auth.models import User

class user_registered(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_name=models.CharField(max_length=50)
    user_email=models.EmailField(max_length=200,blank=False)
    user_phone=models.IntegerField(blank=False,max_length=10)
    user_linkedin=models.URLField(max_length=255, )
    registration_date=models.DateTimeField(auto_now_add=True)
    payment_choice = [('PENDING', 'Pending'),('COMPLETED', 'Completed'),('FAILED', 'Failed')]
    payment_status = models.CharField(max_length=10, choices=payment_choice, default='PENDING')

    def is_payment_completed(self):
        return self.payment_status == "COMPLETED"

    def __str__(self):
        return self.user_name

