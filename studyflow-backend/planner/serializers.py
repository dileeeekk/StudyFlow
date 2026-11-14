from rest_framework import serializers
from django.utils import timezone
from .models import Task, Lesson, Note, FocusSession, StudyGoal


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ('id', 'title', 'subject', 'due_at', 'priority', 'completed', 'completed_at')
        read_only_fields = ('id', 'completed_at')

    def update(self, instance, validated_data):
        if 'completed' in validated_data:
            done = validated_data['completed']
            validated_data['completed_at'] = (instance.completed_at or timezone.now()) if done else None
        return super().update(instance, validated_data)

    def create(self, validated_data):
        if validated_data.get('completed'):
            validated_data['completed_at'] = timezone.now()
        return super().create(validated_data)


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'room', 'lecturer', 'starts_at', 'ends_at')
        read_only_fields = ('id',)

    def validate(self, attrs):
        start = attrs.get('starts_at', getattr(self.instance, 'starts_at', None))
        end = attrs.get('ends_at', getattr(self.instance, 'ends_at', None))
        if start and end and end <= start:
            raise serializers.ValidationError({'ends_at': 'End time must be after start time.'})
        return attrs


class NoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Note
        fields = ('id', 'title', 'body')
        read_only_fields = ('id',)


class FocusSerializer(serializers.ModelSerializer):
    class Meta:
        model = FocusSession
        fields = ('id', 'minutes', 'date')
        read_only_fields = ('id',)

    def validate_date(self, value):
        if value > timezone.localdate():
            raise serializers.ValidationError('Study time cannot be recorded in the future.')
        return value


class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = StudyGoal
        fields = ('weekly_minutes',)
