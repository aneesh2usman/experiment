from django.views.generic import ListView
from .models import Author, Category, LineItem, LineItem2, LineItemImage, Order,Product,Book
from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Order
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.forms.models import model_to_dict
class PersonListView(ListView):
    model = Order
    template_name = 'orders_list.html'
    context_object_name = 'orders'


# views.py

from django.db import connection

def get_raw_query_results():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM orders_product")
        results = cursor.fetchall()
    return results


from .models import Order, LineItem

# Decorator to exempt the view from CSRF protection (for simplicity in this example).
# You should handle CSRF protection appropriately in your production code.
csrf_exempt_view = method_decorator(csrf_exempt, name='dispatch')
class OrderView(View):
    @csrf_exempt_view
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, order_id=None):
        if order_id:
            order = get_object_or_404(Order, id=order_id)
            data = {
                'id': order.id,
                'order_number': order.order_number,
                # Add other fields as needed
            }
        else:
            orders = Order.objects.all()
            # a = model_to_dict(orders[0])
            data = list(orders.values())
            # data = [{'id': order.id, 'order_number': order.order_number} for order in orders]

        return JsonResponse(data, safe=False)

    def post(self, request):
        order_data = request.POST
        order = Order.objects.create(order_number=order_data['order_number'])
        # Handle other fields as needed
        return JsonResponse({'id': order.id, 'order_number': order.order_number})

    def put(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order_data = request.POST
        order.order_number = order_data['order_number']
        # Update other fields as needed
        order.save()
        return JsonResponse({'id': order.id, 'order_number': order.order_number})

    def delete(self, request, order_id):
        order = get_object_or_404(Order, id=order_id)
        order.delete()
        return JsonResponse({'message': 'Order deleted successfully'})

class LineItemView(View):
    @csrf_exempt_view
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def get(self, request, lineitem_id=None):
        if lineitem_id:
            lineitem = get_object_or_404(LineItem, id=lineitem_id)
            data = {
                'id': lineitem.id,
                'product_name': lineitem.product_name,
                'quantity': lineitem.quantity,
                # Add other fields as needed
            }
        else:
            lineitems = LineItem.objects.all().select_related("order")
            # # print(lineitems.lineitemimage)
            # # print("**get_raw_query_results***",get_raw_query_results())
            # for lineitem in lineitems:
            #     products = Product.objects.filter(lineitem_id = lineitem.id)
            #     print("******lineitems*****",products)
            #     for product in products:
            #         print(product)
            # product = Product.objects.all().select_related("lineitem")
            # print("***lineitems.order_id.id****",lineitems.query)
            # print(lineitems.query)
            authors = Author.objects.prefetch_related("book2_set").all()
            print(authors.query)
            for author in authors:
                print(author.book2_set.all())
                print(author.book2_set.all().query)
            # LineItemImage.objects.create()
            # image = LineItemImage(name="test2",lineitem=lineitems[0],date_range = lineitems[0].date_range)
            # image.save()
            # lineitems2 = LineItem.objects.all().select_related("order","lineitemimage").values(
            #     "name","order__name","lineitemimage__name"
            # )
            # print(lineitems2)
            data = list(lineitems.values())
            # data = [{'id': lineitem.id, 'product_name': lineitem.product_name, 'quantity': lineitem.quantity} for lineitem in lineitems]

        return JsonResponse(data, safe=False)

    def post(self, request):
        lineitem_data = request.POST
        order = get_object_or_404(Order, id=lineitem_data['order_id'])
        lineitem = LineItem.objects.create(order=order, product_name=lineitem_data['product_name'], quantity=lineitem_data['quantity'])
        # Handle other fields as needed
        return JsonResponse({'id': lineitem.id, 'product_name': lineitem.product_name, 'quantity': lineitem.quantity})

    def put(self, request, lineitem_id):
        lineitem = get_object_or_404(LineItem, id=lineitem_id)
        lineitem_data = request.POST
        lineitem.product_name = lineitem_data['product_name']
        lineitem.quantity = lineitem_data['quantity']
        # Update other fields as needed
        lineitem.save()
        return JsonResponse({'id': lineitem.id, 'product_name': lineitem.product_name, 'quantity': lineitem.quantity})

    def delete(self, request, lineitem_id):
        lineitem = get_object_or_404(LineItem, id=lineitem_id)
        lineitem.delete()
        return JsonResponse({'message': 'Line item deleted successfully'})


