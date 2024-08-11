from django.db.models import Count
from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse,JsonResponse
from django.views import View
from . models import Product ,Customer,Cart,OrderPlaced,Wishlist
from . forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

# Create your views here.
@login_required
def home(request):
    totalitem = 0 
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/home.html",locals())
    
@login_required
def about(request):
    totalitem = 0 
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/about.html",locals())

@login_required
def contact(request):
    totalitem = 0 
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,"app/contact.html",locals())


    
@method_decorator(login_required,name='dispatch')   
class CategoryView(View):
    def get(self,request,val):
        totalitem = 0 
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(category=val)
        title=Product.objects.filter(category=val).values('title').annotate(total=Count('title'))
        return render(request,"app/category.html",locals())

@method_decorator(login_required,name='dispatch')   
class CategoryTitle(View):
    def get(self,request,val):
        totalitem = 0 
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        product = Product.objects.filter(title=val)
        title=Product.objects.filter(category=product[0].category).values('title')
        return render(request,"app/category.html",locals())

@method_decorator(login_required,name='dispatch')      
class ProductDetail(View):
    def get(self,request,pk):
        product = Product.objects.get(pk = pk)
        wishlist = Wishlist.objects.filter(Q(product=product) & Q(user=request.user))
        totalitem = 0 
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request,"app/productDetail.html",locals()) 

# @method_decorator(login_required,name='dispatch')   
# class ProductDetail(View):
#     def get(self, request, pk):
#         # Retrieve the product, raise 404 if not found
#         product = get_object_or_404(Product, pk=pk)

#         # Initialize variables
#         wishlist = None
#         totalitem = 0 
#         wishitem = 0

#         # Check if the user is authenticated
#         if request.user.is_authenticated:
#             wishlist = Wishlist.objects.filter(product=product, user=request.user)
#             totalitem = Cart.objects.filter(user=request.user).count()
#             wishitem = Wishlist.objects.filter(user=request.user).count()

#         # Create the context dictionary
#         context = {
#             'product': product,
#             'wishlist': wishlist,
#             'totalitem': totalitem,
#             'wishitem': wishitem,
#         }

#         # Render the template with the context
#         return render(request, "app/productDetail.html", locals())

     
class CustomerRegistrationView(View):
    def get(self,request):
        form=CustomerRegistrationForm()
        totalitem = 0 
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        return render(request,'app/customerRegistration.html',locals())
    def post(self,request):
        form=CustomerRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"Congratulations! User Register Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return render(request,'app/customerRegistration.html',locals())

@method_decorator(login_required,name='dispatch')       
class ProfileView(View):
    def get(self,request):
        form = CustomerProfileForm()
        totalitem = 0 
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
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
@login_required    
def address(request):
    add = Customer.objects.filter(user=request.user)
    totalitem = 0 
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/address.html',locals())

@method_decorator(login_required,name='dispatch')       
class updateView(View):
    def get(self,request,pk):
        add=Customer.objects.get(pk=pk)
        form = CustomerProfileForm(instance=add)
        totalitem = 0 
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
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
            
            
            add.save()
            messages.success(request,"Congratulations! User Register Successfully")
        else:
            messages.warning(request,"Invalid Input Data")
        return redirect("address")
@login_required    
def add_to_cart(request):
    user=request.user
    prod_id=request.GET.get('prod_id')
    product=Product.objects.get(id=prod_id)
    Cart(user=user,product=product).save()
    return redirect('/cart')
@login_required
def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0
    for p in cart:
        value = p.quantity * p.product.discounted_price
        amount = amount + value
    totalamount = amount + 40
    totalitem = 0 
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    return render(request,'app/addtocart.html',locals())


@login_required
def show_wishlist(request):
    user=request.user
    totalitem = 0 
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    product =Wishlist.objects.filter(user=user)
    return render(request,'app/wishlist.html',locals())

@method_decorator(login_required,name='dispatch')   
class Checkout(View):
    def get(self,request):
        totalitem = 0 
        wishitem=0
        if request.user.is_authenticated:
            totalitem = len(Cart.objects.filter(user=request.user))
            wishitem = len(Wishlist.objects.filter(user=request.user))
        user=request.user
        add=Customer.objects.filter(user=user)
        cart_items=Cart.objects.filter(user=user)
        famount = 0
        for p in cart_items:
            value = p.quantity * p.product.discounted_price
            famount = famount + value
        totalamount = famount +40    
        return render(request,'app/checkout.html',locals())
@login_required
def payment_done(request):
    pass    
    
@login_required   
def orders(request):
    totalitem = 0 
    wishitem=0
    if request.user.is_authenticated:
        totalitem = len(Cart.objects.filter(user=request.user))
        wishitem = len(Wishlist.objects.filter(user=request.user))
    order_placed=OrderPlaced.objects.filter(user=request.user)    
    return render(request,'app/order.html',locals())
    
@login_required     
def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }   
        return JsonResponse(data)      

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        user = request.user
        cart = Cart.objects.filter(user=user)
        amount=0
        for p in cart:
            value = p.quantity * p.product.discounted_price
            amount = amount + value
        totalamount = amount + 40
        data={
            'quantity':c.quantity,
            'amount':amount,
            'totalamount':totalamount
        }   
        return JsonResponse(data)      


       
@login_required
def remove_cart(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        
        # try:
            # Fetch the product object
        product = Product.objects.get(id=prod_id)
            
            # Fetch all cart items for the product and user
        cart_items = Cart.objects.filter(product=product, user=request.user)
            
        if cart_items.exists():
                # Delete the first cart item found
            cart_items.first().delete()

                # Calculate the cart total
            user = request.user
            cart = Cart.objects.filter(user=user)
            amount = sum(p.quantity * p.product.discounted_price for p in cart)
            totalamount = amount + 40  # Shipping charges can be dynamic or configurable

            data = {
                'amount': amount,
                'totalamount': totalamount
            }
            return JsonResponse(data)
        else:
            return JsonResponse({'error': 'Cart item does not exist'}, status=404)
        
       


@login_required
def plus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist(user=user, product=product).save()
        data = {
            'message': 'Wishlist Added Successfully'
        }
        return JsonResponse(data)
    
@login_required
def minus_wishlist(request):
    if request.method == 'GET':
        prod_id = request.GET.get('prod_id')
        product = Product.objects.get(id=prod_id)
        user = request.user
        Wishlist.objects.filter(user=user, product=product).delete()
        data = {
            'message': 'Wishlist Removed Successfully'
        }
        return JsonResponse(data)
   
def search(request):
    # Correct way to retrieve the 'search' query parameter
    query = request.GET.get('search', '')  # Defaults to an empty string if 'search' is not present
    
    totalitem = 0 
    wishitem = 0

    # Check if the user is authenticated before performing queries related to the user
    if request.user.is_authenticated:
        totalitem = Cart.objects.filter(user=request.user).count()
        wishitem = Wishlist.objects.filter(user=request.user).count()

    # Perform the search query only if 'query' is not empty
    if query:
        product = Product.objects.filter(Q(title__icontains=query))
    else:
        product = Product.objects.none()  # Return an empty queryset if the query is empty

    # Render the search results page with all the necessary context variables
    return render(request, 'app/search.html',locals())
