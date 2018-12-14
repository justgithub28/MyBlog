from django.urls import path,re_path
from django.contrib.auth import views as auth_views
from . import views
from django_otp.forms import OTPAuthenticationForm
from django.urls import reverse_lazy

app_name='accounts'
urlpatterns = [
        #re_path(r'^login/$',auth_views.LoginView.as_view(template_name='accounts/login.html'),name='login'),

        re_path(r'^login/$',views.user_login,name='login'),


        re_path(r'^logout/$',auth_views.LogoutView.as_view(),name='logout'),
        re_path(r'^signup/$',views.SignUp.as_view(),name='signup'),
        re_path(r'^change-password/$',views.CustomPasswordChangeView.as_view(),name='change-password'),
        re_path(r'^password_reset/$',views.CustomPasswordResetView.as_view(),name='password_reset'),
        re_path(r'^password_reset/done/$',auth_views.PasswordResetDoneView.as_view(template_name='accounts/password_reset_done.html'),name='password_reset_done'),
        re_path(r'^reset/<uidb64>/<token>/$',auth_views.PasswordResetConfirmView.as_view(template_name='accounts/password_reset_confirm.html'),name='password_reset_confirm'),
        re_path('^reset/done/$',auth_views.PasswordResetCompleteView.as_view(template_name='accounts/password_reset_complete.html') ,name='password_reset_complete'),
        re_path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
        ]
