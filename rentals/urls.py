from django.urls import path
from . import views

urlpatterns = [
    path('login/',  views.login_view,  name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('', views.home, name='home'),  
    path('rent/<int:snowboard_id>/', views.rent_snowboard, name ='rent_snowboard'),
    path('return/<int:rental_id>/', views.return_snowboard, name='return_snowboard'),
    path('snowboards/', views.snowboard_list, name='snowboard_list'),
]



