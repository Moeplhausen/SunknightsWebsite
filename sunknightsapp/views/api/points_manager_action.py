from rest_framework import viewsets
from ...serializers.pointsubmissions_serializer import PointsManagerActionSerializer
from ...models.point_submission import PointsManagerAction


class PointsManagerActionViewSet(viewsets.ModelViewSet):
    serializer_class = PointsManagerActionSerializer
    queryset = PointsManagerAction.objects.all()
