from django.contrib import admin
from django.urls import include, path
from .health import health
from planner.views import PlannerView

urlpatterns = [path('admin/', admin.site.urls), path('api/auth/', include('accounts.urls')),
               path('api/health/', health), path('api/planner/', PlannerView.as_view())]

