from django.db import models
from django.db.models import UniqueConstraint
from django.db.models.functions import Lower
from django.urls import reverse
import uuid

class Genre(models.Model):
    name = models.CharField(max_length=64, unique=True ,help_text="enter the books genre")

    def __str__(self):
        return {self.name}

    def get_absolute_url(self):
        return reverse("genre_detail",args=[str(self.id)])
    
    class Meta:
        constraints=[
            UniqueConstraint(Lower('name'),name='genre_name_case_insensitive_unique',
                violation_error_message = "Genre already exists (case insensitive match)")
        ]

class Language(models.Model):
    name = models.CharField(max_length=64,unique=True,help_text="Select the language")
    
    def __str__(self):
        return {self.name}

    def get_absolute_url(self):
        return reverse("language_detail",args=[str(self.id)])
    class Meta:
        constraints = [UniqueConstraint(Lower("name"),
                                        name='language_name_case_insensitive_unique',
                violation_error_message = "Language already exists (case insensitive match)")]

class Book(models.Model):
    title = models.CharField(max_length=128)
    author = models.ForeignKey('Author',on_delete=models.RESTRICT,null=True)
    summary = models.TextField(max_length=1024,help_text="enter a description of the book")
    isbn = models.CharField("isbn",max_length=13,unique=True,help_text='13 Character <a href="https://www.isbn-international.org/content/what-isbn'
                                      '">ISBN number</a>')
    genre = models.ManyToManyField(Genre,help_text="Select a genre for this book")
    language = models.ForeignKey('Language',on_delete=models.SET_NULL,null=True)

    def __str__(self):
        return self.title
    def get_absolute_url(self):
        return reverse('book-detail',args=[str(self.id)])
    
class BookInstance(models.Model):
    id = models.UUIDField(primary_key=True,default=uuid.uuid4,
                          help_text="Unique ID for this particular book across whole library")
    book = models.ForeignKey('Book',on_delete=models.RESTRICT,null=True)
    imprint = models.CharField(max_length=64)
    due_back = models.DateField(null=True,blank=True)
    LOAN_STATUS = (('m', 'Maintenance'),('o', 'On loan'),('a', 'Available'),('r', 'Reserved'),)
    status = models.CharField(max_length=1,choices=LOAN_STATUS,blank=True,default='m',help_text="Book availability")
    
    class Meta:
        ordering = ["-due_back"]

    def __str__(self):
        return f'{self.id} ({self.book.title})'

    class Author(models.Model):
        first_name = models.CharField(max_length=100)
        last_name = models.CharField(max_length=100)
        date_of_birth = models.DateField(null=True,blank=True)
        date_of_death = models.DateField("Died",null=True,blank=True)

        class Meta:
            ordering = ['last_name', 'first_name']
        def get_absolute_url(self):
            """Returns the URL to access a particular author instance."""
            return reverse('author-detail', args=[str(self.id)])

        def __str__(self):
            """String for representing the Model object."""
            return f'{self.last_name}, {self.first_name}'


