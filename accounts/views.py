from django.http.response import FileResponse
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User

def register(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['password2']

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, f"Username '{username}' is already taken! Please try another")
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, f"Email '{email}' is already registered!")
                    return redirect('register')
                else:
                    user = User.objects.create_user(username=username, password=password, email=email,
                                                        first_name=first_name, last_name=last_name)
                    # Login after Register
                    # auth.login(request, user)
                    # messages.success(request, "You are now logged in")
                    # return redirect('index')
                    user.save()
                    messages.success(request, "Registration successful! You can now log in")
                    return redirect('register')
        else:
            messages.error(request, "Passwords do not match!")
            return redirect('register')
    else:
        context = {
            'page': 'register'
        }
        return render(request, 'accounts/register.html', context)

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, "You are now logged in")
            return redirect("dashboard")
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        context = {
            'page': 'login'
        }
        return render(request, 'accounts/login.html', context)

def logout(request):
    return redirect('index')

def dashboard(request):
    return render(request, 'accounts/dashboard.html')


