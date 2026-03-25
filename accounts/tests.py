from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User


class AuthPageTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser", email="test@test.com", password="testpass123"
        )

    def test_auth_page_loads(self):
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)

    def test_login_valid_credentials(self):
        response = self.client.post(reverse("accounts:login"), {
            "form_type": "login",
            "username": "testuser",
            "password": "testpass123",
        })
        self.assertRedirects(response, reverse("home"))

    def test_login_invalid_credentials(self):
        response = self.client.post(reverse("accounts:login"), {
            "form_type": "login",
            "username": "testuser",
            "password": "wrongpassword",
        })
        self.assertEqual(response.status_code, 200)
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any("Invalid login" in str(m) for m in messages))

    def test_register_creates_user(self):
        response = self.client.post(reverse("accounts:login"), {
            "form_type": "register",
            "username": "newuser",
            "email": "new@test.com",
            "password": "newpass123",
            "confirm": "newpass123",
        })
        self.assertTrue(User.objects.filter(username="newuser").exists())

    def test_register_passwords_dont_match(self):
        response = self.client.post(reverse("accounts:login"), {
            "form_type": "register",
            "username": "newuser",
            "email": "new@test.com",
            "password": "newpass123",
            "confirm": "differentpass",
        })
        self.assertFalse(User.objects.filter(username="newuser").exists())
        messages = list(response.wsgi_request._messages)
        self.assertTrue(any("Passwords do not match" in str(m) for m in messages))
    
    def test_register_duplicate_username(self):
        response = self.client.post(reverse("accounts:login"), {
            "form_type": "register",
            "username": "testuser",
            "email": "other@test.com",
            "password": "newpass123",
            "confirm": "newpass123",
        })
        self.assertEqual(User.objects.filter(username="testuser").count(), 1)


class LogoutTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass123")

    def test_logout_redirects_home(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("accounts:logout"))
        self.assertRedirects(response, reverse("home"))

    def test_logout_logs_user_out(self):
        self.client.login(username="testuser", password="testpass123")
        self.client.get(reverse("accounts:logout"))
        response = self.client.get(reverse("accounts:profile"))
        self.assertNotEqual(response.status_code, 200)


class ProfileViewTests(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="testpass123")

    def test_profile_redirects_if_not_logged_in(self):
        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, 302)
        self.assertIn("/accounts/login/", response["Location"])

    def test_profile_loads_when_logged_in(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("accounts:profile"))
        self.assertEqual(response.status_code, 200)

    def test_profile_shows_username(self):
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("accounts:profile"))
        self.assertContains(response, "testuser")