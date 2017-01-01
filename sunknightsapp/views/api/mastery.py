from rest_framework import viewsets
from ...serializers.mastery_serializer import MasterySerializer
from ...models.mastery import Mastery


class MasteriesViewSet(viewsets.ModelViewSet):
    serializer_class = MasterySerializer
    queryset = Mastery.objects.all()

