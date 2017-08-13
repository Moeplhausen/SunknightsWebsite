from rest_framework import viewsets
from ...serializers.tank_serializer import DiepTankSerializer,DiepTankInheritanceSerializer
from ...models.diep_tank import DiepTank,DiepTankInheritance


class DiepTanksViewSet(viewsets.ModelViewSet):
    serializer_class = DiepTankSerializer
    queryset = DiepTank.objects.prefetch_related('inheritance','inheritance__parent').all()

class DiepTanksInheritanceViewSet(viewsets.ModelViewSet):
    serializer_class = DiepTankInheritanceSerializer
    queryset = DiepTankInheritance.objects.all()