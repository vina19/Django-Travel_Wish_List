from django.urls import path
from . import views

# The travel_wishlist app url patterns
urlpatterns = [
    path('', views.place_list, name='place_list')
]