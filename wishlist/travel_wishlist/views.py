from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm, TripReviewForm
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.contrib import messages


# Show the view of the place list
@login_required
def place_list(request):
    if request.method == 'POST':
        form = NewPlaceForm(request.POST)
        place = form.save(commit=False) # Create a new Place from the form
        place.user = request.user
        if form.is_valid(): # Checks against DB
            place.save()    # Saves to the database
            return redirect('place_list')   # Redirects to GET view place_list

    # If not a POST, or the form is not valid, render the page
    # with the form to add a new place, and list of place
    places = Place.objects.filter(user=request.user).filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', { 'places': places, 'new_place_form': new_place_form })

# View for visited places
@login_required
def places_visited(request):
    visited = Place.objects.filter(user=request.user).filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited })

# View for if the place was visited by the user
@login_required
def place_was_visited(request):
    
    # if POST where the user click the visited button save as a visited place
    # to the database and redirect it to GET view of place_list
    if request.method == 'POST':
        pk = request.POST.get('pk')
        place = get_object_or_404(Place,pk=pk)
        print(place.user, request.user)
        if place.user == request.user:
            place.visited = True
            place.save()
        else:
            return HttpResponseForbidden()
    
    return redirect('place_list')

# Show the place detail view
@login_required
def place_details(request, place_pk):

    place = get_object_or_404(Place, pk=place_pk)

    if request.method == 'POST':
        form = TripReviewForm(request.POST, request.FILES, instance=place)  # instance = model object to update with the form data
        # instance is the model object to update with the form data
        
        if form.is_valid():
            form.save()
            messages.info(request, 'Trip information updated!')
        else:
            messages.error(request, form.errors)  # Temp error message - future version should improve 

        return redirect('place_details', place_pk=place_pk)

    else:    # GET place details
        if place.visited:
            review_form = TripReviewForm(instance=place)  # Pre-populate with data from this Place instance
            return render(request, 'travel_wishlist/place_detail.html', {'place': place, 'review_form': review_form} )

        else:
            return render(request, 'travel_wishlist/place_detail.html', {'place': place} )

# Create a delete option view
@login_required
def delete_place(request):
    pk = request.POST.get('pk')
    place = get_object_or_404(Place, pk=pk)
    if place.user == request.user:
        place.delete()
        return redirect('place_list')
    else:
        return HttpResponseForbidden()