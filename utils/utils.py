import functools
from rest_framework import status
from rest_framework.response import Response

import pandas as pd
from io import BytesIO
from django.http.response import FileResponse

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