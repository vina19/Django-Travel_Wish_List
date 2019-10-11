from django.shortcuts import render
from .models import Place

# Create your views here.
def place_list(request):
    places = Place.objects.filter(visited=False)
    return render(request, 'travel_wishlist/wishlist.html', { 'places': places })
