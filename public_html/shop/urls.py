from django.conf.urls import url,patterns
from django.views.generic.edit import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.conf.urls import include
from .views import *
from . import views

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),                  #Index url
    url(r'^redirec/$', RedirecView.as_view(), name='redirec'),      #Redirect
    url(r'^home/$', HomeView.as_view(), name='home'),               #home of customer
    url(r'^home_seller/$', HomeView.as_view(), name='home'),        #home of seller
    url(r'^cart/$', v_cartView.as_view(), name='cart'),             #cart 
    url(r'^wishlist/$', v_wishlistView.as_view(), name='wishlist'), #wishlist
    url(r'^checkout/$', checkoutView.as_view(), name='checkout'),   #checkout
    url(r'^updated_cart/$', updated_cartView.as_view(), name='updated_cart'),               #updated cart 
    url(r'^updated_wishlist/$', updated_wishlistView.as_view(), name='updated_wishlist'),   #updated Wishlist
    url(r'^add_to_cart/$', add_to_cartView.as_view(), name='add_to_cart'),                  #add to cart
    url(r'^add/$',addView.as_view(), name='add'),           #adding an item -seller
    url(r'^delete/$', deleteView.as_view(), name='delete'), #deleting an item -seller
    url(r'^update/$', updateView.as_view(), name='update'), #updating an item -seller
    url(r'^view_trans/$', v_transView.as_view(), name='view_trans'), #view Transaction -seller

    #user registration and confirmation
    url(r'^register/$', register_userView.as_view(), name='register_user'),
    #url(r'^confirm/(?P<activation_key>\w+)/$',register_confirmView.as_view(), name='register_confirm'),
    url(r'^confirm/(?P<activation_key>\w+)/$',views.register_confirm, name='register_confirm'),
    #login and logout using Login FormModel
    url(r'^login/$','django.contrib.auth.views.login',name='login',kwargs={'template_name': 'shop/login.html'}),
    url(r'^logout/$','django.contrib.auth.views.logout',name='logout',kwargs={'next_page': '/shop/'}    ),
    url(r'^shop/', include('django.contrib.auth.urls')),
    

    #url(r'^update_cart/$', views.update_cart, name='update_cart'),
    #url(r'^update_wishlist/$', views.update_wishlist, name='update_wishlist'),
    
    #url(r'^redirec/$', views.redirec, name='redirec'),
    #url(r'^register/$', views.register, name='register'),
    
    #url(r'^login/$', views.user_login, name='login'),
    #url(r'^login/$', 'django.contrib.auth.views.login',name="login"),
    #from django.conf.urls import patterns, url
	
    
    
]