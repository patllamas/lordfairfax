from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
from django.http import HttpResponse
import bcrypt

# Create your views here.

# GET
def index(request):
    return render(request, 'index.html')

# POST
def register(request):
    if request.method == "GET":
        return redirect('/')
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/index')
    else:
        hashed_password = bcrypt.hashpw(
            request.POST['password'].encode(), bcrypt.gensalt(8)).decode()
        new_user = User.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            email=request.POST['email'],
            password=hashed_password,
        )
        request.session['user_id'] = new_user.id
    return redirect('/login')


def login(request):
    if 'user_id' not in request.session:
        return redirect('/')
    user = User.objects.get(id=request.session['user_id'])
    pets = Pet.objects.all()
    bookings = Booking.objects.all()
    context = {
        'user': user,
        'pets': pets,
        'bookings': bookings,
    }
    return render(request, 'profile.html', context)

def handle_login(request):
    if request.method == 'GET':
        return redirect('/')
    else:
        users_list = User.objects.filter(email = request.POST['email'])
        if len(users_list):
            existing_user = users_list[0]
            if bcrypt.checkpw(request.POST['password'].encode(), existing_user.password.encode()):
                request.session['user_id'] = existing_user.id
                return redirect('/login')
        messages.error(request, 'Invalid username and password.')
        return redirect('/')

def logout(request):
    request.session.clear()
    return redirect("/")

# Pet Motel Actions

def add_pet(request):
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'user': user,
    }
    return render (request, 'addpet.html', context)

def handle_add_pet(request):
    if request.method =="GET":
        return redirect('/')
    errors = Pet.objects.pet_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/add_pet')

    else:
        user = User.objects.get(id=request.session['user_id'])
        Pet.objects.create(
            pet_name = request.POST['pet_name'],
            animal_type = request.POST['animal_type'],
            breed = request.POST['breed'],
            owner = user,
        )
    return redirect('/login')

def delete_pet(request, id):
    pet_delete = Pet.objects.get(id=id)
    pet_delete.delete()
    return redirect('/login')

def book_pet_get(request):
    pets = Pet.objects.all()
    user = User.objects.get(id=request.session['user_id'])
    context = {
        'pets' : pets,
        'user' : user,
    }
    return render(request, 'booking.html', context)

def book_pet(request):
    if request.method == "GET": 
        return redirect('/')
    errors = Booking.objects.booking_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/book_pet_get')
    else:
        pet = Pet.objects.get(id=request.POST['booked_pet'])
        Booking.objects.create(
            booked_pet = pet,
            room_type = request.POST['room_type'],
            check_in = request.POST['check_in'],
            check_out = request.POST['check_out'],
        )
    return redirect('/login')

def book_cancel(request, id):
    booking = Booking.objects.get(id=id)
    booking.delete()
    return redirect('/login')

def invoice_get(request):
    user = User.objects.get(id=request.session['user_id'])
    invoices = Invoice.objects.all()
    context = {
        'user': user,
        'invoices' : invoices,

    }
    return render(request, 'invoice.html', context)