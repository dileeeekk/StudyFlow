from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class Owned(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        abstract = True


class Task(Owned):
    title = models.CharField(max_length=160)
    subject = models.CharField(max_length=120, blank=True)
    due_at = models.DateTimeField()
    priority = models.CharField(max_length=6, choices=[('high', 'High'), ('medium', 'Medium'), ('low', 'Low')], default='medium')
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)


class Lesson(Owned):
    title = models.CharField(max_length=160)
    room = models.CharField(max_length=120, blank=True)
    lecturer = models.CharField(max_length=120, blank=True)
    starts_at = models.DateTimeField()
    ends_at = models.DateTimeField()


class Note(Owned):
    title = models.CharField(max_length=160)
    body = models.TextField(max_length=5000, blank=True)


class FocusSession(Owned):
    minutes = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(1440)])
    date = models.DateField()


class StudyGoal(models.Model):
    owner = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    weekly_minutes = models.PositiveIntegerField(validators=[MinValueValidator(30), MaxValueValidator(10080)])
