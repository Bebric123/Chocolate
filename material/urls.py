from django.contrib import admin
from django.urls import path, include
from .views import *

urlpatterns = [
    path('', MaterialsListView.as_view(), name='materials_list'),
    path('create/', MaterialCreateView.as_view(), name='create'),
    path('update/<int:pk>', MaterialUpdateView.as_view(), name='update'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('supplier/<int:pk>', SuppliersListView.as_view(), name='suppliers'),
    path('product/<int:pk>', ProductListView.as_view(), name='products'),
    path('supplier_update/<int:pk>', SupplierUpdateView.as_view(), name='suppliers_update'),

]
