from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views
from django.contrib.auth import views as auth_view

from . forms import LoginForm,MyPasswordResetForm,MyPasswordChangeForm,MyPasswordForm

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

    #Order
    path('addtoCart/', views.addtoCart,name="addtoCart"),
    path('cart/', views.showCart,name="showCart"),
    path('checkout/', views.showCart,name="checkout"),
    path('plusCurt/', views.plusCurt,name="plusCurt"),



    path('updateAddress/<int:pk>', views.UpdateAddressView.as_view(),name="updateAddress"),



    
    #login authentication
    path('registration/', views.CustomerRegistrationView.as_view(),name="CustomerRegistration"),
    path('accounts/login/', auth_view.LoginView.as_view(template_name= 'app/login.html', authentication_form = LoginForm), name='login'),
    
    path('passwordChange/', auth_view.PasswordChangeView.as_view(template_name='app/passwordChange.html', form_class= MyPasswordChangeForm, success_url='/passwordChangeDone'),name='passwordChange'),
    path('passwordChangeDone/', auth_view.PasswordChangeDoneView.as_view(template_name='app/passwordChangeDone.html'),name='passwordChangeDone'),
    path('logout/', auth_view.LogoutView.as_view(next_page = 'login'), name='logout'),

    #password reset
    path('passwordReset/',auth_view.PasswordResetView.as_view(template_name = 'app/passwordReset.html',form_class= MyPasswordResetForm),name='passwordReset'),


    path('passwordReset/done/',auth_view.PasswordResetDoneView.as_view(template_name = 'app/passwordResetDone.html'),name='password_reset_done'),

    path('password_reset_confirm/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name = 'app/passwordResetConfirm.html',form_class= MyPasswordForm),name='password_reset_confirm'),

    path('password_reset_complete/',auth_view.PasswordResetCompleteView.as_view(template_name = 'app/passwordResetComplete.html'),name='password_reset_complete'),

    path('passwordReset/done/',auth_view.PasswordResetDoneView.as_view(template_name = 'app/passwordResetDone.html'),name='passwordResetDone'),

    path('passwordResetConfrim/<uidb64>/<token>/',auth_view.PasswordResetConfirmView.as_view(template_name = 'app/passwordResetConfirm.html',form_class= MyPasswordForm),name='passwordResetConfirm'),

    path('passwordResetComplete/',auth_view.PasswordResetCompleteView.as_view(template_name = 'app/passwordResetComplete.html'),name='passwordResetComplete'),


]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)