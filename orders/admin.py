from django.contrib import admin

from orders.models import Author, Book2, Category, LineItem,Book, Product
from orders.models import Order

# Register your models here.
admin.site.register(Order)
admin.site.register(LineItem)
admin.site.register(Product)

admin.site.register(Category)


admin.site.register(Book)

admin.site.register(Book2)
admin.site.register(Author)