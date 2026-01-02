from django.contrib import admin
from django.urls import path
from .import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    
    path('', views.homepage,name='accounts'),
    path('login/',views.user_login,name='user_login'),
    path('register/',views.register,name='register'),
    path('customer-dashboard/', views.customer_dashboard, name='customer_dashboard'),
    path('farmer-dashboard/', views.farmer_dashboard, name='farmer_dashboard'),
    path('logout/',auth_views.LogoutView.as_view(),name='logout'),
    path('my-admin',views.admin_dashboard,name='admin-page'),
    path('django-admin/', admin.site.urls),
    path('approve-product/<int:product_id>/', views.approve_product, name='approve_product'),
    path('approve-farmer/<int:role_id>/', views.approve_farmer, name='approve_farmer'),
    path('my-custom-admin/', views.admin_dashboard, name='admin_page'),
    path('logout/', views.user_logout, name='user_logout'),
    path('product/delete/<int:product_id>/', views.delete_product, name='delete_product'),
    path('admin-panel/toggle-featured/<int:product_id>/', views.toggle_featured, name='toggle_featured'),
]