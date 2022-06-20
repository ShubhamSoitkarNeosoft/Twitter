from django.shortcuts import render,redirect
from django.views.generic import ListView, DetailView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Profile
from .forms import ProfileUpdateForm, UserRegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required



def registeruser(request):
    '''registers user'''
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            #messages.success(request, f'Account created for {username}.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def loginview(request):
    if request.method == 'POST':
        un = request.POST.get('un')
        ps = request.POST.get('ps')
        user = authenticate(username = un, password = ps)
        print('-------', user)
        if user is not None:
            login(request, user)
            return redirect('profile-list-view')
    return render(request,'users/login.html')

def logoutview(request):
    logout(request)
    return redirect ('login')



class ProfileListView(ListView, LoginRequiredMixin):
    model = Profile
    template_name = 'users/main.html'
    context_object_name = 'profiles' #default is object_list

    def get_queryset(self):
        return Profile.objects.all().exclude(user = self.request.user)
        
@login_required()      
def profile_list_view(request):
    profiles = Profile.objects.all().exclude(user = request.user)
    return render(request, 'users/main.html',{'profiles':profiles})

@login_required()
def profile_list(request):
    profiles = Profile.objects.all()
    return render(request,'users/profile-list.html',{'profiles':profiles})


class ProfileDetailView(DetailView):
    model = Profile
    template_name = 'users/detail.html'

    def get_object(self,**kwargs):
        pk = self.kwargs.get('pk')
        view_profile = Profile.objects.get(pk=pk)
        return view_profile

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        view_profile = self.get_object()
        my_profile = Profile.objects.get(user = self.request.user)
        if view_profile.user in my_profile.following.all():
            follow = True
        else:
            follow = False
        context["follow"] = follow
        return context

def profile_update(request,pk):
    pform = ProfileUpdateForm(instance= request.user.profile)
    if request.method == 'POST':
        pform = ProfileUpdateForm(request.POST, request.FILES, instance = request.user.profile)
        if pform.is_valid():
            pform.save()
            # try:
            #     profile =Profile.objects.create(user=request.user)    We can use this to create profile instance but instead use signals
            # except:
            #     pass
            return redirect('home')
    return render(request,'users/update_profile.html',{'pform':pform} )


def follow_unfollow_profile(request):
    if request.method == "POST":
        my_profile = Profile.objects.get(user = request.user)
        pk = request.POST.get('profile_pk')
        obj = Profile.objects.get(pk=pk)

        if obj.user in my_profile.following.all():
            my_profile.following.remove(obj.user)
        else:
            my_profile.following.add(obj.user)
        return redirect(request.META.get('HTTP_REFERER'))   # or use redirect('') url for loading same page
    return redirect('profile-list-view')






