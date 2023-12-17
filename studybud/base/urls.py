from django.urls import path

from . import views


urlpatterns = [
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_page, name='register'),
    path('', views.home_page, name='home'),
    path('room/<str:pk>', views.room_page, name='room'),
    path('create-room/', views.create_room, name='create-room'),
    path('update-room/<str:pk>', views.update_room, name='update-room'),
    path('delete/<str:pk>', views.delete_obj, name='delete'),
    path('delete-message/<str:pk>', views.delete_message, name='delete-message'),
    path('profile/<str:pk>', views.profile_page, name='profile'),
]
