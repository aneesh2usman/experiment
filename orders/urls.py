from django.urls import path
from .views import LineItemView, OrderView, PersonListView

urlpatterns = [
    path('order-list/', PersonListView.as_view(), name='order-list'),
    path('order/', OrderView.as_view(), name='order'),
    path('lineitem/', LineItemView.as_view(), name='lineitem'),
]