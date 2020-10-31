from django.urls import path, include 

urlpatterns = [
  path('api/', include('sw_cart.api.urls')),
]
