from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
import datetime

# Create your models here.
class seller(models.Model):
    user = models.OneToOneField(User, related_name='seller')
    #verified=models.BooleanField(default=False)
    def __str__(self):             
        return self.user.username

class item(models.Model):
    # item_id =models.AutoField(primary_key=True, unique=True, default = 0)
    item_name=models.CharField(max_length=200)
    item_cost=models.DecimalField(max_digits=19,decimal_places=2)
    item_discount=models.DecimalField(max_digits=19,decimal_places=2)
    item_quantity=models.SmallIntegerField()
    item_description=models.TextField()
    item_seller=models.ForeignKey(seller)

    def __str__(self):             
        return self.item_name

    def out_of_stock(self):
        return self.item_quantity <= 0

class customer(models.Model):
    user = models.OneToOneField(User, related_name='customer')
    verified=models.BooleanField(default=True)
    def __str__(self):             
        return self.user.username


class cart(models.Model):
    c_id=models.ForeignKey(customer)
    pitem_id=models.ForeignKey(item)
    pitem_quauntity=models.SmallIntegerField(default=0)
    typec=models.CharField(max_length=2)
    
    def __str__(self):
        return str(self.c_id)+" "+self.pitem_id.item_name +' '+str(self.pitem_quauntity)+' '+self.typec

    




class transaction(models.Model):
    # t_id=models.AutoField(primary_key=True, unique=True, default = 0)
    t_id=models.ForeignKey(customer)
    t_date=models.DateTimeField(default=timezone.now)
    t_cost=models.DecimalField(max_digits=19,decimal_places=2)

    def was_recent(self):
        return self.t_date >= timezone.now() - datetime.timedelta(days=1)

    was_recent.admin_order_field = 't_date'

    def __str__(self):             
        return str(self.id)

class order(models.Model):
    o_id=models.ForeignKey(transaction)
    o_item=models.ForeignKey(item)
    o_quantity=models.SmallIntegerField()

    def __str__(self):             
        return str(self.o_id)+" "+str(self.o_item)+" "+str(self.o_quantity)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    activation_key = models.CharField(max_length=40, blank=True)
    key_expires = models.DateTimeField(default=datetime.date.today())
      
    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name_plural=u'User profiles'