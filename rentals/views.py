from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Snowboard, Renter, Rental
from django.contrib.auth.decorators import login_required


# Create your views here.
from django.http import HttpResponse


def home(request):
    snowboards = Snowboard.objects.all()
    rentals = Rental.objects.filter(return_date__isnull = True)
    renters = None
    if request.session.get('renter_id'):
        try:
            renter = Renter.objects.get(id=request.session['renter_id'])
        except Renter.DoesNotExist:
            renter = None
    return render(request, 'rentals/home.html', {
        'renter': renters,
        'snowboards': snowboards,
        'rentals': rentals
    })

def renter_required(view):
    def wrapped(request, *args, **kwargs):
        if 'renter_id' not in request.session:
            return redirect(f"/login/?next={request.path}")
        return view(request, *args, **kwargs)
    return wrapped

@renter_required
def rent_snowboard(request, snowboard_id):
    snowboard = get_object_or_404(Snowboard, pk=snowboard_id)
    renter = get_object_or_404(Renter, id=request.session['renter_id'])  
    if snowboard.is_available():
        Rental.objects.create(snowboard=snowboard, renter=renter)
        snowboard.quantity_available -= 1
        snowboard.save()
    snowboards = Snowboard.objects.all()
    rentals = Rental.objects.filter(renter_id=renter.id, return_date__isnull=True)
    return render(request, 'rentals/snowboard_list.html', {
        'snowboards': snowboards,
        'rentals': rentals,
    })

@renter_required
def return_snowboard(request, rental_id):
    rental = get_object_or_404(Rental, pk=rental_id)
    renter = get_object_or_404(Renter, id=request.session['renter_id'])
    if rental.return_date is None:
        rental.return_date = timezone.now()
        rental.save()
        rental.snowboard.quantity_available += 1
        rental.snowboard.save()
    snowboards = Snowboard.objects.all()
    rentals = Rental.objects.filter(renter_id=renter.id, return_date__isnull=True)
    return render(request, 'rentals/snowboard_list.html', {
        'snowboards': snowboards,
        'rentals': rentals,
    })

@renter_required
def snowboard_list(request):
    renter_id = request.session['renter_id']
    snowboards = Snowboard.objects.all()
    rentals = Rental.objects.filter(renter_id = renter_id,
                                    return_date__isnull = True)
    return render(request, 'rentals/snowboard_list.html', 
                  {'snowboards': snowboards,
                   'rentals': rentals,
                   })


def login_view(request):
    next_url = request.GET.get('next', 'snowboard_list')
    if request.method == 'POST':
        username = request.POST.get('username','').strip()
        if username:
            renter, _ = Renter.objects.get_or_create(username=username)
            request.session['renter_id'] = renter.id
            request.session['renter_username'] = renter.username
            return redirect(next_url)
    return render(request, 'rentals/login.html', {'next': next_url})

def logout_view(request):
    request.session.pop('renter_id', None)
    request.session.pop('renter_username', None)
    return redirect('login')
