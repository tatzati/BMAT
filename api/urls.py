from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from api.views import WorkModelView

urlpatterns = [
    path('works/enrich', WorkModelView.as_view({'post': 'enrich'})),
]