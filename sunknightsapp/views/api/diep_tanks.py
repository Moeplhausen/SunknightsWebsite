from rest_framework import viewsets
from ...serializers.TankSerializer import DiepTankSerializer,DiepTankInheritanceSerializer
from ...models.diep_tank import DiepTank,DiepTankInheritance


class DiepTanksViewSet(viewsets.ModelViewSet):
    serializer_class = DiepTankSerializer
    queryset = DiepTank.objects.all()

class DiepTanksInheritanceViewSet(viewsets.ModelViewSet):
    serializer_class = DiepTankInheritanceSerializer
    queryset = DiepTankInheritance.objects.all()