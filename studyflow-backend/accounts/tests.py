from datetime import timedelta
from django.contrib.auth import get_user_model
from django.core.cache import cache
from django.utils import timezone
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import AccessToken


class AuthenticationTests(APITestCase):
    def setUp(self):
        cache.clear()
        self.data = {'email': 'student@example.com', 'full_name': 'Test Student',
                     'university': 'Test University', 'password': 'StudyFlow!94Orbit', 'terms_accepted': True}

    def register(self):
        response = self.client.post('/api/auth/register/', self.data, format='json')
        self.assertEqual(response.status_code, 201, response.data)
        return response.data

    def test_register_hashes_password_returns_profile_and_protects_me(self):
        data = self.register()
        user = get_user_model().objects.get(email=self.data['email'])
        self.assertTrue(user.check_password(self.data['password']))
        self.assertNotEqual(user.password, self.data['password'])
        self.assertIsNotNone(user.terms_accepted_at)
        self.assertNotIn('password', data['user'])
        self.assertEqual(self.client.get('/api/auth/me/').status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])
        self.assertEqual(self.client.get('/api/auth/me/').data['email'], self.data['email'])
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['refresh'])
        self.assertEqual(self.client.get('/api/auth/me/').status_code, 401)

    def test_login_case_insensitive_and_invalid_credentials(self):
        self.register()
        response = self.client.post('/api/auth/login/', {'email': 'STUDENT@EXAMPLE.COM', 'password': self.data['password']}, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('refresh', response.data)
        self.assertEqual(self.client.post('/api/auth/login/', {'email': self.data['email'], 'password': 'WrongPassword!'}, format='json').status_code, 401)

    def test_required_fields_consent_password_and_duplicate(self):
        for field in ['email', 'full_name', 'university', 'password', 'terms_accepted']:
            cache.clear()
            bad = self.data.copy(); bad.pop(field)
            self.assertEqual(self.client.post('/api/auth/register/', bad, format='json').status_code, 400)
        for field, value in [('terms_accepted', False), ('password', 'short'), ('password', '        '), ('full_name', '  '), ('university', '  '), ('email', 'not-email')]:
            cache.clear()
            bad = {**self.data, field: value}
            self.assertEqual(self.client.post('/api/auth/register/', bad, format='json').status_code, 400)
        cache.clear(); self.register()
        self.assertEqual(self.client.post('/api/auth/register/', {**self.data, 'email': 'STUDENT@EXAMPLE.COM'}, format='json').status_code, 400)

    def test_refresh_rotates_and_old_refresh_is_rejected(self):
        data = self.register()
        result = self.client.post('/api/auth/refresh/', {'refresh': data['refresh']}, format='json')
        self.assertEqual(result.status_code, 200)
        self.assertNotEqual(result.data['refresh'], data['refresh'])
        self.assertEqual(self.client.post('/api/auth/refresh/', {'refresh': data['refresh']}, format='json').status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + result.data['access'])
        self.assertEqual(self.client.get('/api/auth/me/').status_code, 200)

    def test_expired_or_modified_access_is_rejected(self):
        data = self.register()
        token = AccessToken(data['access']); token.set_exp(from_time=timezone.now() - timedelta(minutes=10), lifetime=timedelta(seconds=1))
        for access in [str(token), data['access'][:-10] + 'invalidXYZ']:
            self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + access)
            self.assertEqual(self.client.get('/api/auth/me/').status_code, 401)

    def test_logout_revokes_refresh(self):
        data = self.register()
        self.assertEqual(self.client.post('/api/auth/logout/', {'refresh': data['refresh']}, format='json').status_code, 200)
        self.assertEqual(self.client.post('/api/auth/refresh/', {'refresh': data['refresh']}, format='json').status_code, 401)

    def test_inactive_user_cannot_login_refresh_or_use_access(self):
        data = self.register()
        user = get_user_model().objects.get(email=self.data['email']); user.is_active = False; user.save()
        self.assertEqual(self.client.post('/api/auth/login/', {'email': self.data['email'], 'password': self.data['password']}, format='json').status_code, 401)
        self.assertEqual(self.client.post('/api/auth/refresh/', {'refresh': data['refresh']}, format='json').status_code, 401)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + data['access'])
        self.assertEqual(self.client.get('/api/auth/me/').status_code, 401)

    def test_login_throttling(self):
        for _ in range(10):
            self.client.post('/api/auth/login/', {'email': 'unknown@example.com', 'password': 'WrongPassword!'}, format='json')
        self.assertEqual(self.client.post('/api/auth/login/', {'email': 'unknown@example.com', 'password': 'WrongPassword!'}, format='json').status_code, 429)
