from rest_framework import viewsets
from ...serializers.badge_serializer import BadgeSerializer
from ...models.badge import Badge


class BadgesViewSet(viewsets.ModelViewSet):
    serializer_class = BadgeSerializer
    queryset = Badge.objects.all()

