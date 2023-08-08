from django.contrib import admin
from django.urls import path
from .views import create_contact, ContactList,delete_contact

urlpatterns = [
    path('create-contact/', create_contact, name='create-contact'),
    path("contacts/", ContactList.as_view(), name='contact-list'),
    path('delete-contact/<int:pk>/', delete_contact, name='delete-contact'),

]