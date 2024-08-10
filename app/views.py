from django.db.models import Count
from django.shortcuts import render,redirect
from django.http import HttpResponse,JsonResponse
from django.views import View
from . models import Product ,Customer,Cart,OrderPlaced,Wishlist
from . forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    totalitem = 0 
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,"app/home.html",locals())
    # return HttpResponse("WellCome to Arka Jani University")

def about(request):
    totalitem = 0 
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,"app/about.html",locals())


def contact(request):
    totalitem = 0 
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,"app/contact.html",locals())


    
    
class CategoryView(View):
    def get(self,request,val):
        totalitem = 0 
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('title').annotate(total=Count('title'))
        return render(request,"app/category.html",locals())

class CategoryTitle(View):
    def get(self,request,val):
        totalitem = 0 
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        product = Product.objects.filter(title=val)
        title=Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())

   
class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk=pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem = 0 
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,"app/productDetail.html",locals()) 
    
class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        totalitem = 0 
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/customerRegistration.html',locals())
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Register Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'app/customerRegistration.html',locals())
    
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        totalitem = 0 
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/profile.html',locals())
    def post(self,request):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            user = request.user
            name = form.cleaned_data['name']
            locality = form.cleaned_data['locality']
            city = form.cleaned_data['city']
            mobile = form.cleaned_data['mobile']
            state = form.cleaned_data['state']
            zipcode = form.cleaned_data['zipcode']
            
            reg = Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            reg.save()
            messages.success(request,"Congratulations! User Register Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'app/profile.html',locals())
    
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0 
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'app/address.html',locals())
    
class updateView(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0 
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        return render(request,'app/updateAddress.html',locals())
    def post(self,request,pk):
        form = CustomerProfileForm(request.POST)
        if form.is_valid():
            add=Customer.objects.get(pk=pk)
            add.name = form.cleaned_data['name']
            add.locality = form.cleaned_data['locality']
            add.city = form.cleaned_data['city']
            add.mobile = form.cleaned_data['mobile']
            add.state = form.cleaned_data['state']
            add.zipcode = form.cleaned_data['zipcode']
            
            # reg = Customer(user=user,name=name,locality=locality,mobile=mobile,city=city,state=state,zipcode=zipcode)
            add.save()
            messages.success(request,"Congratulations! User Register Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")
    
def add_to_cart(request):
    user=request.user
    prod_id=request.GET.get('prod_id')
    product=Product.objects.get(id=prod_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')

def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    totalitem = 0 
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    return render(request,'app/addtocart.html',locals())

class Checkout(View):
    def get(self,request):
        totalitem = 0 
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount +40    
        return render(request,'app/checkout.html',locals())

def payment_done(request):
    pass    
    
    
def orders(request):
    totalitem = 0 
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
    order_placed=OrderPlaced.objects.filter(user=request.user)    
    return render(request,'app/order.html',locals())
    
        
# def plus_cart(request):
#     if request.method == 'GET':
#         prod_id = request.GET['prod_id']
#         c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
#         c.quantity += 1
#         c.save()
#         user = request.user
#         cart = Cart.objects.filter(user=user)
#         amount=0
#         for p in cart:
#             value = p.quantity * p.product.discounted_price
#             amount = amount + value
#         totalamount = amount + 40
#         data={
#             'quantity':c.quantity,
#             'amount':amount,
#             'totalamount':totalamount
#         }   
#         return JsonResponse(data)      

@login_required
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        
        try:
            # Fetch the product object
            product = Product.objects.get(id=prod_id)
            
            # Fetch all cart items for the product and user
            cart_items = Cart.objects.filter(Q(product=product) & Q(user=request.user))
            
            if cart_items.exists():
                # Update the first cart item found
                c = cart_items.first()
                c.quantity += 1
                c.save()

                # Calculate the cart total
                user = request.user
                cart = Cart.objects.filter(user=user)
                amount = sum(p.quantity * p.product.discounted_price for p in cart)
                totalamount = amount + 40  # Shipping charges can be dynamic or configurable

                data = {
                    'quantity': c.quantity,
                    'amount': amount,
                    'totalamount': totalamount
                }
                return JsonResponse(data)
            else:
                return JsonResponse({'error': 'Cart item does not exist'}, status=404)
        
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product does not exist'}, status=404)

@login_required
def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        
        try:
            # Fetch the product object
            product = Product.objects.get(id=prod_id)
            
            # Fetch all cart items for the product and user
            cart_items = Cart.objects.filter(Q(product=product) & Q(user=request.user))
            
            if cart_items.exists():
                # Update the first cart item found
                c = cart_items.first()
                c.quantity -= 1
                c.save()

                # Calculate the cart total
                user = request.user
                cart = Cart.objects.filter(user=user)
                amount = sum(p.quantity * p.product.discounted_price for p in cart)
                totalamount = amount + 40  # Shipping charges can be dynamic or configurable

                data = {
                    'quantity': c.quantity,
                    'amount': amount,
                    'totalamount': totalamount
                }
                return JsonResponse(data)
            else:
                return JsonResponse({'error': 'Cart item does not exist'}, status=404)
        
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product does not exist'}, status=404)
    
@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        
        try:
            # Fetch the product object
            product = Product.objects.get(id=prod_id)
            
            # Fetch all cart items for the product and user
            cart_items = Cart.objects.filter(Q(product=product) & Q(user=request.user))
            
            if cart_items.exists():
                # Update the first cart item found
                c = cart_items.first()
                c.delete()
                c.save()

                # Calculate the cart total
                user = request.user
                cart = Cart.objects.filter(user=user)
                amount = sum(p.quantity * p.product.discounted_price for p in cart)
                totalamount = amount + 40  # Shipping charges can be dynamic or configurable

                data = {
                    'quantity': c.quantity,
                    'amount': amount,
                    'totalamount': totalamount
                }
                return JsonResponse(data)
            else:
                return JsonResponse({'error': 'Cart item does not exist'}, status=404)
        
        except Product.DoesNotExist:
            return JsonResponse({'error': 'Product does not exist'}, status=404)

def plus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user =request.user
        Wishlist(user,product=product).save()
        data={
            'message':'Wishlist Added Successfully'
        }
        return JsonResponse(data)

def minus_wishlist(request):
    if request.method == 'GET':
        prod_id=request.GET['prod_id']
        product=Product.objects.get(id=prod_id)
        user =request.user
        Wishlist(user,product=product).delete()
        data={
            'message':'Wishlist Added Successfully'
        }
        return JsonResponse(data)

 
