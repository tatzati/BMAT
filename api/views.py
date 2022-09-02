from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from api.models import Work
from api.serializers import WorkSerializer, WorkEnrichSerializer


@method_decorator(csrf_exempt, name='dispatch')
class WorkModelView(viewsets.ModelViewSet):
    """
    View to enrich metadata.
    """

    @action(detail=False, methods=['post'])
    def enrich(self, request):
        serializer = WorkEnrichSerializer(data=request.data)
        list_to_filter_by = []
        if serializer.is_valid(raise_exception=True):
            list_to_filter_by = serializer.data.get("iswc")

        qs = Work.objects.filter(is_deleted=False).filter(iswc__in=list_to_filter_by)

        page = self.paginate_queryset(qs)
        if page is not None:
            serializer = WorkSerializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = WorkSerializer(qs, many=True)
        return Response(serializer.data)
