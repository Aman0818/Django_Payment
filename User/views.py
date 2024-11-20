from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.hashers import make_password
from django.views.decorators.cache import cache_control
from .models import user_registered
from django.views.decorators.csrf import csrf_exempt
import razorpay

@csrf_exempt
def update_payment_status(request):
    if request.method == "POST" and request.user.is_authenticated:
        try:
            user_profile = user_registered.objects.get(user=request.user)
            user_profile.payment_status = 'COMPLETED'
            user_profile.save()
            return JsonResponse({'status': 'success'})
        except Exception as e:
            return JsonResponse({'status': 'failed', 'error': str(e)})
    else:
        return redirect('login_view')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def register_view(request):
    if request.user.is_authenticated: 
        return redirect('dashboard_view')
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        phone = int(request.POST['phone'])
        linkedin = request.POST['linkedin']
        password1 = request.POST['password']
        password2 = request.POST['confirm_password']

        if password1 != password2:
            return render(request, 'register.html', {'display':'block','error': 'Passwords do not match'})

        if user_registered.objects.filter(user_phone=phone).exists():
            return render(request, 'register.html', {'display':'block','error': 'phone number already exists'})
        
        try:
            user = User.objects.create(
                username=phone,
                password=make_password(password1)
            )
            a=user_registered.objects.create(
                user=user,
                user_name=name,
                user_email=email,
                user_phone=phone,
                user_linkedin=linkedin,
                payment_status = 'PENDING'
            )
            login(request, user)
            return redirect('dashboard_view')
        except:
            return render(request, 'register.html', {'display':'block','error': 'something went wrong try again'})
    return render(request, 'register.html',{'display':'none'})

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def login_view(request):
    if request.user.is_authenticated:  # Check if the user is already logged in
        return redirect('dashboard_view')
    if request.method == 'POST':
        phone = request.POST['phone']
        password = request.POST['password']
        user = authenticate(request, username=phone, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard_view')
        else:
            return render(request, 'login.html', {'display':'block','error': 'Invalid credentials'})
    return render(request, 'login.html',{'display':'none'})

def logout_view(request):
    logout(request)
    return redirect('login_view')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def dashboard_view(request):
    if not request.user.is_authenticated:  # Check if the user is already logged in
        return redirect('login_view')
    
    return render(request, 'dashboard.html')

@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def payment_view(request):
    if not request.user.is_authenticated:  # Check if the user is already logged in
        return redirect('login_view')
    else:
        try:
            print("pagee aa gaya hai")
            client = razorpay.Client(auth=("your_api_key", "your_secret_key"))
            data = { "amount": 49900, "currency": "INR", "payment_capture":'1' }
            payment = client.order.create(data=data)
            context = {
            'order_id': payment['id'],
            'amount': data['amount']
            }
            print("process done")
            return render(request, 'payment.html',context)
        except:
            print("internet is off!") 
    
@cache_control(no_cache=True, must_revalidate=True, no_store=True)
def premium_view(request):
    if not request.user.is_authenticated: #check logged
        return redirect('login_view')
    user_profile = user_registered.objects.get(user=request.user)
    if  user_profile.payment_status=='PENDING':
        return redirect('payment_view')
    return render(request, 'premium.html')
