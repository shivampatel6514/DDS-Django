from django.urls import path
from .views import themeList,userList,contactList,contactListId,userListId,themeListId,sitedataList,sitedataListId

urlpatterns = [
    path('themes/', themeList, name='themeList'),
    path('themes/<str:id>/', themeListId, name='themeListId'),

    path('users/', userList, name='userList'),
    path('users/<str:id>/', userListId, name='userListId'),

    path('contacts/', contactList, name='contactList'),
    path('contacts/<str:id>/', contactListId, name='contactListId'),


    path('sitedata/', sitedataList, name='sitedataList'),
    path('sitedata/<str:id>/', sitedataListId, name='sitedataListId'),
    
    


]