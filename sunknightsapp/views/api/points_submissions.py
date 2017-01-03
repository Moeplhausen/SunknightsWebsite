from rest_framework import viewsets
from ...serializers.pointsubmissions_serializer import PointsManagerActionSerializer,BasicUserPointSubmissionSerializer
from ...models.point_submission import PointsManagerAction,BasicUserPointSubmission


class PointsManagerActionViewSet(viewsets.ModelViewSet):
    serializer_class = PointsManagerActionSerializer
    queryset = PointsManagerAction.objects.all()


class BasicUserPointSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = BasicUserPointSubmissionSerializer
    queryset = BasicUserPointSubmission.objects.all()

