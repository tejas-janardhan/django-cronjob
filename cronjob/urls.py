from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from .views import JobEndpoint

urlpatterns = [
    path('<str:job_group>/<str:token>', csrf_exempt(JobEndpoint.as_view()), name='job_group'),
]