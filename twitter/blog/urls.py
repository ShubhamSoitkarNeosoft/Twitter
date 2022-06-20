from django.urls import path
from . import views
urlpatterns = [
    path('posts/', views.posts_of_following_profiles, name = 'posts-follow-view'),
    path('home/',views.homeview, name = 'home'),
    path('create-tweet/',views.create_tweet, name = 'create-tweet-view'),
    path('comment/<int:pk>',views.comment_view, name = 'comment'),
    path('post-like/',views.like_post, name = 'like-post'),
    
]