from django.shortcuts import render, redirect 
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
def home(request):
    if request.user.is_superuser:
        users = User.objects.all()
        data = {
            'users' : users
        }
        return render(request,'admin-dashboard.html' , context=data)
    else:
        return render(request,'user.html')

def login(request):
    if request.method == "POST":
        username = request.POST.get('username') 
        password = request.POST.get('password') 
        user = authenticate(request, username = username , password = password)
        print(username,password)
        print(user)
        if user is not None:
            auth_login(request, user)
            return redirect('home')
        else:
            return HttpResponse("No user with this credential")
    return render(request,'login.html')

def logout(request):
    if request.method == "POST":
        auth_logout(request)
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
