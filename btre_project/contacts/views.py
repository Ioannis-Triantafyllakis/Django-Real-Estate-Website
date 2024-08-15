from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from .models import Contact

def contact(request):
    """
    Handle contact form submissions for property listings.

    If the request method is POST, this view processes the contact form data submitted 
    by the user. It checks if the user has already made an inquiry for the same listing.
    If an inquiry has already been made, an error message is displayed, and the user is 
    redirected back to the listing page.

    If the inquiry is new, the form data is saved as a new Contact object in the database. 
    An email notification to the realtor is prepared (but currently commented out). 
    A success message is displayed, and the user is redirected back to the listing page.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: A redirect to the listing page, with appropriate messages based on 
                      the form submission.
    """
    if request.method == 'POST':
        listing_id = request.POST['listing_id']
        listing = request.POST['listing']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']
        message = request.POST['message']
        user_id = request.POST['user_id']
        realtor_email = request.POST['realtor_email']

        # Check if user has made inquiry already
        if request.user.is_authenticated:
            user_id = request.user.id
            has_contacted = Contact.objects.all().filter(listing_id=listing_id, user_id=user_id)
            if has_contacted:
                messages.error(request, 'You have already made an inquiry for this listing')
                return redirect('/listings/' + listing_id)

        contact = Contact(
            listing=listing, 
            listing_id=listing_id, 
            name=name, 
            email=email, 
            phone=phone, 
            message=message, 
            user_id=user_id
        )

        contact.save()

        # Send email (currently commented out)
        # send_mail(
        #   'Property Listing Inquiry',
        #   'There has been an inquiry for ' + listing + '. Sign into the admin panel for more info',
        #   'traversy.brad@gmail.com',
        #   [realtor_email, 'techguyinfo@gmail.com'],
        #   fail_silently=False
        # )

        messages.success(request, 'Your request has been submitted, a realtor will get back to you soon')
        return redirect('/listings/' + listing_id)
