from django.urls import path
from . import views 
urlpatterns = [
    path('register/',views.registeruser, name = 'register'),
    path('login/',views.loginview, name = 'login'),
    path('logout/',views.logoutview, name = 'logout'),
    path('',views.profile_list_view, name = 'profile-list-view'),
    path('<pk>/',views.ProfileDetailView.as_view(), name = 'profile-detail-view'),
    path('profile-update/<int:pk>',views.profile_update, name = 'profile-update-view'),
    path('switch-follow',views.follow_unfollow_profile, name= 'follow-unfollow-view'),
    path('profile-list',views.profile_list, name = 'profile-list'),

]