

#https://betterprogramming.pub/partitioning-in-django-postgresql-d7ebbe8f9c2b
#https://pganalyze.com/blog/postgresql-partitioning-django

#python manage.py makemigrations --empty orders --name partion_order_and_lineitem
from django.db.models.sql.where import WhereNode, AND
from django.db import models
from psqlextra.types import PostgresPartitioningMethod
from psqlextra.models import PostgresPartitionedModel
from psqlextra.backend.migrations.operations import PostgresAddRangePartition
from compositefk.fields import CompositeForeignKey,LocalFieldValue,RawFieldValue,FunctionBasedFieldValue
from django.utils import translation
import datetime
class Order(PostgresPartitionedModel):
    name = models.TextField()
    year = models.CharField(max_length=255)
    order_number = models.CharField(max_length=255)
    created = models.DateTimeField(auto_now_add=True)
    date_range = models.DateField("Date", default=datetime.date.today)

    class PartitioningMeta:
        
        method = PostgresPartitioningMethod.RANGE
        key = ["date_range"]
class CustomCompositeForeignKey(CompositeForeignKey):
    def get_extra_restriction(self, where_class, alias, related_alias=None):
        constraint = WhereNode(connector=AND)
        for remote, local in self._raw_fields.items():
            if remote not in ["created"]:
                lookup = local.get_lookup(self, self.related_model._meta.get_field(remote), alias)
                if lookup:
                    constraint.add(lookup, AND)
        if constraint.children:
            return constraint
        else:
            return None

class LineItem(PostgresPartitionedModel):
    name = models.TextField()
    year = models.CharField(max_length=255)
    order_id = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    date_range = models.DateField("Date", default=datetime.date.today)
    order = CustomCompositeForeignKey(Order, on_delete=models.CASCADE, related_name='order', to_fields={
        "id": "order_id",
        "date_range": "date_range"
    })
    class PartitioningMeta:
        method = PostgresPartitioningMethod.RANGE
        key = ["date_range"]

class LineItemImage(PostgresPartitionedModel):
    name = models.TextField()
    lineitem = models.OneToOneField(
        LineItem,
        on_delete=models.CASCADE,
        primary_key=True,
    )
    date_range = models.DateField("Date", default=datetime.date.today)
    class PartitioningMeta:
        method = PostgresPartitioningMethod.RANGE
        key = ["date_range"]


class Product(PostgresPartitionedModel):
    name = models.TextField()
    lineitem_id = models.IntegerField()
    created = models.DateTimeField(auto_now_add=True)
    date_range = models.DateField("Date", default=datetime.date.today)
    lineitem = CustomCompositeForeignKey(LineItem, on_delete=models.CASCADE, related_name='lineItem', to_fields={
        "id": "lineitem_id",
        "date_range": "date_range"
    })
    class PartitioningMeta:
        method = PostgresPartitioningMethod.RANGE
        key = ["date_range"]


def set_partition_every_6_month(model_name,start_year,end_year):
    partition_list = []
    for year in range(start_year, end_year + 1):
        for month in range(1, 13, 6):
            start_date = datetime.date(year, month, 1)
            end_date = datetime.date(year, month + 5, 30)
            PostgresAddRangePartition(
                model_name=model_name,
                name=f"{model_name}_{start_date}_to_{end_date}",
                from_values=start_date,
                to_values=end_date,
            ),
    return partition_list

# active_translations = CompositeForeignKey(
#     LineItem,
#     on_delete=models.CASCADE,
#     to_fields={
#         'master_id': 'id',
#         'language_code': FunctionBasedFieldValue(translation.get_language)
#     })


# active_translations.contribute_to_class(Order, 'active_translations')

# class Order(models.Model):
#     name = models.TextField()
#     # created = models.DateTimeField(auto_now_add=True)
#     created = models.DateTimeField(auto_now_add=True)

#     # class PartitioningMeta:
#     #     method = PostgresPartitioningMethod.RANGE
#     #     key = ["created"]

# class LineItem(models.Model):
#     name = models.TextField()
#     order = models.ForeignKey(Order, on_delete = models.CASCADE)
#     # created = models.DateTimeField(auto_now_add=True)
#     created = models.DateTimeField(auto_now_add=True)
#     # class PartitioningMeta:
#     #     method = PostgresPartitioningMethod.RANGE
#     #     key = ["created"]

# import datetime

# def get_dates(start_year, end_year):
#     dates = []
#     for year in range(start_year, end_year + 1):
#         for month in range(1, 13, 6):
#             start_date = datetime.date(year, month, 1)
#             end_date = datetime.date(year, month + 5, 30)
#             dates.append((start_date, end_date))
#     return dates

# dates = get_dates(2023, 2040)

# for start_date, end_date in dates:
#     print(f"{start_date} - {end_date}")

# def set_range_pratition_every_sixth_month(start_year):
#     dates = get_dates(2023, 2040)

# def partition_database(start_year, end_year):
#     dates = []
#     now = datetime.datetime.now()
#     for year in range(start_year, end_year):
#         for month in range(1, 13):
#             if month % 6 == 0:
#                 start_date = datetime.date(year, month, 1)
#                 end_date = datetime.date(year, month + 5, 31)
#                 dates.append((start_date, end_date))
#     return dates

# dates = partition_database(2023, 2040)

# for start_date, end_date in dates:
#     print(f"{start_date} - {end_date}")



# I ended up putting this at the end of my initial migrations:

# migrations.RunSQL("""
#             ALTER TABLE qc_trials_trial
#                 ADD CONSTRAINT qc_trials_trial_unique_trial_id_kit_id
#                 UNIQUE (id, kit_id);
#             ALTER TABLE qc_trials_componentoverride
#                 ADD CONSTRAINT qc_trials_componentoverride_comp_constraint_trial_id_kit_id
#                 FOREIGN KEY (kit_id, trial_id)
#                 REFERENCES qc_trials_trial(id, kit_id)
#                 DEFERRABLE INITIALLY DEFERRED
# """),


class LineItem2(models.Model):
    name = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    

class Product2(PostgresPartitionedModel):
    name = models.TextField()
    lineItem2 = models.ForeignKey(
        LineItem2, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class Category(models.Model):
    name = models.CharField(max_length=128)
class Book(models.Model):
    name = models.CharField(max_length=128)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)



class Author(models.Model):
    name = models.CharField(max_length=100)
    # Other fields for the author

    def __str__(self):
        return self.name

class Book2(models.Model):
    title = models.CharField(max_length=200)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    # Other fields for the book

    def __str__(self):
        return self.title
