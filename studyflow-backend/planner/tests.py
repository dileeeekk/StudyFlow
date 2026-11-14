from django.contrib.auth import get_user_model
from django.core.cache import cache
from rest_framework.test import APITestCase


class PlannerTests(APITestCase):
    def setUp(self):
        cache.clear()
        User = get_user_model()
        self.user = User.objects.create_user('one@example.com', 'Orbit!98Password')
        self.other = User.objects.create_user('two@example.com', 'Orbit!98Password')
        self.client.force_authenticate(self.user)

    def post(self, kind, data=None, **kwargs):
        return self.client.post('/api/planner/', {'kind': kind, 'action': 'save', 'data': data or {}, **kwargs}, format='json')

    def test_empty_and_authentication(self):
        self.assertEqual(self.client.get('/api/planner/').data, {'tasks': [], 'lessons': [], 'notes': [], 'focus': [], 'goal': None})
        self.client.force_authenticate(None)
        self.assertEqual(self.client.get('/api/planner/').status_code, 401)

    def test_task_completion_edit_delete_and_isolation(self):
        r = self.post('tasks', {'title': 'Read chapter', 'due_at': '2026-12-01T12:00:00Z', 'priority': 'high', 'owner': self.other.pk})
        self.assertEqual(r.status_code, 200)
        task = r.data['tasks'][0]
        r = self.post('tasks', {'completed': True}, id=task['id'])
        self.assertIsNotNone(r.data['tasks'][0]['completed_at'])
        self.assertIsNone(self.post('tasks', {'completed': False}, id=task['id']).data['tasks'][0]['completed_at'])
        self.client.force_authenticate(self.other)
        self.assertEqual(self.client.get('/api/planner/').data['tasks'], [])
        self.assertEqual(self.post('tasks', {'title': 'Stolen'}, id=task['id']).status_code, 404)
        self.assertEqual(self.post('tasks', action='delete', id=task['id']).status_code, 404)
        self.client.force_authenticate(self.user)
        self.assertEqual(self.post('tasks', action='delete', id=task['id']).data['tasks'], [])

    def test_validation(self):
        self.assertEqual(self.post('tasks', {'title': ' ', 'due_at': 'bad'}).status_code, 400)
        self.assertEqual(self.post('lessons', {'title': 'Math', 'starts_at': '2026-12-01T14:00:00Z', 'ends_at': '2026-12-01T13:00:00Z'}).status_code, 400)
        for minutes in (0, -1, 1441):
            self.assertEqual(self.post('focus', {'minutes': minutes, 'date': '2026-01-01'}).status_code, 400)
        self.assertEqual(self.post('focus', {'minutes': 30, 'date': '2099-01-01'}).status_code, 400)
        self.assertEqual(self.post('tasks', id='bad').status_code, 400)

    def test_lessons_notes_goal_and_focus_persist(self):
        self.assertEqual(self.post('lessons', {'title': 'Math', 'starts_at': '2026-12-01T14:00:00Z', 'ends_at': '2026-12-01T15:00:00Z', 'room': 'B-204'}).status_code, 200)
        self.assertEqual(self.post('notes', {'title': 'Revision', 'body': 'Chapter 3'}).status_code, 200)
        self.assertEqual(self.post('goal', {'weekly_minutes': 720}).status_code, 200)
        self.assertEqual(self.post('goal', {'weekly_minutes': 600}).data['goal']['weekly_minutes'], 600)
        self.assertEqual(self.post('focus', {'minutes': 45, 'date': '2026-01-01'}).status_code, 200)
        r = self.client.get('/api/planner/').data
        self.assertEqual([len(r[k]) for k in ('lessons','notes','focus')], [1,1,1])
        self.client.force_authenticate(self.other)
        self.assertIsNone(self.client.get('/api/planner/').data['goal'])
