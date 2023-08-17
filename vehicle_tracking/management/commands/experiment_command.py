from django.core.management.base import BaseCommand

from core.models import set_partition_every_6_month

class Command(BaseCommand):
    help = 'My custom command that does something.'

    def handle(self, *args, **kwargs):
        update_6month_partition = set_partition_every_6_month(model_name="Vehicle",start_year=2023,end_year=2033) 
        update_6month_partition +=set_partition_every_6_month(model_name="VehicleImage",start_year=2023,end_year=2033) 
        update_6month_partition +=set_partition_every_6_month(model_name="Container",start_year=2023,end_year=2033) 
        update_6month_partition +=set_partition_every_6_month(model_name="ContainersDetail",start_year=2023,end_year=2033) 
        update_6month_partition +=set_partition_every_6_month(model_name="ContainerImage",start_year=2023,end_year=2033) 
        update_6month_partition +=set_partition_every_6_month(model_name="ContainerImdg",start_year=2023,end_year=2033) 
        update_6month_partition +=set_partition_every_6_month(model_name="ContainerSeal",start_year=2023,end_year=2033) 
        print(update_6month_partition)


