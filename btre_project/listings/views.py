from django.shortcuts import get_object_or_404, render
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from .choices import price_choices, bedroom_choices, state_choices
from .models import Listing

def index(request):
    """
    Display the main listings page with paginated listings.

    This view retrieves all published listings ordered by the date they were listed 
    (newest first). It then paginates the listings to display a limited number per page.

    The paginated listings are passed to the template for rendering.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered listings page with paginated listings.
    """
    listings = Listing.objects.order_by('-list_date').filter(is_published=True)

    paginator = Paginator(listings, 6)  # Show 6 listings per page
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)

    context = {
        'listings': paged_listings
    }

    return render(request, 'listings/listings.html', context)

def listing(request, listing_id):
    """
    Display a single listing's detail page.

    This view retrieves a specific listing by its ID. If the listing is not found,
    it returns a 404 error. The listing details are passed to the template for rendering.

    Args:
        request (HttpRequest): The HTTP request object.
        listing_id (int): The ID of the listing to display.

    Returns:
        HttpResponse: The rendered listing detail page.
    """
    listing = get_object_or_404(Listing, pk=listing_id)

    context = {
        'listing': listing
    }

    return render(request, 'listings/listing.html', context)

def search(request):
    """
    Handle searches for listings based on various criteria.

    This view allows users to filter listings by keywords, city, state, number of bedrooms,
    and price. The filtered results are passed to the template for rendering along with the 
    search choices and the current search values.

    Args:
        request (HttpRequest): The HTTP request object.

    Returns:
        HttpResponse: The rendered search results page with filtered listings.
    """
    queryset_list = Listing.objects.order_by('-list_date')

    # Keywords
    if 'keywords' in request.GET:
        keywords = request.GET['keywords']
        if keywords:
            queryset_list = queryset_list.filter(description__icontains=keywords)

    # City
    if 'city' in request.GET:
        city = request.GET['city']
        if city:
            queryset_list = queryset_list.filter(city__iexact=city)

    # State
    if 'state' in request.GET:
        state = request.GET['state']
        if state:
            queryset_list = queryset_list.filter(state__iexact=state)

    # Bedrooms
    if 'bedrooms' in request.GET:
        bedrooms = request.GET['bedrooms']
        if bedrooms:
            queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

    # Price
    if 'price' in request.GET:
        price = request.GET['price']
        if price:
            queryset_list = queryset_list.filter(price__lte=price)

    context = {
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'listings': queryset_list,
        'values': request.GET  # Preserves form input values in the search form
    }

    return render(request, 'listings/search.html', context)
