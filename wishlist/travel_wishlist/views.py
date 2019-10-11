from django.shortcuts import render, redirect, get_object_or_404
from .models import Place
from .forms import NewPlaceForm

# Create your views here.
def place_list(request):

    # if POST request where the user click the add button save a new place
    # to the database and redirect it to the same page 
    if request.method == 'POST':
        form = NewPlaceForm(request.POST) 
        place = form.save() # Create a new Place from the form
        if form.is_valid(): # Check if the required fields are present
            place.save() # Save to the database
            return redirect('place_list') # Redirect to GET view with name place_list

    places = Place.objects.filter(visited=False).order_by('name')
    new_place_form = NewPlaceForm()
    return render(request, 'travel_wishlist/wishlist.html', { 'places': places, 'new_place_form': new_place_form })

def places_visited(request):

    visited = Place.objects.filter(visited=True)
    return render(request, 'travel_wishlist/visited.html', { 'visited': visited})

def place_was_visited(request):
    
    if request.method == 'POST':
        pk = request.POST.get('pk')
        place = get_object_or_404(Place, pk=pk)
        place.visited = True
        place.save()
    
    return redirect('place_list')