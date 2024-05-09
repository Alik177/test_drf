from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


# class Product(models.Model):
#     name = models.CharField(max_length=255)
#     description = models.TextField()
#     price = models.DecimalField(max_digits=12, decimal_places=2)



class Author(models.Model):
    name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Currency(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=3)

    def __str__(self):
        return self.name
class Genre(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
class Book(models.Model):
    name = models.CharField(max_length=100)
    author = models.ForeignKey(Author, on_delete=models.CASCADE) #related_name='books',
    publication_year = models.IntegerField()
    genres = models.ManyToManyField(Genre)
    description = models.TextField()
    image = models.ImageField(upload_to='books/', null=True, blank=True)
    audio = models.FileField(upload_to='books/audio/', null=True, blank=True)
    video = models.FileField(upload_to='books/video/', null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.ForeignKey(Currency, on_delete=models.CASCADE) #  related_name='books',

    def __str__(self):
        return self.name

class Review(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE)
    review_description = models.TextField()

    def __str__(self):
        return f"Review of {self.book.name} by {self.reviewer}"

class Purchase(models.Model):
    items = models.ManyToManyField('PurchaseItem')
    total = models.PositiveIntegerField()
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(default=timezone.now)

class PurchaseItem(models.Model):
    book = models.ForeignKey('Book', on_delete=models.SET_NULL, null=True)
    quantity = models.PositiveSmallIntegerField(default=1)
    subtotal = models.PositiveIntegerField()


