from django.urls import path

from api.views import WorkModelView

urlpatterns = [
    path('works/enrich', WorkModelView.as_view({'post': 'enrich'})),
]