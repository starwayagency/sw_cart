from django.urls import path, include 

urlpatterns = [
  path('api/', include('sw_shop.sw_cart.api.urls')),
]
