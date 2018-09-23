from django.contrib.auth import login as auth_login
from django.shortcuts import render, redirect
from .forms import SignUpForm

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('/')
    else:
        form = SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def whoAmI(request):
    print(request.user.username)

# def login(request):
#     return render(request, 'accounts/login.html')

# def logout(request):
#     return redirect('/')