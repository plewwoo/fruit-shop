# urls.py

from django.urls import path, include
from .views import *

urlpatterns = [
    path('', Home, name='home-page'),
    path('profile/', profile, name='profile-page'),
    path('apple/', Apple, name='apple-page'),
    path('addproduct/', AddProduct, name='addproduct-page'),
    path('product/', Product, name='product-page'),
    path('cart/', MyCart, name='cart-page'),
    path('cart/edit/', EditMycart, name='editcart-page'),
    path('register/', Register, name='register-page'),
    path('addtocart/<int:productId>/', AddToCart, name='addtocart-page'),
    path('checkout/', Checkout, name='checkout-page'),
    path('orderlist/', MyOrderList, name='orderlist-page'),
    path('allorderlist/', AllOrderList, name='allorderlist-page'),
    path('uploadslip/<str:orderId>/', UploadSlip, name='uploadslip-page'),
    path('updatestatus/<str:orderId>/<str:status>/',
         UpdatePaid, name='updatestatus'),
    path('tracking/<str:orderId>/',
         UpdateTracking, name='updatetracking-page'),
    path('myorder/<str:orderId>/', MyOrder, name='myorder-page'),
]
