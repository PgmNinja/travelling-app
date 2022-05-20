from email.policy import default
from django.db import models
from django.contrib.auth.models import AbstractUser
from .choices import *
from django.db.models.signals import pre_save
from django.dispatch import receiver

def append_zero(number):
    if len(str(number)) != 3:
        appended = '0'*(3 - len(str(number))) + str(number)
    else:
        appended = number
    return appended

def generate_code(latest_package, min_val=1, max_val=999):
    if  latest_package and latest_package.code:
        code = latest_package.code
        latest_key = int(code[-3:])
        if latest_key < max_val:
            key = latest_key + 1
        else:
            key = min_val
    else:
        key = min_val
    return append_zero(key)


class Users(AbstractUser):
    USER_ROLE_CHOICES = (
        ('user', 'user'),
        ('owner', 'owner')
    )
    email = models.CharField(max_length=255)
    role = models.CharField(max_length=20, choices=USER_ROLE_CHOICES, null=True, blank=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.email

    class Meta:
        db_table = 'users'


class Location(models.Model):
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    code = models.CharField(max_length=8, unique=True)
    
    def __str__(self):
        return self.city

    class Meta:
        db_table = 'location'


class Flight(models.Model):
    company_name = models.CharField(max_length=50)
    from_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='source')
    to_location = models.ForeignKey(Location, on_delete=models.CASCADE, related_name='destination')
    departure_date = models.DateField()
    departure_time = models.TimeField()
    fare = models.DecimalField(max_digits=15,decimal_places=2)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=5, null=True, blank=True)

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = 'flight'


class Hotel(models.Model):
    company_name = models.CharField(max_length=50)
    daily_cost = models.DecimalField(max_digits=15,decimal_places=2)
    address = models.TextField()
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=5, null=True, blank=True)

    def __str__(self):
        return self.company_name

    class Meta:
        db_table = 'hotel'

class Package(models.Model):
    title = models.CharField(max_length=100)
    code = models.CharField(max_length=8, default="", unique=True)
    location = models.ForeignKey(Location, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    flight = models.ManyToManyField(Flight, related_name='flights')
    description=models.TextField(blank=True,null=True)
    price=models.DecimalField(max_digits=15,decimal_places=2)
    currency = models.CharField(choices=CURRENCY_CHOICES, max_length=5, null=True, blank=True)

    def __str__(self):
        return self.title
    

    @classmethod
    def generate_unique_code(cls):
        while True:
            latest_package = cls.objects.last()
            new_code = generate_code(latest_package)
            if cls.objects.filter(code=new_code).count() == 0:
                break
        return new_code

    class Meta:
        db_table = 'package'


class Review(models.Model):
    package = models.ForeignKey(Package, on_delete=models.CASCADE)
    review = models.CharField(max_length=1000)
    rating = models.IntegerField()
    rated_by = models.ForeignKey(Users, on_delete=models.SET_NULL, blank=True, null=True)
    rated_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'review'
