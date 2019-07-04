from django.urls import path, include
from django.conf.urls import url
from . import views

urlpatterns = [
    path('', views.base_view, name='base'),
    path('category/<slug:category_slug>/', views.category_view, name='category_detail'),
    path('cart', views.cart, name='cart'),
    path('add_to_cart', views.add_to_cart, name='add_to_cart'),
    path('remove_from_cart', views.remove_from_cart, name='remove_from_cart'),
    path('payment/<slug:beat_slug>/', views.payment, name='payment')
]
