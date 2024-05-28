from django.urls import path
from . import views
from django.urls import include

urlpatterns = [
    path('', views.index, name='index'),
    path('response/', views.response, name='response'),
    path('recommendation/', views.recommendation, name="recommendation"),
    path('flush/', views.flush, name='flush'),
    path('reset/', views.reset, name='reset'),
    path("accounts/", include("django.contrib.auth.urls")),
    path('accounts/signup/', views.signup, name='signup'),
    # More URL patterns specific to this app...
]
