from django.urls import path

from .views import ItemsCreateView, items_list, list_mac_address, form_create
urlpatterns = [
    path('', ItemsCreateView.as_view(), name='home'),
    path('items', items_list, name='items-list'),
    path('mac', list_mac_address, name='mac-list'),
    path('list', form_create, name='list'),
]