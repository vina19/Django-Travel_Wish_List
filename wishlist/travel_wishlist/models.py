from django.db import models

# Create Place model with two fields
# (name and if the user has visited or not)
class Place(models.Model):
    name = models.CharField(max_length=200)
    visited = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.name}, visited? {self.visited}'
