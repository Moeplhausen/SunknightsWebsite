from rest_framework import viewsets
from ...serializers.pointsubmissions_serializer import PointsManagerActionSerializer,BasicUserPointSubmissionSerializer,OneOnOneFightSubmissionSerializer
from ...models.point_submission import PointsManagerAction,BasicUserPointSubmission,OneOnOneFightSubmission


class PointsManagerActionViewSet(viewsets.ModelViewSet):
    serializer_class = PointsManagerActionSerializer
    queryset = PointsManagerAction.objects.all()


class BasicUserPointSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = BasicUserPointSubmissionSerializer
    queryset = BasicUserPointSubmission.objects.all()

class BasicFightsSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = OneOnOneFightSubmissionSerializer
    queryset = OneOnOneFightSubmission.objects.all()