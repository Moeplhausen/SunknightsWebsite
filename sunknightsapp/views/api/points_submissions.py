from rest_framework import viewsets
from ...serializers.pointsubmissions_serializer import PointsManagerActionSerializer, BasicUserPointSubmissionSerializer, OneOnOneFightSubmissionSerializer, BasicEventQuestsSubmissionSerializer
from ...models.point_submission import PointsManagerAction, BasicUserPointSubmission, OneOnOneFightSubmission, EventQuestSubmission


class PointsManagerActionViewSet(viewsets.ModelViewSet):
    serializer_class = PointsManagerActionSerializer
    queryset = PointsManagerAction.objects.all()


class BasicUserPointSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = BasicUserPointSubmissionSerializer
    queryset = BasicUserPointSubmission.objects.all()


class BasicFightsSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = OneOnOneFightSubmissionSerializer
    queryset = OneOnOneFightSubmission.objects.all()


class BasicEventQuestsSubmissionViewSet(viewsets.ModelViewSet):
    serializer_class = BasicEventQuestsSubmissionSerializer
    queryset = EventQuestSubmission.objects.all()
