from django.shortcuts import render
from .models import Snowboard

# Create your views here.
from django.http import HttpResponse

def home(request):
    return HttpResponse("Welcome to the Snowboard Rental Shop!")

def snowboard_list(request):
    snowboards = Snowboard.objects.all()
    return render(request, 'rentals/snowboard_list.html', {'snowboards': snowboards})