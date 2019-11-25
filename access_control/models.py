from django.db import models
from core.models import Person, Face
import json

class AccessRecord(models.Model):
    timestamp = models.DateTimeField(null=False)
    label = models.ForeignKey(Person, on_delete=models.CASCADE)
    distance = models.FloatField(null=False)
    location = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'time={self.timestamp},label={self.label},distance={self.distance},location={self.location}'

    def to_json(self):
        result = {
            'timestamp':int(self.timestamp.timestamp()),
            'label': self.label.pk,
            'distance': self.distance,
            'location': self.location
        }
        return json.loads(json.dumps(result))

    class Meta:
        db_table = 'AccessRecord'