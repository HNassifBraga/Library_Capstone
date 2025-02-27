from django.contrib.auth.models import User
from django.db import models

# creating the table author
class Author(models.Model):
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    country_of_birth = models.CharField(max_length=100)
    date_of_death = models.DateField(null=True, blank=True)


    def __str__(self):
        return self.name    

# creating table book
class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='books')
    publication_date = models.DateField()
    description = models.CharField(max_length=250)
    genre = models.CharField(max_length=30)
    isRented = models.BooleanField()
    def __str__(self):
        return self.title
    
# creating table rented
class Rented(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='rented')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='rented_books')
    rented_date = models.DateField()
    return_date = models.DateField()
    returned_date = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.book.title} was rented rented by {self.user.username} on {self.rented_date}, the book should be returned at the day {self.return_date}, was returned at {self.returned_date}"
    
