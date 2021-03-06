from rest_framework import serializers
from core.models import User, Face, Person
from array import array
import struct

class PersonSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    name = serializers.CharField(required=True,max_length=200)
    student_id = serializers.CharField(required=False, min_length=5)
    title = serializers.ChoiceField(choices=['STUDENT','TEACHER'])
    label = serializers.IntegerField(required=False)

    def create(self, validated_data):
        data = {
            'name': validated_data['name'],
            'title':validated_data['title'],
        }
        label = validated_data.get('label', None)
        student_id = validated_data.get('student_id', None)
        if label is not None:
            data['pk'] = label
        if student_id is not None:
            data['student_id'] = student_id
        return Person(**data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance

class FaceListSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    room = serializers.CharField(required=False)

class FaceSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    vector = serializers.ListField(required=True,child=serializers.FloatField(min_value=-255.,max_value=255.),min_length=512,max_length=512)
    label = serializers.IntegerField(required=True)
    room = serializers.CharField(required=False)
    def create(self, validated_data):
        data = {
            'vector':array('f',validated_data['vector']).tobytes(),
            'person_id':validated_data['label']
        }
        room = validated_data.get('room','214')
        data['room'] = room
        return Face(**data)

    def update(self, instance, validated_data):
        instance.vector = array('f',validated_data.get('vector', struct.unpack('f'*512,instance.vector))).tobytes()
        instance.save()
        return instance