from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from .models import Task, Lesson, Note, FocusSession, StudyGoal
from .serializers import TaskSerializer, LessonSerializer, NoteSerializer, FocusSerializer, GoalSerializer

TYPES = {'tasks': (Task, TaskSerializer), 'lessons': (Lesson, LessonSerializer),
         'notes': (Note, NoteSerializer), 'focus': (FocusSession, FocusSerializer)}


def snapshot(user):
    result = {key: serializer(model.objects.filter(owner=user).order_by('id'), many=True).data
              for key, (model, serializer) in TYPES.items()}
    goal = StudyGoal.objects.filter(owner=user).first()
    result['goal'] = GoalSerializer(goal).data if goal else None
    return result


class PlannerView(APIView):
    throttle_scope = 'planner'

    def get(self, request):
        return Response(snapshot(request.user))

    @transaction.atomic
    def post(self, request):
        kind = request.data.get('kind')
        action = request.data.get('action')
        if kind == 'goal' and action in ('save', 'delete'):
            if action == 'delete':
                StudyGoal.objects.filter(owner=request.user).delete()
            else:
                serializer = GoalSerializer(data=request.data.get('data', {}))
                serializer.is_valid(raise_exception=True)
                StudyGoal.objects.update_or_create(owner=request.user, defaults=serializer.validated_data)
        elif kind in TYPES and action in ('save', 'delete'):
            model, serializer_class = TYPES[kind]
            object_id = request.data.get('id')
            if object_id is not None and (type(object_id) is not int or object_id < 1):
                raise ValidationError({'id': 'Invalid identifier.'})
            obj = get_object_or_404(model, owner=request.user, id=object_id) if object_id else None
            if action == 'delete':
                if obj is None:
                    raise ValidationError({'id': 'An identifier is required.'})
                obj.delete()
            else:
                serializer = serializer_class(obj, data=request.data.get('data', {}), partial=obj is not None)
                serializer.is_valid(raise_exception=True)
                serializer.save(owner=request.user)
        else:
            raise ValidationError({'detail': 'Unknown planner action.'})
        return Response(snapshot(request.user))
