

# Create your models here.
from django.db.models.sql.where import WhereNode, AND
from django.db import models
from psqlextra.types import PostgresPartitioningMethod
from psqlextra.models import PostgresPartitionedModel
from psqlextra.backend.migrations.operations import PostgresAddRangePartition
from core.fields import CustomCompositeForeignKey, CustomCompositeOneToOneField
from compositefk.fields import CompositeOneToOneField

import datetime
from core.config import CamAngleOption, ContainerPosition, ContainerSizeOption, GateEnterOption, VehicleImageTypeOption, VehicleTypeOption
from django.utils import timezone
from django.conf import settings

from vehicle_tracking.fields import Base64FileField

class Vehicle(PostgresPartitionedModel):
    vehicle_identifier = models.CharField(max_length=100,null=True, blank=True) #API ref truck_id :"abcd1289fc"
    vehicle_no = models.CharField(max_length=100,null=True, blank=True) #eg:KL09G6666
    vehicle_type = models.IntegerField(
                                       default=VehicleTypeOption.TRUCK, 
                                       choices=VehicleTypeOption.choices)
    
    in_time = models.DateTimeField(null=True, blank=True)
    out_time = models.DateTimeField(null=True, blank=True)
    gate_enter = models.SmallIntegerField(
                                       default=GateEnterOption.UNKNOWN, 
                                       choices=GateEnterOption.choices)
    gate_no =  models.CharField(max_length=100,null=True, blank=True) #eg:G1 T1, G1 T2
    anpr_status = models.BooleanField(default=0)
    date_range = models.DateField("Date", default=datetime.date.today)
    extra_data = models.JSONField(null=True, blank=True)
    created	= models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)

    class PartitioningMeta:
        
        method = PostgresPartitioningMethod.RANGE
        key = ["date_range"]
    
    class Meta:
		
        indexes = [
            models.Index(fields=['vehicle_identifier']),
            models.Index(fields=['vehicle_identifier','date_range',"gate_enter","created"]),

        ]

class VehicleImage(PostgresPartitionedModel):
    name  = models.CharField(max_length=100,null=True, blank=True) #eg: Truck image
    vehicle_identifier	= models.CharField(max_length=100,null=True, blank=True)
    date_range = models.DateField("Date", default=datetime.date.today)
    if settings.DISABLE_COMPOSITEFOREIGNKEY:

        vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE,null=True, blank=True)
    else:
        vehicle_id = models.IntegerField()
        vehicle = CustomCompositeForeignKey(Vehicle, on_delete=models.CASCADE, 
        null=True, blank=True,
        related_name='image_parent_vehicle', to_fields={
            "id": "vehicle_id",
            "date_range": "date_range"
        })
    cam_angle = models.SmallIntegerField(
                                       default=CamAngleOption.UNKNOWN, 
                                       choices=CamAngleOption.choices)
    image	= Base64FileField(upload_to='vehicle_images/',null=True, blank=True)
    image_type	= models.SmallIntegerField(
                                       default=VehicleImageTypeOption.UNKNOWN, 
                                       choices=VehicleImageTypeOption.choices)
    extra_data = models.JSONField(null=True, blank=True)
    default_image	= models.BooleanField(default=0)
    
    created	= models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)

    class PartitioningMeta:
        
        method = PostgresPartitioningMethod.RANGE
        key = ["date_range"]
    
    class Meta:
		
        indexes = [
            models.Index(fields=['vehicle_identifier']),
            models.Index(fields=['vehicle_identifier','date_range',"cam_angle","created"]),

        ]

class Container(PostgresPartitionedModel):
    vehicle_identifier	= models.CharField(max_length=100,null=True, blank=True) #API ref truck_id :"abcd1289fc"
    date_range = models.DateField("Date", default=datetime.date.today)
    if settings.DISABLE_COMPOSITEFOREIGNKEY:

        vehicle = models.ForeignKey(Vehicle, on_delete=models.CASCADE,null=True, blank=True)
    else:
        vehicle_id = models.IntegerField(null=True, blank=True)
        vehicle = CustomCompositeForeignKey(Vehicle, on_delete=models.CASCADE, 
            related_name='container_parent_vehicle', 
            null=True, blank=True,
            to_fields={
            "id": "vehicle_id",
            "date_range": "date_range"
        })
    iso_code = models.CharField(max_length=50,null=True, blank=True)
    container_code	= models.CharField(max_length=100,null=True, blank=True) #eg. TGBU1234567
    container_type	= models.CharField(max_length=100,null=True, blank=True) #eg. GENERAL PURPOSE HIGH CUBE
    container_position = models.IntegerField(default=ContainerPosition.UNKNOWN)
    valid_container  = models.BooleanField(default=0)
    capture_date	= models.DateTimeField(default=timezone.now ,null=True, blank=True)
    
    created	= models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)
    class PartitioningMeta:
        
        method = PostgresPartitioningMethod.RANGE
        key = ["date_range"]
    
    class Meta:
        # unique_together = [
        #     ("vehicle_id", "date_range"),
        # ]
        indexes = [
            models.Index(fields=['vehicle_identifier']),
            models.Index(fields=['container_code']),
            models.Index(fields=['vehicle_identifier','container_code']),
            models.Index(fields=['container_code','date_range',"created"]),

        ]

