from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class CartForm(forms.ModelForm):
    
    class Meta:
        # Provide an association between the ModelForm and a model
        model = cart
        fields = ('pitem_id','pitem_quauntity')

    def clean(self):
        cleaned_data = super(CartForm, self).clean()
        # cleaned_data = self.cleaned_data
        #assert False, cleaned_data
        if(cleaned_data['pitem_quauntity'] > 20):
            raise forms.ValidationError("quantity limit exceeded")
        else:
            #assert False, cleaned_data
            return self.cleaned_data

class AddForm(forms.ModelForm):

    class Meta:
        model = item
        fields=('item_name','item_cost','item_discount','item_quantity','item_description')

  

class RegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True, widget=forms.TextInput(attrs={'placeholder': 'E-mail address'}))
    first_name = forms.CharField(required=True)
    last_name = forms.CharField(required=True)

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password1', 'password2')  

    #clean email field
    def clean_email(self):
        email = self.cleaned_data["email"]
        try:
            User._default_manager.get(email=email)
        except User.DoesNotExist:
            return email
        raise forms.ValidationError('duplicate email')

    #modify save() method so that we can set user.is_active to False when we first create our user
    def save(self, commit=True):        
        user = super(RegistrationForm, self).save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.is_active = False # not active until he opens activation link
            user.save()

        return user




'''class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    ver_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ('username', 'email', 'password','ver_password')

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        #assert False, cleaned_data['password']
        if(cleaned_data['password'] is None):
            raise forms.ValidationError("password")
        if(cleaned_data['password'] !=cleaned_data['ver_password'] ):
            raise forms.ValidationError("passwords do not match")
        else:
            #assert False, cleaned_data
            return self.cleaned_data

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = customer
        fields = ()'''


#'''widget=forms.HiddenInput(),'''       item.objects.get(id=self.cleaned_data['pitem_id'])      
