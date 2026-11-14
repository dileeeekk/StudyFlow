from django.contrib.auth import get_user_model
from django.db import DatabaseError
from django.http import JsonResponse
from django.views.decorators.http import require_safe


@require_safe
def health(request):
    """Public connectivity probe with no account details or exception messages."""
    try:
        get_user_model().objects.exists()
    except DatabaseError:
        return JsonResponse({'status': 'unavailable'}, status=503)
    response = JsonResponse({'status': 'ok'})
    response['Cache-Control'] = 'no-store'
    return response
