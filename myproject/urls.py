from django.contrib import admin
from django.urls import path
from main import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('inventory/add/', views.add_product, name='add_product'),
    path('orders/', views.index, name='index'),
    path('order/update/<int:pk>/', views.order_update, name='order_update'),
    path('order/delete/<int:pk>/', views.order_delete, name='order_delete'),
]