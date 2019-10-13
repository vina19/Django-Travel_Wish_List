from django.test import TestCase
from django.urls import reverse

from .models import Place

# Test if the home page show an empty list.
class TestHomePageIsEmptyList(TestCase):

    def test_load_home_page_shows_empty_list(self):

        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html') # Check correct template used
        self.assertFalse(response.context['places']) # Data used to populate the template
        self.assertContains(response, 'You have no places in your wishlist') # Check correct display message

# Test if the wishlist page contains not visited places.
class TestWishList(TestCase):
    
    # load the test_place.json fixtures file
    fixtures = ['test_place'] 

    def test_view_wishlist_contains_not_visited_places(self):

        response = self.client.get(reverse('place_list'))
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html') # Check correct template used

        # Check if the wishlist contains Tokyo and New York which not visited by the user
        # and not contains San Francisco and Moab which user visited
        self.assertContains(response, 'Tokyo')
        self.assertContains(response, 'New York')
        self.assertNotContains(response, 'San Francisco')
        self.assertNotContains(response, 'Moab')

class TestNoPlacesVisitedMessage(TestCase):

    def test_display_message_for_no_places_visited(self):

        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html') # Check correct template used
        self.assertFalse(response.context['visited']) # Data used to populate the template
        self.assertContains(response, 'You have not visited any places yet.') # Check correct display message

class TestVisitedPlaces(TestCase):

    # load the test_place.json fixtures file
    fixtures = ['test_place']

    def test_only_visited_places_are_displayed(self):
        response = self.client.get(reverse('places_visited'))
        self.assertTemplateUsed(response, 'travel_wishlist/visited.html') # Check correct template used
        
        # Check if the visited places contains Moab and San Francisco
        # and not contains Tokyo and New York which not visited by the user
        self.assertContains(response, 'Moab')
        self.assertContains(response, 'San Francisco')
        self.assertNotContains(response, 'Tokyo')
        self.assertNotContains(response, 'New York')

class TestAddNewPlace(TestCase):

    def test_add_new_unvisited_place_to_wishlist(self):

        response = self.client.post(reverse('place_list'), { 'name': 'Tokyo', 'visited': False }, follow=True)

        # Check correct template used
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        # Data used to populate the template
        response_places = response.context['places']

        # Check it should be 1 item
        self.assertEqual(len(response_places), 1)
        tokyo_response = response_places[0]

        # Expect this data to be in the database.
        # Use get() to get data with the values expected. 
        # Will throw an exception if no data, or more than one row matches.
        # Remember throwing an exception will cause this test to fail.
        tokyo_in_database = Place.objects.get(name='Tokyo', visited=False)

        # Is the data used to render the template, the same as the data in the database?
        self.assertEqual(tokyo_response, tokyo_in_database)
    
    def test_add_new_visited_place_to_wishlist(self):

        response =  self.client.post(reverse('place_list'), { 'name': 'Tokyo', 'visited': True }, follow=True)

        # Check correct template was used
        self.assertTemplateUsed(response, 'travel_wishlist/wishlist.html')

        # What data was used to populate the template?
        response_places = response.context['places']

        # Should be 0 items - have not added any un-visited places
        self.assertEqual(len(response_places), 0)

        # Expect this data to be in the database. Use get() to get data with
        # the values expected. Will throw an exception if no data, or more than
        # one row, matches. Remember throwing an exception will cause this test to fail
        place_in_database = Place.objects.get(name="Tokyo", visited=True)