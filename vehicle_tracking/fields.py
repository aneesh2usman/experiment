from django.db import models
import base64
from django.core.files.base import ContentFile

class Base64ImageField(models.ImageField):
    def from_db_value(self, value, expression, connection):
        if not value:
            return value
        return self.to_python(value)

    def to_python(self, value):
        if not value:
            return value

        if isinstance(value, str):
            return value

        return base64.b64encode(value.read())

    def get_prep_value(self, value):
        if not value:
            return value

        if isinstance(value, str):
            return value

        image_data = base64.b64decode(str(value))
        return ContentFile(image_data, name="image.jpg")
