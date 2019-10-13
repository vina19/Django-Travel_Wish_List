from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm

# View for place list
def place_list(request):

    # if POST request where the user click the add button save a new place
    # to the database and redirect it to the same page 
    if request.method == 'POST':
        form = NewPlaceForm(request.POST) 
        place = form.save() # Create a new Place from the form
        if form.is_valid(): # Check if the required fields are present
            place.save() # Save to the database
            return redirect('place_list') # Redirect to GET view with name place_list

    # if not POST, or the form is not valid, render the page
    # with the form to add a new place, and list of places
    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', { 'places': places, 'new_place_form': new_place_form })

# View for visited places
def places_visited(request):

    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited})

# View for if the place was visited by the user
def place_was_visited(request):
    
    # if POST where the user click the visited button save as a visited place
    # to the database and redirect it to GET view of place_list
    if request.method == 'POST':
        pk = request.POST.get('pk') 
        place = get_object_or_404(Place, pk=pk)
        place.visited = True
        place.save()
    
    return redirect('place_list')