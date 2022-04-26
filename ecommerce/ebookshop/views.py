from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,JsonResponse
import json
import datetime
from . models import *
from . utils import cookieCart,cartData,guestOrder
# Create your views here.
def home(request): 
    product_list = Products.objects.all()
    category_list = Category.objects.all()
    writers_list = Author.objects.values('name')
    Data = cartData(request)
    cartItems = Data['cartItems']

    return render(request,"home.html",
    {
        'products':product_list,
        'categories':category_list,
        'authors':writers_list,
        #'items':items,
        'cartItems':cartItems
     }
      )

def product(request):
    product_list = Products.objects.all()
    Data = cartData(request)
    cartItems = Data['cartItems']
    return render(request,"category.html",
    {
        'products':product_list,
        'cartItems':cartItems
    })

def cart(request):
    Data = cartData(request)
    items = Data['items']
    order = Data['order']
    cartItems = Data['cartItems']

    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request,"cart.html",context)

def checkout(request):
   
    Data = cartData(request)

    items = Data['items']
    order = Data['order']
    cartItems = Data['cartItems']
    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request,"checkout.html",context)
   


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']
    print('Action:',action)
    print('productId:',productId)
    customer = request.user.customer
    product = Products.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer = customer,complete = False)
    orderItem,created = OrderItem.objects.get_or_create(order = order, product = product)
    if action =='add':
        # by clicking up arrow, increment orderItem by 1
        orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
        # by clicking up arrow, decrement orderItem by 1
        orderItem.quantity = (orderItem.quantity - 1)

    # save quantity of products, for an order
    orderItem.save()

    if orderItem.quantity <= 0:
        # remove the orderItem from cart, when quantity reaches 0, or below it
        orderItem.delete()

    return JsonResponse("item was added", safe=False)

def processOrder(request):
    print('Data:',request.body)
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body) 
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer,complete = False)
        
       
    else:
        customer,order = guestOrder(request,data) 

    total = float(data['form']['total'] )
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save() 
    ShippingAddress.objects.create(
            customer = customer,
            order = order,
            mobile = data['shipping']['mobile'],
            address = data['shipping']['address'],
            city = data['shipping']['city'],
            state = data['shipping']['state'],
            zipcode = data['shipping']['zipcode']
        )
    return JsonResponse('payment completed', safe= False)