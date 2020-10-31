from django.urls import path, include 

urlpatterns = [
  path('api/', include('box.apps.sw_shop.sw_cart.api.urls')),
]
