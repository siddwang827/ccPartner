from django.contrib.messages.api import MessageFailure
from django.shortcuts import redirect, render

from .models import Profile
from projects.models import  Group


from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .form import CustomerUserCreationForm, MessageForm, ProfileForm, HobbyForm
from . import utils

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
            messages.error(request, 'Username does not exist')

        user = authenticate( request, 
                             username=username, 
                             password=password )

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'account')

        else:
            messages.error(request, 'Username OR password is incorrect')

    return render(request, 'users/login-register.html')

        

def logoutUser(request):
    logout(request)
    messages.success(request, 'User logout')
    return redirect('login')




def profiles(request):
    profiles, search_query = utils.searchProfiles(request)
    custom_range, profiles = utils.paginateProfile(request, profiles, 2)

    context = {
        "profiles":profiles,
        "search_query": search_query,
        "custom_range":custom_range,
    }

    return render(request, 'users/profiles.html', context=context)


def userProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    topHobbies = profile.hobby_set.exclude(description__exact='')
    otherHobbies = profile.hobby_set.filter(description__exact='')
    context = {
        "profile":profile,
        'topHobbies': topHobbies,
        'otherHobbies': otherHobbies,
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
    

@login_required(login_url='login')
def createHobby(request):
    profile = request.user.profile
    form = HobbyForm()

    if request.method == "POST":
        form =  HobbyForm(request.POST)
        if form.is_valid():
            hobby = form.save(commit=False)
            hobby.owner = profile
            hobby.save()

            messages.success(request, 'Hobby was created successfully!')
            return redirect('account')
    
    context = {
        'form':form,
    }

    return render(request, 'users/hobby_form.html', context=context)


@login_required(login_url='login')
def updateHobby(request, pk):
    profile = request.user.profile
    hobby = profile.hobby_set.get(id=pk)
    form = HobbyForm(instance=hobby)

    if request.method == "POST":
        form = HobbyForm(request.POST, instance=hobby)
        if form.is_valid():
            form.save()
            messages.success(request, 'Hobby was updated successfully!')

            return redirect('account')

    context = {
        "form":form,
    }
    return render(request, 'users/hobby_form.html', context=context)

@login_required(login_url='login')
def deleteHobby(request, pk):
    profile = request.user.profile
    hobby = profile.hobby_set.get(id=pk)

    if request.method == "POST":
        hobby.delete()
        messages.success(request, 'Hobby was deleted successfully')

        return redirect('account')
    
    context = {
        "hobby":hobby,
    }
    return render(request, 'users/delete-hobby.html', context=context)


@login_required(login_url='login')
def inbox(request):
    profile = request.user.profile
    messageRequest = profile.messages.all()

    unreadCount = messageRequest.filter(is_read__in = ['False']).count()
    context = {
        "messageRequests": messageRequest, 
        "unreadCount":unreadCount,
    }

    return render(request, 'users/inbox.html', context=context)



@login_required(login_url='login')
def viewMessage(request, pk):
    profile = request.user.profile
    messageRequest = profile.messages.get(id=pk)

    if not messageRequest.is_read:
        messageRequest.is_read = True
        messageRequest.save()
    
    context = {
        "message": messageRequest,
    }

    return render(request, 'users/message.html', context=context)

def createMessage(request, pk):
    recipient = Profile.objects.get(id=pk)
    form = MessageForm()

    try:
        sender = request.user.profile
    except: 
        sender = None

    if request.method == "POST":
        form = MessageForm(request.POST)

        if form.is_valid():
            message = form.save(commit=False)
            message.sender = sender
            message.recipient = recipient
            
            if sender:
                message.email = sender.email
                message.name = sender.name
            
            message.save()
            messages.success(request, "Your message was successfully sent!")
            return redirect('user-profile', pk=recipient.id)
    
    context={
        'form':form,
        'recipient':recipient,
    }
    return render(request, 'users/message-form.html', context=context)