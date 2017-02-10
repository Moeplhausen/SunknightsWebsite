from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer,BulkSerializerMixin
from ..models.diep_tank import DiepTank,DiepTankInheritance


class DiepTankSimpleSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class Meta:
        model=DiepTank
        fields=('id','name','opness')
        list_serializer_class = BulkListSerializer


class DiepTankSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    class DiepTankInheritanceSimpleSerializer(BulkSerializerMixin,serializers.ModelSerializer):
        parent=DiepTankSimpleSerializer(many=False,read_only=True)

        class Meta:
            model=DiepTankInheritance
            fields=('parent',)
            list_serializer_class = BulkListSerializer


    inheritance=DiepTankInheritanceSimpleSerializer(many=True,read_only=True)

    class Meta:
        model=DiepTank
        fields=('id','name','diep_isDeleted','opness','tier','inheritance')
        list_serializer_class = BulkListSerializer



class DiepTankInheritanceSerializer(BulkSerializerMixin,serializers.ModelSerializer):
    parent=DiepTankSerializer(many=False,read_only=True)
    me=DiepTankSerializer(many=False,read_only=True)

    class Meta:
        model=DiepTankInheritance
        fields=('parent','me')
        list_serializer_class = BulkListSerializer



