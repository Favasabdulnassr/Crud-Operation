from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
import re
      
def index(request):
    if 'username' in request.session:
        return redirect('home')  
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user= auth.authenticate(username=username, password=password)
        if user is not None:
            request.session['username'] = username
            return redirect('home')
        else:
            messages.error(request, "Invalid password or username")
            return redirect('index')
    else:
        return render(request, "index.html")
 
 
def home(request):
    if 'username' in request.session:
        username = ''
        username = request.session['username']
    else:
        return redirect('index') 

    return render(request, 'home.html', {'username': username})


def validate_email(email):
    email_pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'
    if not re.match(email_pattern, email):
        return False
    return True

                                                            
def validate_password(password):
    password_pattern = r'^(?=.*[a-zA-Z]).{8,}$'
    if not re.match(password_pattern, password):
        return False
    return True


def validate_username(username):
    username_pattern = r'^[a-zA-Z0-9]+$'
    if not re.match(username_pattern, username):
        return False
    return True


        

def sign_up(request):
    #in case if the tab goes backb=ward redirect to the home page : for kpreventing goiong back
    if 'username' in request.session:
        return redirect('home')

    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']

        if not validate_username(username):
            messages.error(request, "Username should only contain characters")
            return redirect('sign_up')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('sign_up')

        elif User.objects.filter(email=email).exists():
            messages.error(request, "Email is already taken")
            return redirect('sign_up')

        elif not validate_email(email): 
            messages.error(request, "Invalid email format")
            return redirect('sign_up')

        elif not validate_password(password):
            messages.error(request, "Password should be at least 8 characters or numbers")
            return redirect('sign_up')

        # Create a new user if everything is valid
        else:
            user = User.objects.create_user(username=username, email=email, password=password)
            user.save()
            messages.info(request, "User created successfully.")
            return redirect('index')                                               
    else:
        # Render the sign-up form for GET requests
        return render(request, 'sign_up.html')



def logout(request):
    if 'username' in request.session:
        request.session.flush()  # Clear the session
        return redirect('index')
    
