from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    path('create-room/', views.create_room, name='create_room'),
    # keep this last — it's a catch-all slug
    path('<str:slug>/', views.chatroom, name='chatroom'),
]
