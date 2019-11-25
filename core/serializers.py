from rest_framework import serializers
from core.models import User, Face, Person
from array import array
import struct

class PersonSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    name = serializers.CharField(required=True,max_length=200)
    student_id = serializers.CharField(required=False, min_length=5)
    title = serializers.ChoiceField(choices=['STUDENT','TEACHER'])

    def create(self, validated_data):
        if 'student_id' in validated_data:
            return Person(name=validated_data['name'], title=validated_data['title'], student_id=validated_data['student_id'])
        else:
            return Person(name=validated_data['name'], title=validated_data['title'])
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.title = validated_data.get('title', instance.title)
        instance.save()
        return instance

class FaceSerializer(serializers.Serializer):
    token = serializers.CharField(required=True)
    vector = serializers.ListField(required=True,child=serializers.FloatField(min_value=-255.,max_value=255.),min_length=512,max_length=512)
    label = serializers.IntegerField(required=True)

    def create(self, validated_data):
        return Face(vector=array('f',validated_data['vector']).tobytes(),person=Person.objects.get(pk=validated_data['label']))
    
    def update(self, instance, validated_data):
        instance.vector = array('f',validated_data.get('vector', struct.unpack('f'*512,instance.vector))).tobytes()
        instance.save()
        return instance