from django.shortcuts import render,get_object_or_404
from django.http import HttpResponse,JsonResponse
import json
import datetime
from . models import *
# Create your views here.
def home(request): 
    product_list = Products.objects.all()
    category_list = Category.objects.all()
    writers_list = Author.objects.values('name')
    if request.user.is_authenticated:
        customer = request.user.customer 
        try:
            order = Order.objects.get(customer = customer,complete = False)
            items = order.orderitem_set.all() 
            cartItems = order.get_cart_items
        except:
            items =[]
            order ={'get_cart_items':0,'get_cart_total':0}
            cartItems = order['get_cart_items']
            

        
        
    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0,'shipping':False }
        cartItems = order['get_cart_items']

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
    if request.user.is_authenticated:
        customer = request.user.customer
        order = Order.objects.get(customer = customer, complete = False) 
        items = order.orderitem_set.all() 
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0,'get_cart_total':0,'shipping':False }
        cartItems = order['get_cart_items']
    return render(request,"category.html",
    {
        'products':product_list,
        'cartItems':cartItems
    })

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all() 
        cartItems = order.get_cart_items

        
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0,'shipping':False}
        cartItems = order['get_cart_items']
    context = {'items':items,'order':order,'cartItems':cartItems}
    return render(request,"cart.html",context)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer = customer,complete = False)
        items = order.orderitem_set.all() 
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_items':0, 'get_cart_total':0,'shipping':False}
        cartItems = order['get_cart_items']
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
    else:
        print('user is not logged in..')
    return JsonResponse('payment completed', safe= False)