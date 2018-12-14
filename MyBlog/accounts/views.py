from django.shortcuts import render,redirect
from django.urls import reverse_lazy,reverse
from django.views.generic import CreateView
from django.contrib.auth.views import (PasswordChangeView,
                                PasswordResetView,
                                LoginView
                                )
from . import forms
from django.contrib.auth.forms import (PasswordChangeForm,
                            PasswordResetForm,
                            )

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.http import HttpResponse ,HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout


from .models import User



# Create your views here.

def user_login(request):
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')

        try:
            print("trying to authenticate")
            user=authenticate(email=email,password=password)
            print(user)
            if user:
                if user.is_active:
                    login(request,user)
                    return HttpResponseRedirect(reverse('post_list'))
                else:
                    HttpResponse("account is not active...")
            else:
                try:
                    user=User.objects.get(email=email)
                    if user.email_confirmed:
                        return HttpResponse("Incorrect password")
                    else:
                        current_site=get_current_site(request)
                        message = render_to_string('accounts/account_activate_message.html', {
                                'user':user,
                                'domain':current_site.domain,
                                'uid': urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                                'token': account_activation_token.make_token(user),
                            })
                        mail_subject = 'Activate your blog account.'
                        to_email = email
                        email_m = EmailMessage(mail_subject, message, to=[to_email])
                        email_m.send()
                        return HttpResponse("Email is not confirmed! Please Confirm")


                except:
                    return HttpResponse("Please sign Up!")
        except:
            return HttpResponse("Account is not registered ")
    else:
        print("in views")
        form=forms.UserLoginForm()
        return render(request,'accounts/login.html',{'form':form})




class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url=reverse_lazy('accounts:login')
    template_name='accounts/signup.html'

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            print("hello1")
            return self.form_valid(form,request)
        else:
            print("form invlaid")
            try:
                User.objects.get(email=request.POST['email'])
                return HttpResponse("Email is already registered")
            except:
                return HttpResponse("Password doesn't match")

    def form_valid(self,form,request):
        """If the form is valid, save the associated model."""
        self.object = form.save(commit=False)
        self.object.is_active = False
        self.object.save()
        print('hello2')
        current_site=get_current_site(request)
        message = render_to_string('accounts/account_activate_message.html', {
                'user':self.object,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(self.object.pk)).decode(),
                'token': account_activation_token.make_token(self.object),
            })
        mail_subject = 'Activate your blog account.'
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        return super().form_valid(form)



    """def form_valid(self,request,form):
        self.object = form.save()
        #self.object.is_active = False
        #self.object = self.object.save()
        current_site=get_current_site(request)
        message = render_to_string('accounts/account_activate_message.html', {
                'user':self.object,
                'domain':current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(self.object.pk)),
                'token': account_activation_token.make_token(self.object),
            })
        mail_subject = 'Activate your blog account.'
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(mail_subject, message, to=[to_email])
        email.send()
        #return HttpResponse('Please confirm your email address to complete the registration')
        return super().form_valid(form)"""

class CustomPasswordChangeView(PasswordChangeView):
    form_class = PasswordChangeForm
    success_url = reverse_lazy('post_list')
    template_name = 'accounts/password_change.html'

class CustomPasswordResetView(PasswordResetView):
    form_class = PasswordResetForm
    template_name = 'accounts/password_reset_form.html'
    subject_template_name = 'accounts/password_reset_subject.txt'
    email_template_name = 'accounts/password_reset_email.html'

def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.email_confirmed=True
        user.save()
        return redirect('accounts:logout')
    else:
        return HttpResponse('Activation link is invalid!')
