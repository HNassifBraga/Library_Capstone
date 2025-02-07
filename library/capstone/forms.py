
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Book, Author
from django import forms

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields =( 'username', 'last_name','email', 'is_staff', 'first_name')

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'author','publication_date', 'description', 'genre']


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = ['name', 'date_of_birth','country_of_birth', 'date_of_death']





    