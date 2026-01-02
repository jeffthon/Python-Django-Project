from django.urls import path
from .views import farmer_data_dashboard, PersonalData_view
from .import views

urlpatterns = [
    
    path('personal_data/',PersonalData_view,name='personal_data'),
    path('personal_data_dashboard/',farmer_data_dashboard,name='personal_data_dashboard'),
    path('personal_data/edit/', PersonalData_view, name='edit_personal_data'),
    path('logout/', views.user_logout, name='user_logout'),
    path('edit-product/<int:pk>/', views.edit_product, name='edit_product'),
]