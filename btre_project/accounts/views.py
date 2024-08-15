from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from contacts.models import Contact

def register(request):
    """
    Handle user registration.

    If the request method is POST, this view processes the registration form.
    It checks if the passwords match and if the username or email is already in use.
    If the data is valid, it creates a new user, saves them to the database, and redirects 
    the user to the login page. Otherwise, it displays appropriate error messages.

    If the request method is GET, it renders the registration page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered registration page (for GET requests) or a redirect
                      to the appropriate page based on the form submission.
    """
    if request.method == 'POST':
        # Get form values
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        # Check if passwords match
        if password == password2:
            # Check username
            if User.objects.filter(username=username).exists():
                messages.error(request, 'That username is taken')
                return redirect('register')
            else:
                if User.objects.filter(email=email).exists():
                    messages.error(request, 'That email is being used')
                    return redirect('register')
                else:
                    # Looks good
                    user = User.objects.create_user(
                        username=username, 
                        password=password,
                        email=email, 
                        first_name=first_name, 
                        last_name=last_name
                    )
                    user.save()
                    messages.success(request, 'You are now registered and can log in')
                    return redirect('login')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'accounts/register.html')

def login(request):
    """
    Handle user login.

    If the request method is POST, this view processes the login form.
    It authenticates the user with the provided username and password.
    If successful, it logs the user in and redirects them to the dashboard.
    Otherwise, it displays an error message and redirects back to the login page.

    If the request method is GET, it renders the login page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered login page (for GET requests) or a redirect
                      to the appropriate page based on the form submission.
    """
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            messages.success(request, 'You are now logged in')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid credentials')
            return redirect('login')
    else:
        return render(request, 'accounts/login.html')

def logout(request):
    """
    Handle user logout.

    If the request method is POST, this view logs out the currently authenticated user
    and redirects them to the homepage with a success message.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A redirect to the homepage.
    """
    if request.method == 'POST':
        auth.logout(request)
        messages.success(request, 'You are now logged out')
        return redirect('index')

def dashboard(request):
    """
    Display the user's dashboard with their contacts.

    This view retrieves the contacts associated with the currently logged-in user,
    orders them by the contact date in descending order, and renders them on the dashboard page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered dashboard page displaying the user's contacts.
    """
    user_contacts = Contact.objects.order_by('-contact_date').filter(user_id=request.user.id)

    context = {
        'contacts': user_contacts
    }
    return render(request, 'accounts/dashboard.html', context)
