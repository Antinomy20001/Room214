from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from access_control.serializers import AccessRecordSerializer, AccessRecordListSerializer
from access_control.models import AccessRecord
from core.models import Person
from django.conf import settings
from utils.utils import validate_serializer, convert_cn_tz, convert_utc
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
            "code":status.HTTP_201_CREATED if created else status.HTTP_200_OK
        },status=status.HTTP_201_CREATED)

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
            query_param = {
                'timestamp__gt':convert_utc(data['date_ranges'].lower),
                'timestamp__lt':convert_utc(data['date_ranges'].upper),
                'location__in':data.get('location_list',['214',])
            }
            labels__in = data.get('labels', None)
            distance_ranges = data.get('distance_ranges', None)
            if labels__in is not None:
                query_param['labels__in'] = labels__in
            if distance_ranges is not None:
                query_param['distance__gt'] = distance_ranges.lower
                query_param['distance__lt'] = distance_ranges.upper

            queryset = AccessRecord.objects.filter(**query_param)
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