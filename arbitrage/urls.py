from django.urls import path
from . import views

urlpatterns = [
    path('', views.contact, name='contact'),
    path('signup', views.signup, name='signup'),
    path('login', views.loginForm, name='login'),
    path('logout', views.logout, name='logout'),
    path('blockfolio', views.blockfolio, name='blockfolio')
]