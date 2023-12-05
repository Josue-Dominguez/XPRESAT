from importlib.resources import path
from django.urls import path

from .views import UserProfileView, EditProfile, AddFollower, RemoveFollower, ListFollowers, NotificationView, mark_as_read
from . import views

app_name="accounts"

urlpatterns = [
    path('notifications/', NotificationView.as_view(), name='notifications'),
    path('notifications/mark-as-read/<int:notification_id>/', mark_as_read, name='mark_as_read'),
    
    
    path('<username>/', UserProfileView, name="profile"),
    path('profile/edit', EditProfile, name="edit-profile"),

    path('profile/<int:pk>/followers/add', AddFollower.as_view(), name='add-follower'),
	path('profile/<int:pk>/followers/remove', RemoveFollower.as_view(), name='remove-follower'),

    

    path('profile/<int:pk>/followers/',ListFollowers.as_view(), name='followers-list'),


]
