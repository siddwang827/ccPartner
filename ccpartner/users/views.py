from django.shortcuts import redirect, render

from .models import Profile
from projects.models import  Group


from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .form import CustomerUserCreationForm, ProfileForm


def registerUser(request):
    page = 'register'
    form = CustomerUserCreationForm()

    if request.method == 'POST':
        form = CustomerUserCreationForm(request.POST)
        
        if form.is_valid():
            user = form.save(commit=False)
            user.save()

            messages.success(request, f'Welcome to the ccPartner, {user}')
            login(request, user)
            return redirect('profiles')
        else:
            messages.error(request, "An error has occured during register...")
    
    context = {
        'form':form,
        'page':page,
    }
    return render(request, 'users/login-register.html', context=context)



def loginUser(request):
    if request.user.is_authenticated:
        return redirect('profiles')
    
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "Username doesn't exist")
            return redirect('login')

        user = authenticate(request, username=username, password=password)
        
        if user:
            login(request, user)
            messages.success(request, f"Welcome back, {user.username}!")
            return redirect("profiles")
        else:
            messages.error(request, 'Username or password is incorrect')
    
    return render(request, 'users/login-register.html')


def logoutUser(request):
    logout(request)
    messages.success(request, 'User logout')
    return redirect('login')




def profiles(request):
    profiles = Profile.objects.all()

    context = {
        "profiles":profiles,
    }

    return render(request, 'users/profiles.html', context=context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)

    context = {
        "profile":profile,
    }

    return render(request, 'users/user-profile.html', context=context)


@login_required(login_url='login')
def userAccount(request):
    profile = request.user.profile
    if profile.group_id:
        group = Group.objects.get(id=profile.group_id)
        project = group.project
    else:
        group, project = None, None


    context = {
        'profile':profile,
        'group': group,
        'project': project,
    }
    
    return render(request, 'users/account.html', context=context)


@login_required(login_url='login')
def updateProfile(request):
    profile = request.user.profile
    form = ProfileForm(instance=profile)

    if request.method == 'POST':
        form = ProfileForm(request.POST, 
                           request.FILES,
                           instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your Profile is updated successfully!')
            return redirect('account')
    
        else:
            messages.error(request, "Please check the fields in your profile form again...")
    
    context = {
        'form':form,
    }

    return render(request, 'users/profile_form.html', context=context)
    
        