from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django import forms

class UserCreateForm(UserCreationForm):

    class Meta():
        fields =('username','email',)
        model=get_user_model()

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields['email'].label = 'Email Address'

class UserLoginForm(forms.Form):
    email=forms.EmailField(label="enter the email:")
    password=forms.CharField(widget=forms.PasswordInput,label="enter password")
