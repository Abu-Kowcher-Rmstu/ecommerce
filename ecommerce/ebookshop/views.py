from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponse,JsonResponse
import json
import datetime
from . models import *
from . utils import cookieCart,cartData,guestOrder
from django.contrib.auth import login,authenticate,logout 
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib import messages
from . forms import NewUserForm
# Create your views here.
def registerPage(request):
  
    if request.method == 'POST':
        form = NewUserForm(request.POST)
        if form.is_valid():
            user=form.save() 
          
            user.save() 
            name = form.cleaned_data.get('full_name')
            email = user.email
            customer= Customer.objects.create(user=user,name =name,email=email,)
            
            customer.save() 
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            return redirect('ebookshop:home') 
    else:
        form =NewUserForm() 
    
    return render(request,'registration/register.html',{'form':form})


def loginPage(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username= username, password=password)
            if user is not None:
                login(request,user)
                messages.info(request,f"You are now logged in as {username}.")
                
                return redirect("ebookshop:home")
            else:
                messages.error(request,"Invalid username or password.")
        else:
            messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    return render(request,'registration/login.html',{'form':form}) 
                
   
def logoutpage(request): 
    logout(request)
    messages.info(request,"you have successfully logged out.")
    return redirect("ebookshop:home")


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