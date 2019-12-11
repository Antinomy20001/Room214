from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from core.serializers import PersonSerializer, FaceSerializer, FaceListSerializer
from core.models import Person, Face
from django.conf import settings
from utils.utils import validate_serializer
import json

class PersonAPI(APIView):
    # def get(self, request):
    #     label = request.GET.get('label',None)
    #     if label is None:
    #         return Response({"code": status.Http_404_NOT_FOUND}
    #     # try:
    #     #     person = None
    #     return 
    @validate_serializer(PersonSerializer)
    def post(self, request):
        serializer = request.serializer
        data = serializer.validated_data
        if data['token'] != settings.ACCESS_TOKEN:
            return Response({'code': status.HTTP_406_NOT_ACCEPTABLE,
                             'detail': 'ACCESS_TOKEN not acceptable'},
                             status=status.HTTP_406_NOT_ACCEPTABLE)
        try:
            person = serializer.create(data)
            person.save()
            return Response({
                "code": status.HTTP_201_CREATED,
                "label": person.pk
            }, status=status.HTTP_201_CREATED)
        except:
            return Response({
                "code":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)


class FaceListAPI(APIView):
    @validate_serializer(FaceListSerializer)
    def post(self, request):
        serializer = request.serializer
        data = serializer.validated_data
        if data['token'] != settings.ACCESS_TOKEN:
            return Response({'code': status.HTTP_406_NOT_ACCEPTABLE,
                             'detail': 'ACCESS_TOKEN not acceptable'},
                             status=status.HTTP_406_NOT_ACCEPTABLE)
        room = data.get('room', '214')
        queryset = Face.objects.filter(room__exact=room)
        data = [{'label':face.person.pk, 'room': face.room, 'person': face.person.to_json() } for face in queryset]
        return Response({
            "code": status.HTTP_200_OK,
            'results': data
        }, status=status.HTTP_200_OK)

class FaceAPI(APIView):
    @validate_serializer(FaceSerializer)
    def post(self, request):
        serializer = request.serializer
        data = serializer.validated_data
        if data['token'] != settings.ACCESS_TOKEN:
            return Response({'code': status.HTTP_406_NOT_ACCEPTABLE,
                             'detail': 'ACCESS_TOKEN not acceptable'},
                             status=status.HTTP_406_NOT_ACCEPTABLE)
        try:
            face = serializer.create(data)
            face.save()
            return Response({
                "code": status.HTTP_201_CREATED,
            }, status=status.HTTP_201_CREATED)
        except:
            return Response({
                "code":status.HTTP_400_BAD_REQUEST
            },status=status.HTTP_400_BAD_REQUEST)
