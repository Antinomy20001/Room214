from rest_framework import serializers
from rest_framework.fields import Field
from access_control.models import AccessRecord
from drf_extra_fields.fields import DateTimeRangeField, FloatRangeField
from core.models import Person
from array import array
import struct
import datetime
from pytz import timezone
from django.conf import settings

class TimestampField(Field):

    def to_representation(self, value):
        return int(value.timestamp())

    def to_internal_value(self, data):
        timestamp = int(data)
        no_tz = datetime.datetime.fromtimestamp(timestamp)
        return no_tz.astimezone(timezone(settings.TIME_ZONE))

class AccessRecordSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    timestamp = TimestampField(required=True)
    label = serializers.IntegerField(required=True)
    distance = serializers.FloatField(required=True)
    location = serializers.CharField(max_length=200,required=False)

    def create(self, validated_data):
        interval = validated_data['timestamp'] - settings.INSERT_INTERVAL
        record = AccessRecord.objects.filter(timestamp__gte=interval, label_id__exact=validated_data['label'])
        created = False
        if record.count() > 0:
            record = record.first()
            record.distance = validated_data['distance']
            record.location = validated_data.get('location','214')
            record.save()
        else:
            # label must exist
            record = AccessRecord.objects.create(label_id=validated_data['label'],
                                        timestamp=validated_data['timestamp'],
                                        distance=validated_data['distance'],
                                        location=validated_data.get('location','214'))
            created = True
        return record, created

class AccessRecordBulkSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    records = serializers.ListField(child=AccessRecordSerializer(), required=True)
    
class AccessRecordListSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    date_ranges = DateTimeRangeField(required=True)
    location_list = serializers.ListField(child=serializers.CharField(max_length=200),required=False)
    labels = serializers.ListField(required=False,child=serializers.IntegerField(min_value=0))
    distance_ranges = FloatRangeField(required=False)