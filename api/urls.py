from django.urls import path
from .views import themeList,userList,contactList,contactListId

urlpatterns = [
    path('themes/', themeList, name='themeList'),
    path('users/', userList, name='themeList'),
    path('contacts/', contactList, name='contactList'),
    path('contacts/<str:id>/', contactListId, name='contactListId'),
    # path('create_contact/', createContact, name='createContact'),


]