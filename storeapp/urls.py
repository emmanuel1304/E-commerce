from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
app_name = 'storeapp'

urlpatterns = [ 
    path('login/',views.login_request, name='login'),
    path('', views.homePage, name='home'),
    path('signup/', views.signup, name='signup'),
    path('logout', views.logout_request, name='logout'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name="checkout"),
    path('order/', views.orderpage, name="order"),
    path('paystack/', views.paystack, name='paystack'),
    path('order_detaile/<int:pk>/', views.order_detaile, name='order_detaile'),
    path('product_detaile/<int:pk>/', views.product_detaile, name='product_detaile'),
    path('cart/add/<int:id>/', views.cart_add, name='cart_add'),
    path('cart/item_clear/<int:id>/', views.item_clear, name='item_clear'),
    path('cart/item_increment/<int:id>/', views.item_increment, name='item_increment'),
    path('cart/item_decrement/<int:id>/', views.item_decrement, name='item_decrement'),
    path('cart/cart_clear/', views.cart_clear, name='cart_clear'),
    path('reviews/', views.reviews, name='reviews'),
    
]