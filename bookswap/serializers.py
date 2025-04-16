from django.contrib.auth.models import User
from rest_framework import serializers
from .models import FactBookListing

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}


class Bookname(serializers.ModelSerializer):
    book_name=serializers.CharField(source="book_id.book_name")

    class meta:
        model=FactBookListing
        fields=["id","book_name"]

class bookdetails(serializers.ModelSerializer):
    book_name=serializers.CharField(source="book_id.book_name")
    genre=serializers.CharField(source="book_id.genre_id.genre_name")
    username=serializers.CharField(source="user_id.username")

    class meta:
        model=FactBookListing
        fields=['id','bookname','username','genre']

"""from django.views import View
from django.shortcuts import render
from django.db.models import Q
from .models import Book, FactBookListing
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

@method_decorator(login_required, name='dispatch')
class search(View):
    def get(self, request):
        query = request.GET.get("q")
        context = {}

        if query:
            listings = FactBookListing.objects.filter(
                book__book_name__icontains=query
            ).select_related('user', 'book__genre')

            if listings.exists():
                context['results'] = []
                for listing in listings:
                    context['results'].append({
                        'user': listing.user.username,
                        'book': listing.book.book_name,
                        'genre': listing.book.genre.genre_name
                    })
            else:
                context['error'] = "No books found with that name."
        else:
            context['error'] = "Please enter a book name to search."

        return render(request, "search.html", context)
"""