class ContainersDetail(PostgresPartitionedModel):
    date_range = models.DateField("Date", default=datetime.date.today)
    if settings.DISABLE_COMPOSITEFOREIGNKEY:

        container = models.OneToOneField(Container, on_delete=models.CASCADE,null=True, blank=True)
    else:
        container_id = models.IntegerField(null=True, blank=True)
        container = CustomCompositeOneToOneField(Container, on_delete=models.CASCADE, 
        null=True, blank=True,
        related_name='container', 
        to_fields={
            
            "id": "container_id",
            "date_range": "date_range"
        })
    container_code	= models.CharField(max_length=100,null=True, blank=True) #eg. TGBU1234567

    container_owner	= models.CharField(max_length=500,null=True, blank=True) #eg.TRITON Containers, Belgium

    container_size = models.IntegerField(default=ContainerSizeOption.UNKNOWN)

    imdg_present = models.BooleanField(default=0)
    seal_present = models.BooleanField(default=0)
    
    extra_data = models.JSONField(null=True, blank=True)

    class PartitioningMeta:
        
        method = PostgresPartitioningMethod.RANGE
        key = ["date_range"]
    

    class Meta:
        indexes = [
            models.Index(fields=['container_owner']),
            models.Index(fields=['container_code']),
            models.Index(fields=['container_code','date_range']),

        ]

    

class ContainerImage(PostgresPartitionedModel):
    name  = models.CharField(max_length=100,null=True, blank=True) #eg: container image
    vehicle_identifier	= models.CharField(max_length=100,null=True, blank=True)
    date_range = models.DateField("Date", default=datetime.date.today)
    if settings.DISABLE_COMPOSITEFOREIGNKEY:

        container = models.ForeignKey(Container, on_delete=models.CASCADE,null=True, blank=True)
    else:
        container_id = models.IntegerField(null=True, blank=True)
        container = CustomCompositeForeignKey(Container, on_delete=models.CASCADE, 
            null=True, blank=True,             
            related_name='image_parent_container', 
            to_fields={
            "id": "container_id",
            "date_range": "date_range"
        })
    container_code	= models.CharField(max_length=100,null=True, blank=True) #eg. TGBU1234567
    cam_angle = models.SmallIntegerField(
                                       default=CamAngleOption.UNKNOWN, 
                                       choices=CamAngleOption.choices)
    image	= Base64FileField(upload_to='container_images/',null=True, blank=True)
    image_type	= models.SmallIntegerField(
                                       default=VehicleImageTypeOption.UNKNOWN, 
                                       choices=VehicleImageTypeOption.choices)
    extra_data = models.JSONField(null=True, blank=True)
    default_image	= models.BooleanField(default=0)
    created	= models.DateTimeField(default=timezone.now)
    modified = models.DateTimeField(default=timezone.now)

    class PartitioningMeta:
        
        method = PostgresPartitioningMethod.RANGE
        key = ["date_range"]
    
    class Meta:
		
        indexes = [
            models.Index(fields=['container_code']),
            models.Index(fields=['container_code','date_range']),
            models.Index(fields=['container_code','date_range',"cam_angle","created"]),

        ]

class ContainerImdg(PostgresPartitionedModel):
    label = models.CharField(max_length=100,null=True, blank=True) #eg. class 3
    date_range = models.DateField("Date", default=datetime.date.today)
    if settings.DISABLE_COMPOSITEFOREIGNKEY:

        container = models.ForeignKey(Container, on_delete=models.CASCADE,null=True, blank=True)
    else:
        container_id = models.IntegerField(null=True, blank=True)
        container = CustomCompositeForeignKey(Container, on_delete=models.CASCADE, 
            null=True, blank=True,             
            related_name='imgd_parent_container', 
            to_fields={
            "id": "container_id",
            "date_range": "date_range"
        })
    container_code	= models.CharField(max_length=100,null=True, blank=True) #eg. TGBU1234567

    

    class PartitioningMeta:
        
        method = PostgresPartitioningMethod.RANGE
        key = ["date_range"]
    
    class Meta:
		
        indexes = [
            models.Index(fields=['container_code']),
            models.Index(fields=['container_code','date_range']),

        ]

class ContainerSeal(PostgresPartitionedModel):
    label = models.CharField(max_length=100,null=True, blank=True) #eg. class 3
    date_range = models.DateField("Date", default=datetime.date.today)
    if settings.DISABLE_COMPOSITEFOREIGNKEY:

        container = models.ForeignKey(Container, on_delete=models.CASCADE,null=True, blank=True)
    else:
        container_id = models.IntegerField(null=True, blank=True)
        container = CustomCompositeForeignKey(Container, on_delete=models.CASCADE, 
            null=True, blank=True,             
            related_name='seal_parent_container', 
            to_fields={
            "id": "container_id",
            "date_range": "date_range"
        })
    container_code	= models.CharField(max_length=100,null=True, blank=True) #eg. TGBU1234567

    

    class PartitioningMeta:
        
        method = PostgresPartitioningMethod.RANGE
        key = ["date_range"]
    
    class Meta:
		
        indexes = [
            models.Index(fields=['container_code']),
            models.Index(fields=['container_code','date_range']),

        ]