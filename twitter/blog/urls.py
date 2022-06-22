from django.urls import path
from . import views
urlpatterns = [
    path('posts/', views.posts_of_following_profiles, name = 'posts-follow-view'),
    path('home/',views.homeview, name = 'home'),
    path('create-tweet/',views.create_tweet, name = 'create-tweet-view'),
    path('comment/<int:pk>',views.comment_view, name = 'comment'),
    path('post-like/',views.like_post, name = 'like-post'),
    path('update-post/<int:pk>',views.update_post, name = 'update-post'),
    path('delete-post/<int:pk>',views.delete_post, name = 'delete-post'),
    
]