from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
import time
from .models import Attendance
def home(request):
    if request.user.is_superuser:
        user_list = []
        users = User.objects.all()
        for i in users:
            try:
                attendance = Attendance.objects.get(student__pk = i.pk)
                merged_data = {'user': i, 'attendance': attendance}
            except:
                merged_data = {'user': i}
            user_list.append(merged_data) 
        data = {
            'users' : user_list,
            'attendance' : attendance 
        }
        return render(request,'admin-dashboard.html' , context=data)
    else:
        return render(request,'user.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username') 
        password = request.POST.get('password') 
        user = authenticate(request, username = username , password = password)
        if user is not None:
            auth_login(request, user)
            if user.is_superuser:
                return redirect('home')
            else:
                att_user = user
                time_now = time.strftime("%H:%M", time.localtime())
                attendace = Attendance(student = att_user, start_time = time_now)
                attendace.save()
                return redirect('home')
        else:
            return HttpResponse("No user with this credential")
    return render(request,'login.html')

def logout(request):
    if request.method == "POST":
        if request.user.is_superuser:
            auth_logout(request)
        else:
            user = request.POST.get('user_id')
            get_user = Attendance.objects.get(student__pk = user)
            time_now = time.strftime("%H:%M", time.localtime())
            get_user.end_time = time_now
            get_user.save()
    return redirect('login')
 
def register(request):
    if request.method == "POST":
        firstname = request.POST.get('edit')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        username = firstname+lastname
        hashed_password = make_password(password)
        user = User(username = username, first_name = firstname, last_name = lastname, email = email, password = hashed_password)
        user.save()
    
    users = User.objects.all()
    data = {
        'users' : users
    }
    return render(request,'admin-registeration.html',context=data)

def update_user(request):
    if request.method == "POST":
        user_id = request.POST.get('user_id')
        username = request.POST.get('username')
        firstname = request.POST.get('first_name')
        lastname = request.POST.get('last_name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        if user_id:
            user = User.objects.get(pk = user_id)
            user.username = username
            user.first_name = firstname
            user.last_name = lastname
            user.email = email
            user.password = password
            user.save()
            return redirect('register')
        else:
            print("No User name Found")

def delete_user(request):
    if request.method == "POST":
        user = request.POST.get('ID')
        u = User.objects.get(pk = user)
        u.delete()
    return redirect('register')
