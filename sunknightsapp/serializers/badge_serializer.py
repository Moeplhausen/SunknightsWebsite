from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer,BulkSerializerMixin
from ..models.badge import Badge


class BadgeSerializer(BulkSerializerMixin,serializers.ModelSerializer):

    class Meta:
        model=Badge
        fields=('id','tank','manager','pointsinfo')
        list_serializer_class = BulkListSerializer




