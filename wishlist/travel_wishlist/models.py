from django.db import models

# Create Place model with two fields
# (name and if the user has visited or not)
class Place(models.Model):
    user = models.ForeignKey('auth.user', null=False, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)
    notes = models.TextField(blank=True, null=True)
    date_visited = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='user_images/', blank=True, null=True)

    def __str__(self):
        photo_str = self.photo.url if self.photo else 'no photo'
        return f'{self.name}, visited? {self.visited} on {self.date_visited}\nPhoto {photo_str}'
