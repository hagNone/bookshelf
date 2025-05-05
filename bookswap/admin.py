from django.contrib import admin
from bookswap.models import Genre, Book, FactBookListing, FactGenre, Request, FactRequest
# Register your models here.
admin.site.register(Genre)
admin.site.register(Book)
admin.site.register(FactBookListing)
admin.site.register(FactGenre)
admin.site.register(Request)
admin.site.register(FactRequest)