from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
from . import views

urlpatterns = [
    path('', views.home),
    path('about/', views.about,name='about'),
    path('contact/', views.contact,name='contact'),
    path('category/<slug:val>', views.CategoryView.as_view(),name="category"),
    path('category-title/<val>', views.CategoryTitleView.as_view(),name="category-title"),
    path('product-detail/<int:pk>', views.ProductDetailView.as_view(),name="product-detail"),
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)