"""
URL configuration for myproject project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from myapp import views
from myapp.views import CustomLoginView, create_order, building_order_view, order_history
from django.contrib.auth.views import LogoutView
from django.contrib.auth import views as auth_views
from datetime import datetime

current_year = datetime.now().year
current_month = datetime.now().month



urlpatterns = [
    path('admin/', admin.site.urls), # 관리자 페이지
    path('', views.home_view, name='home'),  # 홈페이지 URL 설정
    # Developer CRUD URLs
    # path('developers/', views.developer_list, name='developer_list'),
    # path('developer/create/', views.developer_create, name='developer_create'),
    # path('developer/update/<int:pk>/', views.developer_update, name='developer_update'),
    # path('developer/delete/<int:pk>/', views.developer_delete, name='developer_delete'),
    # Building CRUD URLs
    # Apartment CRUD URLs
    # path('apartments/', views.apartment_list, name='apartment_list'),
    # path('apartments/create/', views.apartment_create, name='apartment_create'),
    # path('apartments/<int:pk>/update/', views.apartment_update, name='apartment_update'),
    # path('apartments/<int:pk>/delete/', views.apartment_delete, name='apartment_delete'),
    # Buyer CRUD URLs
    # path('buyers/', views.buyer_list, name='buyer_list'),
    # path('buyers/create/', views.buyer_create, name='buyer_create'),
    # path('buyers/update/<int:pk>/', views.buyer_update, name='buyer_update'),
    # path('buyers/delete/<int:pk>/', views.buyer_delete, name='buyer_delete'),
    # Contract CRUD URLs
    # path('contracts/', views.contract_list, name='contract_list'),
    # path('contracts/create/', views.contract_create, name='contract_create'),
    # path('contracts/update/<int:pk>/', views.contract_update, name='contract_update'),
    # path('contracts/delete/<int:pk>/', views.contract_delete, name='contract_delete'),
    # Login URLs
    path('register/', views.register, name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    # order URLs
    path('order/create/', create_order, name='create_order'),
    path('order_history/', order_history, name='order_history'),
    # path('building-order/', views.building_order_view, name='building_order'),
    path('building-order/<int:order_id>/<int:land_quantity>/<int:building_quantity>/', building_order_view, name='building_order_view'),
    # find password
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    path('password_change/', views.change_password, name='password_change'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('all_events/', views.all_events, name='all-events'),
    path('add_event/', views.add_event, name='add-event'),
    path('update/', views.update, name='update'),
    path('remove/', views.remove, name='remove'),
    # path('', views.dashboard_view, name='home'),



]


