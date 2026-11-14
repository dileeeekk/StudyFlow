from unittest.mock import patch
from django.db import DatabaseError
from django.test import TestCase, override_settings


class HealthTests(TestCase):
    def test_health_is_public_but_has_no_account_data(self):
        result = self.client.get('/api/health/')
        self.assertEqual(result.status_code, 200)
        self.assertEqual(result.json(), {'status': 'ok'})
        self.assertEqual(result['Cache-Control'], 'no-store')
        self.assertEqual(self.client.post('/api/health/').status_code, 405)

    def test_database_errors_are_not_disclosed(self):
        with patch('config.health.get_user_model', side_effect=DatabaseError('private details')):
            result = self.client.get('/api/health/')
        self.assertEqual(result.status_code, 503)
        self.assertEqual(result.json(), {'status': 'unavailable'})

    @override_settings(SECURE_SSL_REDIRECT=True, ALLOWED_HOSTS=['studyflow-test.pythonanywhere.com'])
    def test_https_is_required_and_unknown_hosts_are_rejected(self):
        host = 'studyflow-test.pythonanywhere.com'
        self.assertEqual(self.client.get('/api/health/', HTTP_HOST=host).status_code, 301)
        self.assertEqual(self.client.get('/api/health/', HTTP_HOST=host, secure=True).status_code, 200)
        self.assertEqual(self.client.get('/api/health/', HTTP_HOST='invalid.example', secure=True).status_code, 400)
