from django.shortcuts import redirect, render
from .models import Product,Category
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .forms import SignUpForm
from django import forms

# Create your views here.


def category(request,foo):
    #replace hyphens with space
    foo= foo.replace('-',' ')
    # category form the url
    try:
        #look up category
        category= Category.objects.get(name=foo)
        products= Product.objects.filter(category=category) 
        return render(request, 'category.html', {"products":products, 'category':category})

    except:
        messages.success(request, {"That category Doesn't Exist..."})
        return redirect('home')


def product(request,pk):
    products = Product.objects.get(id=pk) 
    return render(request, 'product.html', {'product':products})

def home(request):
    products = Product.objects.all() 
    return render(request, 'home.html', {'products':products})


def about(request):
    return render(request, 'about.html')

def login_user(request):
    if request.method == 'POST':
         username = request.POST['username']
         password= request.POST['password']
         user= authenticate(request, username=username,password=password)
         if user is not None:
             login(request, user)
             messages.success(request, ('Your have been logged In'))
             return redirect('home')
         else:
             messages.success(request, ('There was an error, please try again...'))
             return redirect('login')
    else:
        return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request,('You have been Logged Out...!'))
    return redirect('home')

def register_user(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)  # Save user but don't commit yet
            user.set_password(form.cleaned_data['password1'])  # Ensure password is hashed
            user.save()  # Now save the user
            
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            
            # Authenticate the user
            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)  # Log in the user
                messages.success(request, "You have registered successfully!")
                return redirect('home')
            else:
                messages.error(request, "Authentication failed. Please try logging in manually.")
        
        else:
            print("Form Errors:", form.errors)  # Debugging: Print errors to console
            messages.error(request, "There was a problem in registering, please try again...")

    else:
        form = SignUpForm()  # Empty form for GET request
    
    return render(request, 'register.html', {'form': form})  # Render form with errors if any