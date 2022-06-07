
from email.policy import default
from unicodedata import category
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.forms import BooleanField
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.
"""class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)

@receiver(post_save, sender=User)
def update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    instance.profile.save()"""


	
class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
    @property
    def get_products(self):
        return Products.objects.filter(category__name=self.name)


class Author(models.Model):
    name = models.CharField(max_length=100)
    biodata = models.TextField(max_length=1000, verbose_name='author_bio', blank=True, null=True)

    def __str__(self):
        return self.name

     		


class Products(models.Model):
    name = models.CharField(max_length=250, blank=False,null=False)
    category = models.ForeignKey(Category,null=True,on_delete=models.SET_NULL, related_name='category')
    digital = models.BooleanField(default=False,null=True, blank=True)
    author = models.ForeignKey(Author,null=True,on_delete=models.SET_NULL, related_name='author' )
    image = models.ImageField(upload_to='products',blank = True, null=True)
    edition = models.CharField(max_length=50,blank=True,null=True) 
    description = models.TextField(max_length=500,verbose_name='summary')
    price = models.DecimalField(max_digits=7,decimal_places=2,validators=[MinValueValidator(0.01)])
    discount  = models.IntegerField(blank = True, null = True)
    old_price = models.FloatField(default=0.00, blank=True, null= True)
    stock = models.IntegerField(blank=True, null= True)
    tag = models.CharField(max_length=20, blank= True,null = True)

    def __str__(self):
        return self.name

	


class Customer(models.Model):
	user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
	name = models.CharField(max_length=200, null=True)
	email = models.EmailField(max_length=254)

	def __str__(self):
		return self.name




class Order(models.Model):
	order_status = (
		
		('1','package being prepared'),
		('2','shipping'),
		('3','shipped'),
		('4','delivered'),
		('5','processing'),

	)
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
	date_ordered = models.DateTimeField(auto_now_add=True)
	complete = models.BooleanField(default=False)
	transaction_id = models.CharField(max_length=100, null=True)
	status = models.CharField(max_length=50, choices=order_status, default='5')


	def __str__(self):
		return str(self.id)

	@property
	def shipping(self):
		shipping = False 
	
		orderitems = self.orderitem_set.all()
		for i in orderitems:
			if i.product.digital == False:
				shipping = True 
			
		return shipping


	@property
	def get_cart_total(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.get_total for item in orderitems])
		return total

	@property
	def get_cart_items(self):
		orderitems = self.orderitem_set.all()
		total = sum([item.quantity for item in orderitems])
		return total


class OrderItem(models.Model):
	product = models.ForeignKey(Products, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	quantity = models.IntegerField(default=0, null=True, blank=True)
	date_added = models.DateTimeField(auto_now_add=True)
	def __str__(self):
		return str(self.order)
	

	@property
	def get_total(self):
		total = self.product.price * self.quantity
		return total


class ShippingAddress(models.Model):
	customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
	order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
	mobile = models.CharField(max_length=50, null = False)
	address = models.CharField(max_length=200, null=False)
	city = models.CharField(max_length=200, null=False)
	state = models.CharField(max_length=200, null=False)
	zipcode = models.CharField(max_length=200, null=False)
	date_added = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return str(self.address) 





