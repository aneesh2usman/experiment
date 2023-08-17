from django.urls import path
from .views import ApiImageView, ApiValidationView

urlpatterns = [
    path('api-validation/', ApiValidationView.as_view(), name='api-validation'),
    path('image/', ApiImageView.as_view(), name='api-image'),
]