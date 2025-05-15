from django import forms
from .models import Book


class Book_Model_Form(forms.ModelForm):
    class Meta:
        model = Book
        fields=['book_name','book_author','book_description','genre']
        widgets = {
            'genre':forms.Select()
        }