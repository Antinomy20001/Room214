from django.db import models
from core.models import Person, Face
import json
from utils.utils import TIME_OUTPUT_FORMAT, convert_cn_tz

class AccessRecord(models.Model):
    timestamp = models.DateTimeField(null=False)
    label = models.ForeignKey(Person, on_delete=models.CASCADE)
    distance = models.FloatField(null=False)
    location = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'time={self.timestamp.strftime(TIME_OUTPUT_FORMAT)},label={self.label_id},distance={self.distance},location={self.location}'

    def to_json(self):
        result = {
            'timestamp':convert_cn_tz(self.timestamp).strftime(TIME_OUTPUT_FORMAT),
            'label': self.label.pk,
            'name': self.label.name,
            'distance': self.distance,
            'location': self.location
        }
        if self.label.student_id is not None:
            result['student_id'] = self.label.student_id
        return json.loads(json.dumps(result))

    class Meta:
        db_table = 'AccessRecord'