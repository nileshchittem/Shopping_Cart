from django.shortcuts import render, get_object_or_404, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from .models import *
from django.template import RequestContext, loader
from .forms import *
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.conf import settings
from django.shortcuts import redirect
from django.contrib import auth
from django.core.context_processors import csrf
from django.core.mail import send_mail
import hashlib, datetime, random
from django.utils import timezone
from django.views.generic.base import *
from django.views.generic.edit import FormView



mess=""#global message variable 



#Redirects The page to HOme showing the message
class RedirecView(TemplateView):
    template_name = "shop/redirec.html"

    def get_context_data(self, **kwargs):
        context = super(RedirecView, self).get_context_data(**kwargs)
        global mess
        context={'mess':mess}
        mess=""
        return context

#index page it redirects to login page showing the message
class IndexView(TemplateView):
    template_name = "shop/index.html"

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        global mess
        context={'mess':mess}
        mess=""
        return context



#homepage of  seller and customer both
class HomeView(TemplateView):
    template_name = ""
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():#redirect if user is not authenticated
            return redirect('/shop')
        else:
            return super(HomeView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        try:
            self.request.user.seller
            item_list=item.objects.filter(item_seller=self.request.user.seller)  
            context = {'item_list': item_list,}
            self.template_name="shop/home_seller.html"
            return context
        except:
            item_list=item.objects.filter(item_quantity__gt = 0).order_by('id')
            context = {'item_list': item_list,}
            self.template_name="shop/home.html"
            return context

#view cart for customer 
class v_cartView(TemplateView):
    template_name = "shop/cart.html"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/shop')
        else:
            return super(v_cartView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        cust_name=self.request.user.customer
        cart_list=cart.objects.filter(c_id=cust_name,typec='c')
        cost_list=[]
        totalcost=0
        for cart2 in cart_list:
            cost=cart2.pitem_id.item_cost*cart2.pitem_quauntity
            cost_list.append({
                'item':cart2.pitem_id,
                'quantity':cart2.pitem_quauntity,
                'cost':cost,
                })
            totalcost+=cost
        context =  {'cart_list': cart_list,'cost_list':cost_list,'totalcost':totalcost,}
        return context

#wishlist view for customer
class v_wishlistView(TemplateView):
    template_name = "shop/wishlist.html"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/shop')
        else:
            return super(v_wishlistView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        cust_name=self.request.user.customer
        cart_list=cart.objects.filter(c_id=cust_name,typec='w')

        cost_list=[]
        totalcost=0
        for cart2 in cart_list:
            cost=cart2.pitem_id.item_cost*cart2.pitem_quauntity
            cost_list.append({
                'item':cart2.pitem_id,
                'quantity':cart2.pitem_quauntity,
                'cost':cost,
                })
            totalcost+=cost
        context =  {'cart_list': cart_list,'cost_list':cost_list,'totalcost':totalcost,}
        return context


#checkout adds tranasction and orders and redirects to home
class checkoutView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/shop')
        else:
            a=self.request.POST['total']
            global mess
            t=transaction(t_cost=a)
            t.t_id=request.user.customer
            cart_list=cart.objects.filter(c_id=self.request.user.customer,typec='c')
            t.save()
            for items in cart_list:
                it=items.pitem_id
                it.item_quantity-=items.pitem_quauntity
                it.save()
                o=order(o_id=t,o_item=items.pitem_id,o_quantity=items.pitem_quauntity)
                o.save()
            cart.objects.filter(c_id=self.request.user.customer,typec='c').delete()
            mess="successfully checked out"
            return redirect('/shop/redirec/')



#updates the cart 
class updated_cartView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/shop')
        else:
            item_list=item.objects.get(item_name=request.POST['itemx'])
            cart_list=cart.objects.get(c_id=request.user.customer,typec='c',pitem_id=item_list)
            cart_list.pitem_quauntity=int(request.POST['q'])
            cart_list.save()
            return redirect('/shop/cart/')


#updates the wishlist
class updated_wishlistView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/shop')
        else:
            item_list=item.objects.get(item_name=request.POST['itemx'])
            cart_list=cart.objects.get(c_id=request.user.customer,typec='w',pitem_id=item_list)
            cart_list.pitem_quauntity=int(request.POST['q'])
            cart_list.save()
            return redirect('/shop/wishlist/')



#add to cart and wishlist  using CartForm 
class add_to_cartView(FormView):
    template_name = 'shop/add_to_cart.html'
    form_class = CartForm
    success_url = '/shop/redirec/'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/shop')
        else:
            return super(add_to_cartView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        
        typecq="c"
        if self.request.POST['submit']=="cart":
            typecq="c"
        elif self.request.POST['submit']=="wishlist":
            typecq="w"


        cart_item = cart.objects.get_or_create(
            pitem_id=form.cleaned_data['pitem_id'],c_id=self.request.user.customer,typec=typecq)
        cart_item[0].c_id=self.request.user.customer
        cart_item[0].pitem_quauntity += form.cleaned_data['pitem_quauntity']
        cart_item[0].typec=typecq
        
        global mess 
        
        if(typecq=="c"):
            cart_item[0].save()
            mess="successfully added to cart"
            try:
                if(self.request.POST['flag']=="1"):
                    cart.objects.filter(pitem_id=form.cleaned_data['pitem_id'],c_id=self.request.user.customer,typec='w').delete()
            except:
                pass
        elif(typecq=="w"):
            cart_item[0].save()
            mess="successfully added to wishlist"


        return super(add_to_cartView, self).form_valid(form)



#seller part

#adding an item
class addView(FormView):
    template_name = 'shop/add.html'
    form_class = AddForm
    success_url = '/shop/redirec/'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/shop')
        else:
            return super(addView, self).dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        item_add=item(item_name=form.cleaned_data['item_name'],item_cost=form.cleaned_data['item_cost'],
                item_discount=form.cleaned_data['item_discount'],item_quantity=form.cleaned_data['item_quantity'],
                item_description=form.cleaned_data['item_description'],item_seller=self.request.user.seller)
        item_add.save()
        global mess
        mess="item added"
        return super(addView, self).form_valid(form)

#deleting an item
class deleteView(View):
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/shop')
        else:
            item_id=request.POST['pitem_id']
            item.objects.get(id=item_id).delete()
            global mess
            mess="item deleted"
            return redirect("/shop/redirec")
            #return super(deleteView, self).dispatch(request, *args, **kwargs)

#updating an item
class updateView(TemplateView):
    template_name="shop/update.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/shop')
        else:
            return super(updateView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        item_id=self.request.GET['pitem_id']
        item_update=item.objects.get(id=item_id)
        context={'item':item_update}
        return context

    def post(self, request):
        item_update=item.objects.get(id=request.POST['item_id'])
        item_update.item_name=request.POST['item_name']
        item_update.item_cost=request.POST['item_cost']
        item_update.item_discount=request.POST['item_discount']
        item_update.item_description=request.POST['item_description']
        item_update.item_quantity=request.POST['item_quantity']
        item_update.save()
        global mess
        mess="item updated"
        return redirect('/shop/redirec')
        

    
#view Transctions
class v_transView(TemplateView):
    template_name = "shop/view_trans.html"
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return redirect('/shop')
        else:
            return super(v_transView, self).dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        item_list=item.objects.filter(item_seller=self.request.user.seller)
        orderlist=[]
        for items in item_list:
            order_list=order.objects.filter(o_item=items)
            for orders in order_list:
                orderlist.append(orders)
        context={'itemlist':orderlist}
        return context





#register User 
class register_userView(FormView):
    template_name = 'shop/register.html'
    form_class = RegistrationForm
    success_url = '/shop/'

    def form_valid(self, form):
        form.save()
        username = form.cleaned_data['username']
        email = form.cleaned_data['email']
        salt = hashlib.sha1(str(random.random())).hexdigest()[:5]            
        activation_key = hashlib.sha1(salt+email).hexdigest()            
        key_expires = datetime.datetime.today() + datetime.timedelta(2)

        #Get user by username
        user=User.objects.get(username=username)

        # Create and save user profile                                                                                                                                  
        new_profile = UserProfile(user=user, activation_key=activation_key, 
            key_expires=key_expires)
        new_profile.save()

        # Send email with activation key
        email_subject = 'Account confirmation'
        email_body = "Hey %s, thanks for signing up. To activate your account, click this link within \
        48hours http://127.0.0.1:8000/shop/confirm/%s" % (username, activation_key)

        send_mail(email_subject, email_body, 'myemail@example.com',
            [email], fail_silently=False)
        global mess
        mess="Registration Successfull"
        return super(register_userView, self).form_valid(form)


#user registration confromation

'''class register_confirmView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            return redirect('shop/home')
        else:
            # check if there is UserProfile which matches the activation key (if not then display 404)
            user_profile = get_object_or_404(UserProfile, activation_key=self.activation_key)
            global mess
            #check if the activation key has expired, if it hase then render confirm_expired.html
            if user_profile.key_expires < timezone.now():
                mess="confirmation ID expired"
                return redirect('/shop/')
            #if the key hasn't expired save user and set him as active and render some template to confirm activation
            user = user_profile.user
            user.is_active = True
            user.save()
            mess="Thank You ,Your Account is Activated"
            return redirect("/shop/home")
            #return super(deleteView, self).dispatch(request, *args, **kwargs)'''


def register_confirm(request, activation_key):
    #check if user is already logged in and if he is redirect him to some other url, e.g. home
    if request.user.is_authenticated():
        HttpResponseRedirect('shop/home')

    # check if there is UserProfile which matches the activation key (if not then display 404)
    user_profile = get_object_or_404(UserProfile, activation_key=activation_key)
    global mess
    #check if the activation key has expired, if it hase then render confirm_expired.html
    if user_profile.key_expires < timezone.now():
        mess="confirmation ID expired"
        return render_to_response('/shop/')
    #if the key hasn't expired save user and set him as active and render some template to confirm activation
    user = user_profile.user
    user.is_active = True
    user.save()
    mess="Thank You ,Your Account is Activated"
    return HttpResponseRedirect('/shop/home')
    return render_to_response('shop/confirm.html')