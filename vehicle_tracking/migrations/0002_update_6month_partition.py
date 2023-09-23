# Generated by Django 4.2.3 on 2023-08-08 09:19

from django.db import migrations

from core.models import set_partition_every_6_month

update_6month_partition = set_partition_every_6_month(model_name="Vehicle",start_year=2023,end_year=2033) 
update_6month_partition +=set_partition_every_6_month(model_name="VehicleImage",start_year=2023,end_year=2033) 
update_6month_partition +=set_partition_every_6_month(model_name="Container",start_year=2023,end_year=2033) 
update_6month_partition +=set_partition_every_6_month(model_name="ContainersDetail",start_year=2023,end_year=2033) 
update_6month_partition +=set_partition_every_6_month(model_name="ContainerImage",start_year=2023,end_year=2033) 
update_6month_partition +=set_partition_every_6_month(model_name="ContainerImdg",start_year=2023,end_year=2033) 
update_6month_partition +=set_partition_every_6_month(model_name="ContainerSeal",start_year=2023,end_year=2033) 



class Migration(migrations.Migration):

    dependencies = [
        ("vehicle_tracking", "0001_initial"),
    ]

    operations = update_6month_partition