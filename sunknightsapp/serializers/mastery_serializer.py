from rest_framework import serializers
from rest_framework_bulk import BulkListSerializer,BulkSerializerMixin
from ..models.mastery import Mastery


class MasterySerializer(BulkSerializerMixin,serializers.ModelSerializer):



    class Meta:
        model=Mastery
        fields=('id','tank','tier','points','fromSubmission','manager','pointsinfo')
        list_serializer_class = BulkListSerializer




