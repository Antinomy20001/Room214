import functools
from rest_framework import status
from rest_framework.response import Response
import datetime
import pytz

TIME_OUTPUT_FORMAT = '%Y-%m-%d %H:%M:%S'

def validate_serializer(serializer):
    """
    如果符合序列化要求，序列化之后的数据放在request.serializer.data
    否则直接返回序列化失败
    @validate_serializer(TestSerializer)
    def post(self, request):
        return self.success(request.data)
    """

    def validate(view_method):
        @functools.wraps(view_method)
        def handle(*args, **kwargs):
            self = args[0]
            request = args[1]
            s = serializer(data=request.data)
            if s.is_valid():
                request.serializer = s
                return view_method(*args, **kwargs)
            else:
                return Response(s.errors, status=status.HTTP_400_BAD_REQUEST)

        return handle

    return validate

def convert_cn_tz(date):
    UTC = pytz.timezone('UTC')
    CN_TZ = pytz.timezone(pytz.country_timezones('cn')[0])
    return date.astimezone(CN_TZ)

def convert_utc(date):
    UTC = pytz.timezone('UTC')
    CN_TZ = pytz.timezone(pytz.country_timezones('cn')[0])
    return date.astimezone(UTC)