from django.urls import path,re_path
from django.urls import re_path as url
from . import views

app_name = "ebookshop"

urlpatterns = [
    path('',views.home, name ='home'),
    path('cart/',views.cart,name='cart'),
    path('update_item/',views.updateItem,name='update_item'),
    path('process_order/',views.processOrder,name='process_order'),
    path('checkout/',views.checkout,name='checkout'),
    path('product/',views.product,name ='product' ),
    path('category/<str:name>',views.category,name ='category' ),
    url(r'^register/$',views.registerPage, name='register'),
    path('login/',views.loginPage, name='login'),
    path('logout/',views.logoutpage,name='logout' ), 
    url(r'^search/$',views.search, name='search'),
    path('myorder', views.orderlist, name = 'orderlist'),


]