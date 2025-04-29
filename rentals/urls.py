from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),  # Home route for the app
    path('snowboards/', views.snowboard_list, name='snowboard_list'),
]



