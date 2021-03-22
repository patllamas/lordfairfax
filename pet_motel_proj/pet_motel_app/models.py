from django.db import models
from django.db.models.base import ModelStateFieldsCacheDescriptor
from django.db.models.deletion import CASCADE
from django.db.models.fields import DateField, DateTimeField
from datetime import datetime
from django import forms
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.
class UserManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        
        if len(postData['first_name']) < 2:
            errors['first_name'] = 'First name should be at least 2 characters.'
        if len(postData['last_name']) < 2:
            errors['last_name'] = 'Last name should be at least 2 characters.'
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'The email you have entered is invalid.'
        if len(postData['password']) < 8:
            errors['password'] = 'Your password should be at least 8 characters.'
        if postData['password'] != postData['confirm_password']:
            errors['password'] = "Passwords don't match."
        return errors

class PetManager(models.Manager):
    def pet_validator(self, postData):
        errors = {}


        if len(postData['pet_name']) < 1:
            errors['pet_name'] = 'Your pet should have a name.'
        if len(postData['animal_type']) < 1:
            errors['animal_type'] = 'Your pet should be a cat or dog.'
        return errors

class BookingManager(models.Manager):
    def booking_validator(self, postData):
        errors = {}


        current_date = datetime.today()
        check_in_date = datetime.strptime(postData['check_in'], '%Y-%m-%d')

        if len(postData['room_type']) < 0:
            errors['room_type'] = 'You must select a room type.'
        if len(postData['booked_pet']) < 1:
            errors['booked_pet'] = 'You must create a pet.'
        if postData['check_in'] > postData['check_out']:
            errors['check_in'] = 'Check in date must be before checkout date.'
        if current_date > check_in_date:
            errors['check_out'] = 'Check in date must be in the future.'
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.CharField(max_length=50)
    password = models.CharField(max_length=50)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = UserManager()

class Pet(models.Model):
    pet_name = models.CharField(max_length=50)
    animal_type = models.CharField(max_length=10)
    breed = models.CharField(max_length=50)
    owner = models.ForeignKey(User, related_name="pets", on_delete = models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PetManager()


class Booking(models.Model):
    booked_pet = models.ForeignKey(Pet, related_name="invoices", on_delete=models.CASCADE)
    room_type = models.CharField(max_length=10)
    check_in = models.DateField()
    check_out = models.DateField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = BookingManager()

class Invoice(models.Model):
    total_price = models.DecimalField(decimal_places=2, max_digits=6)
    booking = models.OneToOneField(Booking, on_delete=CASCADE, related_name="bookings", primary_key=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)