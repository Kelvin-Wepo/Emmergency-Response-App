
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    
    # path('signup/', views.base_register, name='signup'),
    
    
    path('public_register/', views.public_register, name='register'),
    
    # path('owner_register/', views.owner_register, name='owner_register'),
    
    
    path('login/', views.user_login, name='login'),
    
    path('admin/', views.admin, name='admin'),
    
    path('logout/', views.user_logout, name='logout'),
    
    path('profile/', views.profile, name='profile'),
    
    path('update_profile/', views.update_profile, name ='update'),
    
    path('owner_home/', views.owners, name='owner'),
    
    path('add_ambulance/', views.add_ambulance, name='add'),
    
    path('ambulance/<int:ambulance_id>/', views.single_ambulance, name='single'),
    
    path('update/<int:ambulance_id>/details', views.update_ambulance, name='update'),
    
    
    path('delete/<int:ambulance_id>', views.delete_ambulance, name='delete'),
    
    path('services/', views.services, name='services'),
    
    path('user_ambulance/<int:ambulance_id>/', views.user_single_ambulance, name='single_ambulance'),
    
    path('comment/<int:ambulance_id>', views.comment, name='comment'),
    
    path('hire/<int:ambulance_id>', views.order, name='order'),
    
    
    
]
