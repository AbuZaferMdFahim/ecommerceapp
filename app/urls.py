from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_view

from . forms import LoginForm,MyPasswordResetForm,MyPasswordChangeForm

from . forms import LoginForm,MyPasswordResetForm


urlpatterns = [
    path('', views.home),
    path('about/', views.about,name='about'),
    path('contact/', views.contact,name='contact'),
    path('category/<slug:val>', views.CategoryView.as_view(),name="category"),
    path('category-title/<val>', views.CategoryTitleView.as_view(),name="category-title"),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(),name="product-detail"),
    path('profile/', views.ProfileView.as_view(),name="profile"),
    path('address/', views.address,name="address"),

    path('updateAddress/<int:pk>', views.UpdateAddressView.as_view(),name="updateAddress"),


    
    #login authentication
    path('registration/', views.CustomerRegistrationView.as_view(),name="CustomerRegistration"),
    path('accounts/login/', auth_view.LoginView.as_view(template_name= 'app/login.html', authentication_form = LoginForm), name='login'),
    path('password-reset/', auth_view.PasswordResetView.as_view(template_name= 'app/password_reset.html', form_class = MyPasswordResetForm), name='password_reset'),
    path('passwordChange/', auth_view.PasswordChangeView.as_view(template_name='app/passwordChange.html', form_class= MyPasswordChangeForm, success_url='/passwordChangeDone'),name='passwordChange'),
    path('passwordChangeDone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordChangeDone.html'),name='passwordChangeDone'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)