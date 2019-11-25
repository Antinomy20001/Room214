from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from access_control.serializers import AccessRecordSerializer, AccessRecordListSerializer
from access_control.models import AccessRecord
from core.models import Person
from django.conf import settings
from utils.utils import validate_serializer
import json

class AccessRecordAPI(APIView):
    @validate_serializer(AccessRecordSerializer)
    def post(self, request):
        serializer = request.serializer
        data = serializer.validated_data
        if data['token'] != settings.ACCESS_TOKEN:
            return Response({'code': status.HTTP_406_NOT_ACCEPTABLE,
                             'detail': 'ACCESS_TOKEN not acceptable'},
                             status=status.HTTP_406_NOT_ACCEPTABLE)
        try:
            person = Person.objects.get(pk=data['label'])
        except:
            person = None
        if person is None:
            return Response({
            "code":status.HTTP_200_OK,
            },status=status.HTTP_200_OK)

        obj, created = serializer.create(data)
        return Response({
            "code":status.HTTP_201_CREATED,
        },
        status=status.HTTP_201_CREATED)

class AccessRecordListAPI(APIView):
    @validate_serializer(AccessRecordListSerializer)
    def post(self, request):
        serializer = request.serializer
        data = serializer.validated_data
        if data['token'] != settings.ACCESS_TOKEN:
            return Response({'code': status.HTTP_406_NOT_ACCEPTABLE,
                             'detail': 'ACCESS_TOKEN not acceptable'},
                             status=status.HTTP_406_NOT_ACCEPTABLE)
        try:
            queryset = AccessRecord.objects.filter(
                timestamp__gt=data['date_ranges'].lower,
                timestamp__lt=data['date_ranges'].upper,
                location__in=data.get('location_list',['214',]),
                labels__in=data['labels'],
                distance__gt=data['distance_ranges'].lower,
                distance__lt=data['distance_ranges'].upper,
            )
            queryset = [i.to_json() for i in queryset]
            result = {
                "code":status.HTTP_200_OK,
                "result": queryset,
            }
            return Response(result,status=status.HTTP_200_OK)
        except:
            return Response({
                "code":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)