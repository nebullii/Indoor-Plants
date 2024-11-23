from django.urls import path
from . import views
from .views import CreateCheckoutSession, PlaceOrderView

app_name = 'cart'

urlpatterns = [
    path('', views.view_cart, name='view_cart'),
    path('add/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove/<int:item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('place-order/', PlaceOrderView.as_view(), name='place-order'),
    
    #path('create-checkout-session/', CreateCheckoutSession.as_view(), name='create-checkout-session'),
]