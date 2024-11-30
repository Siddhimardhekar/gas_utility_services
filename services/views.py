from django.shortcuts import render, redirect
from .forms import ServiceRequestForm
from .models import ServiceRequest, Customer
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Customer

def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Link the user to a customer instance
            Customer.objects.create(
                user=user,
                email=request.POST.get('email', ''),
                first_name=request.POST.get('first_name', ''),
                last_name=request.POST.get('last_name', ''),
            )
            login(request, user)
            return redirect('account_created')
    else:
        form = UserCreationForm()
    return render(request, 'services/signup.html', {'form': form})
@login_required
def submit_request(request):
    if request.method == 'POST':
        form = ServiceRequestForm (request.POST, request.FILES)
        if form.is_valid():
            service_request = form.save(commit=False)
            try:
                customer = Customer.objects.get(email=request.user.email)
                service_request.customer = customer
                service_request.save()
                return redirect('track_request')
            except Customer.DoesNotExist:
                return render(request, 'services/error.html', {'message': 'Customer not found.'})
    else:
        form = ServiceRequestForm()
    return render(request, 'services/submit_request.html', {'form': form})

@login_required
def track_request(request):
    if not request.user.is_authenticated:
        return HttpResponseBadRequest("Unauthorized access.")
    try:
        customer = Customer.objects.get(user=request.user)
        requests = ServiceRequest.objects.filter(customer=customer)
        return render(request, 'services/track_request.html', {'requests': requests})
    except Customer.DoesNotExist:
        return render(request, 'services/error.html', {'message': 'Customer account not found.'})

def account_created(request):
    return render(request, 'services/account_created.html')