from django.urls import path
from . import views

app_name = "ebookshop"

urlpatterns = [
    path('',views.home, name ='home'),
    path('cart/',views.cart,name='cart'),
    path('update_item/',views.updateItem,name='update_item'),
    path('process_order/',views.processOrder,name='process_order'),
    path('checkout/',views.checkout,name='checkout'),
    path('product/',views.product,name ='product' )


]