from django.urls import path
from django.contrib.auth import views as auth_views
from . import views 
urlpatterns = [
    path('register/',views.registeruser, name = 'register'),
    path('login/',views.loginview, name = 'login'),
    path('logout/',views.logoutview, name = 'logout'),
    path('',views.profile_list_view, name = 'profile-list-view'),
    path('profile-detail/<pk>/',views.ProfileDetailView.as_view(), name = 'profile-detail-view'),
    path('profile-update/<int:pk>',views.profile_update, name = 'profile-update-view'),
    path('switch-follow',views.follow_unfollow_profile, name= 'follow-unfollow-view'),
    path('profile-list',views.profile_list, name = 'profile-list'),
    #path('profile-detail/<int:pk>/',views.profile_detail_view, name = 'profile-detail-view'),


    #Reset password urls
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name = 'users/password_reset.html'),
         name='reset_password'),

    path('reset_password_sent/',auth_views.PasswordResetDoneView.as_view(template_name = 'users/password_reset_sent.html'),
    name ='password_reset_done'),

    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name = 'users/password_reset_confirm.html'),
        name='password_reset_confirm'),

    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name = 'users/password_reset_complete.html'),
        name='password_reset_complete'),

]