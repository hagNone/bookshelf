from django.test import TestCase
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Book
from .forms import Book_Model_Form

class BookAppTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', email='test@example.com', password='pass123')
        self.book = Book.objects.create(book_name='Django Basics', book_author='John Doe', genre='Tech', user=self.user)

    # ---------- RegisterView ----------
    def test_register_view_get(self):
        response = self.client.get(reverse('register'))
        self.assertEqual(response.status_code, 200)

    def test_register_view_post_valid(self):
        session = self.client.session
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'pass123'
        })
        session = self.client.session
        self.assertIn("otp", session)
        self.assertIn("username", session)
        self.assertRedirects(response, reverse('verify_otp'))

    # ---------- VerifyOTPView ----------
    def test_verify_otp_valid(self):
        session = self.client.session
        session['otp'] = '123456'
        session['username'] = 'otpuser'
        session['email'] = 'otp@example.com'
        session['password'] = 'pass123'
        session.save()

        response = self.client.post(reverse('verify_otp'), {'otp': '123456'})
        self.assertRedirects(response, reverse('login'))
        self.assertTrue(User.objects.filter(username='otpuser').exists())

    def test_verify_otp_invalid(self):
        session = self.client.session
        session['otp'] = '123456'
        session.save()
        response = self.client.post(reverse('verify_otp'), {'otp': '000000'})
        self.assertContains(response, 'Invalid OTP')

    # ---------- LoginView ----------
    def test_login_view_get(self):
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)

    def test_login_valid(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'pass123'})
        self.assertRedirects(response, reverse('profile-page'))

    def test_login_invalid(self):
        response = self.client.post(reverse('login'), {'username': 'testuser', 'password': 'wrongpass'})
        self.assertContains(response, 'Password Invalid')

    # ---------- SearchBooksAPIView ----------
    def test_search_books_authenticated(self):
        self.client.login(username='testuser', password='pass123')
        response = self.client.get(reverse('search-books-page'), {'q': 'Django'})
        self.assertContains(response, 'Django Basics')

    def test_search_books_not_authenticated(self):
        response = self.client.get(reverse('search-books-page'))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('search-books-page')}")

    # ---------- BookDetailAPIView ----------
    def test_book_detail_authenticated(self):
        self.client.login(username='testuser', password='pass123')
        response = self.client.get(reverse('book-detail-page', args=[self.book.pk]))
        self.assertContains(response, 'Django Basics')

    def test_book_detail_not_authenticated(self):
        response = self.client.get(reverse('book-detail-page', args=[self.book.pk]))
        self.assertRedirects(response, f"{reverse('login')}?next={reverse('book-detail-page', args=[self.book.pk])}")

    # ---------- Userprofile ----------
    def test_profile_view_authenticated_get(self):
        self.client.login(username='testuser', password='pass123')
        response = self.client.get(reverse('profile-page'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'testuser')

    def test_profile_view_authenticated_post_valid(self):
        self.client.login(username='testuser', password='pass123')
        response = self.client.post(reverse('profile-page'), {
            'book_name': 'New Book',
            'book_author': 'Author',
            'book_description': 'Some desc',
            'genre': 'Fiction'
        })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Book.objects.filter(book_name='New Book').exists())

    def test_profile_view_post_invalid(self):
        self.client.login(username='testuser', password='pass123')
        response = self.client.post(reverse('profile-page'), {
            'book_author': 'Missing name field',
        })
        self.assertContains(response, 'Form entry is invalid')

    # ---------- Logout ----------
    def test_logout_redirect(self):
        self.client.login(username='testuser', password='pass123')
        response = self.client.get(reverse('logout'))
        self.assertRedirects(response, reverse('login'))
