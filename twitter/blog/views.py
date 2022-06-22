import profile
from django.http import HttpResponse
from django.shortcuts import render,redirect
from users.models import Profile
from .models import Post, Like
from .forms import CommentForm, PostForm
from itertools import chain
from django.core.paginator import Paginator,PageNotAnInteger, EmptyPage
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.db.models import Q

@login_required()
def homeview(request):
    return render(request,'blog/home.html')

@login_required()
def posts_of_following_profiles(request):
    #get looged in user profile
    profile = Profile.objects.get(user = request.user)
    #Check who we are following
    users = [user for user in profile.following.all()] 
    # intial values for variables
    posts = []
    qs = None
    # get the posts of people who we are following
    for u in users:
        p = Profile.objects.get(user = u)
        p_posts = p.post_set.all()
        posts.append(p_posts)
    # our posts
    my_posts = profile.post_set.all()
    posts.append(my_posts)
    #sort and chain querysets and unpack the posts list
    if len(posts)>0:
        qs = sorted(chain(*posts), reverse = True, key = lambda obj: obj.created)

    p = Paginator(qs, 3)
    page_number = request.GET.get('page')
    try:
        page_obj = p.get_page(page_number)
    except PageNotAnInteger:
        page_obj = p.page(1)
    except EmptyPage:
        page_obj = p.page(p.num_pages)
    for p in page_obj:
        print(p.author.id,request.user.id)
        if str(p.author) == str(request.user) :
            post_owner = True
        else:
            post_owner = False
        print(post_owner)
    return render(request, 'blog/main.html',{'profile':profile, 'posts':page_obj})


def create_tweet(request):
    form = PostForm(instance = request.user)
    if request.method == 'POST':
        form = PostForm(request.POST,)
        if form.is_valid():
            user = Profile.objects.get(user = request.user)
            form.instance.author = user
            form.save()
            return redirect('posts-follow-view')

    return render(request,'blog/create_tweet.html', {'form':form})


def comment_view(request,pk):
    post = Post.objects.get(id = pk)
    comments = post.comments.filter(active=True)

    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            comment_form.instance.name = request.user          
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            return redirect(request.META.get('HTTP_REFERER')) 
            #return redirect('comment')
    else:
        comment_form = CommentForm()                   
    return render(request,
                  'blog/comments.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form}) 

def like_post(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post_obj = Post.objects.get(id = post_id)
        
        if request.user in post_obj.liked.all():
            post_obj.liked.remove(request.user)
        else:
            post_obj.liked.add(request.user)

        like, created = Like.objects.get_or_create(user=request.user,  post_id = post_id)

        if not created:
            if like.value == 'Like':
                like.value = 'Unlike'
            else:
                like.value = 'Like'
        like.save()
    return redirect(request.META.get('HTTP_REFERER'))
    #return redirect('posts-follow-view') 

def update_post(request,pk):
    post = Post.objects.get(id = pk)
    form = PostForm(instance = post)
    if request.method == 'POST':
        form = PostForm(data=request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts-follow-view')
    return render(request,'blog/create_tweet.html',{'form':form})

def delete_post(request,pk):
    if request.method == 'POST':
        post = Post.objects.get(pk=pk)
        post.delete()
        return redirect('posts-follow-view')
    return render(request,'blog/post_delete_confirm.html')


def search_profile_view(request,*args,**kwargs):
    # k = Q()
    # profiles = Profile.objects.all()
    # for profile in profiles:
    #     k |= Q(user__icontains = profile)
    #     print(k)
    #return Profile.objects.filter(k)
    query = request.GET.get('q')
    print(query)
    if len(query) > 0:
        search_results = Profile.objects.filter(user__username__icontains = query)
    if len(search_results) == 0:
        search_results = False
    return render(request,'blog/search_profiles.html',{'search_results':search_results})