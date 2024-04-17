from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('response/', views.response, name='response'),
    path('flush', views.flush, name='flush'),
    path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    # More URL patterns specific to this app...
]
