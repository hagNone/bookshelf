from django.db import models
from django.contrib.auth.models import User


def default_user():
    return User.objects.first().id

class Book(models.Model):
    Genre_Options = [
        ('horror', 'Horror'),
        ('thriller', 'Thriller'),
        ('romance', 'Romance'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE,default=default_user)  # Who posted the book
    book_id = models.AutoField(primary_key=True)
    book_name = models.CharField(max_length=255)
    book_author = models.CharField(max_length=255)
    book_description = models.TextField()
    genre = models.CharField(max_length=100, choices=Genre_Options)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.book_name

class Request(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('accepted', 'Accepted'),
        ('declined', 'Declined'),
    ]
    request_id = models.AutoField(primary_key=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    book = models.ForeignKey(Book, related_name='requests', on_delete=models.CASCADE)
    requester = models.ForeignKey(User, related_name='sent_requests', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_requests', on_delete=models.CASCADE)

    def __str__(self):
        return f"Request {self.request_id} - {self.status}"




























# from django.db import models
# from django.contrib.auth.models import User

# # -------------------------
# # Genre Model
# # -------------------------
# class Genre(models.Model):
#     Genre_Options = [
#         ('horror', 'Horror'),
#         ('thriller', 'Thriller'),
#         ('romance', 'Romance'),
#     ]
#     genre_ID = models.AutoField(primary_key=True)
#     genre_name = models.CharField(max_length=100, choices=Genre_Options)

#     def __str__(self):
#         return self.genre_name

# # -------------------------
# # |      Book Model        |
# # -------------------------
# class Book(models.Model):
#     Genre_Options = [
#         ('horror', 'Horror'),
#         ('thriller', 'Thriller'),
#         ('romance', 'Romance'),
#     ]

#     book_id = models.AutoField(primary_key=True)
#     book_name = models.CharField(max_length=255)
#     book_author = models.CharField(max_length=255)
#     book_description = models.TextField()
#     genre = models.CharField(max_length=100, choices=Genre_Options)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     # genre = models.ForeignKey(Genre, on_delete=models.PROTECT)

#     def __str__(self):
#         return self.book_name

# # -------------------------
# # User's Book Listings
# # -------------------------
# class FactBookListing(models.Model):
#     user = models.ForeignKey(User, on_delete=models.PROTECT)
#     book = models.ForeignKey(Book, on_delete=models.PROTECT)
#     listing_date = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.user.username} listed {self.book.book_name}"

# # -------------------------
# # User's Genre Interests
# # -------------------------
# class FactGenre(models.Model):
#     user = models.ForeignKey(User, on_delete=models.PROTECT)
#     genre = models.ForeignKey(Genre, on_delete=models.PROTECT)

#     def __str__(self):
#         return f"{self.user.username} is interested in {self.genre.genre_name}"

# # -------------------------
# # Request Model
# # -------------------------
# class Request(models.Model):
#     STATUS_CHOICES = [
#         ('pending', 'Pending'),
#         ('accepted', 'Accepted'),
#         ('declined', 'Declined'),
#     ]
#     request_id = models.AutoField(primary_key=True)
#     status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
#     book = models.ForeignKey(FactBookListing, related_name='requests', on_delete=models.PROTECT,default=1)
#     requester = models.ForeignKey(User, related_name='sent_requests', on_delete=models.PROTECT)

#     def __str__(self):
#         return f"Request {self.request_id} - {self.status}"

# # -------------------------
# # FactRequest Model (swap request table)
# # -------------------------
# class FactRequest(models.Model):
#     requester = models.ForeignKey(User, related_name='Fact_sent_requests', on_delete=models.PROTECT)
#     receiver = models.ForeignKey(User, related_name='Fact_received_requests', on_delete=models.PROTECT)
#     book = models.ForeignKey(Book, on_delete=models.PROTECT)
#     request = models.ForeignKey(Request, on_delete=models.PROTECT)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.requester.username} requested {self.book.book_name} from {self.receiver.username}"
