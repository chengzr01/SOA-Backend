from django.urls import path

from . import views

urlpatterns = [
    path('response/', views.response, name='response'),
    path('recommendation/', views.recommendation, name="recommendation"),
    path('flush/', views.flush, name='flush'),
    path('reset/', views.reset, name='reset'),
    path('summarize/', views.summarize, name='summarize'),
    path('analyze/', views.analyze, name='analyze'),
    path('visualize/', views.visualize, name='visualize'),
    path('update_description/', views.update_description,
         name='update_description'),
    path('get_description/', views.get_description, name='get_description'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.costumed_login, name='costumed_login'),
    path('logout/', views.logout, name='logout'),
    # More URL patterns specific to this app...
]
