from django.shortcuts import render

def index(request):
    return render(request, 'personal/home.html')

def contact(request):
    return render(request, 'personal/basic.html', {'content': ['if you would', 'email@email.com']})

def arbitrage(request):
    return render(request, 'personal/arbitrage.html', {'arbitrage': 234})