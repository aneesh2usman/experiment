import base64
from django.db import models

from htmx_test.crypto import decrypt, encrypt
from vehicle_tracking.fields import  Base64ImageField
from django.core.files.base import ContentFile


class Contact(models.Model):
    name = models.CharField(max_length=200)
    phone_number=models.CharField(max_length=200)
    def __str__(self):
        return self.name
    

class APIKey(models.Model):
    api_key = models.CharField(max_length=500)
    api_secret=models.CharField(max_length=500)
    def __str__(self):
        return self.api_key
    def save(self, *args, **kwargs):
        if self.api_key:
            self.api_key = encrypt(self.api_key)
        if self.api_secret:
            self.api_secret = encrypt(self.api_secret)

        super().save(*args, **kwargs)

    @property
    def _api_key(self):
        return decrypt(self.api_key)
    
    @property
    def _api_secret(self):
        return decrypt(self.api_secret)
    
def create_from_base64(base64_data,file_name="custom_image.jpg"):
    image_data = base64.b64decode(base64_data)
    file_name = "custom_image.jpg"  # You can generate a unique name here
    content_file = ContentFile(image_data, name=file_name)
    return content_file



class SampleImage(models.Model):
    image = models.ImageField(upload_to='images/',null=True, blank=True)
    @classmethod
    def create_from_base64_old(cls, base64_data):
        image_data = base64.b64decode(base64_data)
        file_name = "custom_image.jpg"  # You can generate a unique name here
        content_file = ContentFile(image_data, name=file_name)
        # custom_image = cls(image=content_file)
        cls.image=content_file
        # custom_image.save()
        return cls.image
    
    def create_from_base64(self, base64_data):

        self.image=create_from_base64(base64_data)

