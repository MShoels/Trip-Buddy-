from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt


def index(request):
    return render(request, 'logandreg.html')

def create(request): 
    errors = User.objects.registration_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            print(errors)
        return redirect('/')
    elif request.method == 'POST':    
        pw_hash = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        new_user=User.objects.create(first_name=request.POST['fname'], last_name=request.POST['lname'], email=request.POST['email'], password=pw_hash)
        request.session['username']=new_user.first_name
        request.session['id']=new_user.id
        print("this is the submit path")
        print(new_user)
        return redirect('/dashboard')

def login(request):    
    print(request.POST['email'])
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            print(errors)
        return redirect('/')
    elif request.method == 'POST':  
        user=User.objects.get(email=request.POST['email'])
        request.session['username']=user.first_name
        request.session['id']=user.id
    return redirect('/dashboard')


def dashboard(request):   
    if 'id' in request.session:
        user_trips=Trip.objects.filter(planner=User.objects.get(id=request.session['id']))
        other_trips=Trip.objects.exclude(planner=User.objects.get(id=request.session['id'])).exclude(guest=User.objects.get(id=request.session['id']))
        guest_trips=Trip.objects.filter(guest=User.objects.get(id=request.session['id']))
        context={
            "user_trips": user_trips,
            'other_trips': other_trips,
            'guest_trips': guest_trips,
        }
        return render(request, 'dashboard.html', context)
    else:
        messages.error(request, 'Please Log In.', extra_tags='fail')
        return redirect('/')

def destroy(request):  
    del request.session['username']
    del request.session['id']
    print('session cleared')
    return redirect('/')

def newtrip(request): 
    return render(request, 'newshow.html')

def create_trip(request): 
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            print(errors)
        return redirect('/trips/new')
    elif request.method == "POST":
        Trip.objects.create(destination=request.POST['destination'], start_date=request.POST['start_date'], end_date=request.POST['end_date'], plan=request.POST['plan'], planner=User.objects.get(id=request.session['id']))
    return redirect('/dashboard')

def edit_trip(request, id): 
    this_trip=Trip.objects.get(id=id)
    context={
        'this_trip': this_trip
    }
    return render(request, 'editshow.html', context)

def update_trip(request):
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags=key)
            print(errors)
        return redirect(f"/trips/{request.POST['tripid']}/edit")
    elif request.method == 'POST':
        this_trip=Trip.objects.get(id=request.POST['tripid'])
        this_trip.destination=request.POST['destination']
        this_trip.start_date=request.POST['start_date']
        this_trip.end_date=request.POST['end_date']
        this_trip.plan=request.POST['plan']
        this_trip.save()
    return redirect('/dashboard')

def view(request, id):
    guest_trips=Trip.objects.filter(guest=User.objects.get(id=request.session['id']))
    this_trip=Trip.objects.get(id=id)
    context = {
        'this_trip': this_trip,
        'guest': guest_trips,
    }
    print(this_trip.guest)
    return render(request, 'viewshow.html', context)

def join(request, id): 
    this_guest=User.objects.get(id=request.session['id'])
    this_trip=Trip.objects.get(id=id)
    this_trip.guest.add(this_guest)
    return redirect('/dashboard')

def cancel(request, id): 
    this_trip=Trip.objects.get(id=id)
    guest=User.objects.get(id=request.session['id'])
    this_trip.guest.remove(guest)
    return redirect('/dashboard')

def destroy_trip(request, id):
    this_trip=Trip.objects.get(id=id)
    this_trip.delete()
    return redirect('/dashboard')