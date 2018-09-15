from django.shortcuts import render

def signup(request):
    if request.method == 'POST':
        form = forms.SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('/')
    else:
        form = forms.SignUpForm()
    return render(request, 'accounts/signup.html', {'form': form})

def whoAmI(request):
    print(request.user.username)

def loginForm(request):
    return render(request, 'accounts/login.html')

def logout(request):
    return redirect('/')