from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import *
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .forms import *
from django.contrib.auth.decorators import login_required

# APPLICATION VIEWS.
# home function


def home(request):
    comments= Feedback.objects.all()
    return render(request, 'public/index.html', {'comments':comments})


def services(request):
    ambulances = Ambulance.objects.all()
    return render(request, 'public/services.html', {'ambulances': ambulances})


def public_register(request):
    msg = None
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            msg = 'user created'
            return redirect('login')
        else:
            msg = 'form is not valid'
    else:
        form = SignUpForm()
    return render(request,'logins/register.html', {'form': form, 'msg': msg})

def admin(request):
    return render(request, 'logins/admin.html')


#user login
def user_login(request):
    form = LoginForm(request.POST or None)
    msg = None
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None and user.is_owner:
                login(request, user)
                return redirect('owner')
            elif user is not None and user.is_public:
                login(request, user)
                return redirect('home')
            elif user is not None and user.is_admin:
                login(request, user)
                return redirect('admin')
            else:
                msg= 'invalid credentials'
        else:
            messages.info = 'error validating form'
    return render(request, 'logins/login.html', {'form': form, 'msg': msg})



#admin
def admin(request):
    return render(request,'admin.html')


# logout function


def user_logout(request):
    logout(request)
    return render(request, 'public/index.html')


def profile(request):
    users = User.objects.all()
    current_user = request.user
    # profile = get_object_or_404(Profile,user=request.user)

    return render(request, 'profile/profile.html', {"users": users})


def update_profile(request):
    # profiles= Profile.objects.get(user=request.user)
    if request.method == 'POST':
        userprofileform = ProfileUpdateForm(
            request.POST, request.FILES, instance=request.user.profile)
        if userprofileform.is_valid():
            userprofileform.save()
            return redirect(to='profile')
    else:
        form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'profile/update_profile.html', {'form': form})


# def owners(request):
#     return render (request, 'owner.html')

# owners html
def owners(request):
    ambulance = Ambulance.objects.all()
    return render(request, 'owners/owner_home.html', {'ambulance': ambulance})


def add_ambulance(request):
    if request.method == 'POST':
        image = request.FILES.get('image')
        ambulance_properties = request.POST.get('describe')
        ambulance_name = request.POST.get('ambulance')
        current_location = request.POST.get('location')
        availability = request.POST.get('available')
        hire_price = request.POST.get('hire')
        ploughing_pay_rate = request.POST.get('ploughing')
        forklifting_pay_rate = request.POST.get('forklifting')
        transport_pay_rate = request.POST.get('transport')
        planting_pay_rate = request.POST.get('planting')
        operator_name = request.POST.get('operator_name')

        ambulance = Ambulance(image=image, ambulance_properties=ambulance_properties, ambulance_name=ambulance_name, current_location=current_location, availability=availability, hire_price=hire_price, ploughing_pay_rate=ploughing_pay_rate,
                              forklifting_pay_rate=forklifting_pay_rate, transport_pay_rate=transport_pay_rate, planting_pay_rate=planting_pay_rate, operator_name=operator_name)

        ambulance.owner_id = request.user

        ambulance.save_ambulance()

        return redirect('owner')

    return render(request, 'owners/add.html')


def single_ambulance(request, ambulance_id):
    single_ambulance = Ambulance.objects.get(id=ambulance_id)
    current_user = request.user
    user = User.objects.get(username=current_user.username)
    orders = Order.get_orders(ambulance_id)

    return render(request, 'owners/single_ambulance.html', {'single_ambulance': single_ambulance,'orders':orders})


def delete_ambulance(request, ambulance_id):
    ambulance = ambulance.objects.get(id=ambulance_id)
    ambulance.delete()
    return redirect('owner')


def update_ambulance(request, ambulance_id):
    update = Ambulance.objects.get(id=ambulance_id)
    if request.method == 'POST':
        ambulanceform = AmbulanceUpdateForm(
            request.POST, request.FILES, instance=update)
        if ambulanceform.is_valid():
            ambulanceform.save()
            return redirect('single', ambulance_id)
    else:
        form2 = AmbulanceUpdateForm(instance=update)
    return render(request, 'owners/update_ambulance.html', {'form2': form2})


def user_single_ambulance(request, ambulance_id):
    single_ambulance = Ambulance.objects.get(id=ambulance_id)
    current_user = request.user
    user = User.objects.get(username=current_user.username)

    return render(request, 'public/single_ambulance.html', {'single_ambulance': single_ambulance})


def comment(request, ambulance_id):
    current_user = request.user
    user = User.objects.get(username=current_user.username)
    ambulance = Ambulance.objects.get(id=ambulance_id)
    form2 = CommentForm()
    
    if request.method == 'POST':
        form2 = CommentForm(request.POST)
        if form2.is_valid():

            comment = form2.save(commit=False)

            comment.user_id = user
            comment.ambulance_id = ambulance

            comment.save()

            return redirect('single_ambulance',ambulance_id)
        else:
            form2 = CommentForm()

    return render(request, 'public/comment.html', {'form2': form2, 'ambulance': ambulance})


#order form
def order(request, ambulance_id):
    current_user = request.user
    user = User.objects.get(username=current_user.username)
    ambulance = Ambulance.objects.get(id=ambulance_id)
    form3 = OrderForm()
    
    if request.method == 'POST':
        form3 = OrderForm(request.POST)
        if form3.is_valid():

            order = form3.save(commit=False)

            order.user_id = user
            order.ambulance_id = ambulance

            order.save()

            return redirect('single_ambulance',ambulance_id)
        else:
            form3 = OrderForm()

    return render(request, 'public/order.html', {'form3': form3, 'ambulance': ambulance})