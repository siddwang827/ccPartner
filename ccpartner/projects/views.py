from django.contrib import messages
from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from . import utils

from django.contrib.auth.decorators import login_required



# Create your views here.

def projects(request):
    projects, search_query = utils.searchProjects(request)
    custom_range, projects = utils.paginateProject(request, projects, 1)

    context = {
        "projects":projects,
        "search_query": search_query,
        'custom_range': custom_range,
    }

    return render(request, "projects/projects.html", context=context)


def project(request, pk):
    projObj = Project.objects.get(id=pk)
    
    context = {
        "project": projObj,
    }

    return render(request, "projects/project.html", context=context)



@login_required(login_url='login')
def createProject(request):
    profile = request.user.profile
    form = ProjectForm()

    if request.method == "POST":
        newModules = request.POST.get('newmodules').replace(',', ' ').split()
        newModules = list(map(str.capitalize, newModules))
        print(newModules)
        form = ProjectForm(request.POST, request.FILES)
        
        if form.is_valid():
            project = form.save(commit=False)
            project.owner = profile
            project.save()
            profile.is_host = True

            for module in newModules:
                moduleObj, created = Module.objects.get_or_create(name=module)
                project.modules.add(moduleObj)
            
            
            
            return redirect('projects')
    else:
        print("Error in creating Project")

    context = {
        "form":form,
    }
    return render(request, 'projects/project_form.html', context=context)


@login_required(login_url='login')
def updateProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)
    form = ProjectForm(instance=project)

    if request.method == "POST":
        newModules = request.POST.get('newmodules').replace(',', ' ').split()
        newModules = list(map(str.capitalize, newModules))

        # check if new image is uploaded
        if len(request.FILES):
            if not "default.jpg" in project.imageURL:
                project.featured_image.delete(save=True)

        form = ProjectForm(request.POST, request.FILES, instance=project)
        
        if form.is_valid():
            project = form.save()

            for module in newModules:
                moduleObj, created = Module.objects.get_or_create(name=module)
                project.modules.add(moduleObj)
            
            return redirect('project', pk=project.id)
        else:
            print('Error in Update Project...')
    
    context = {
        "form":form,
        "project": project,
    }
    return render(request, "projects/project_form.html", context=context)


@login_required(login_url='login')
def deleteProject(request, pk):
    profile = request.user.profile
    project = profile.project_set.get(id=pk)

    if request.method == "POST":
        project.delete()
        messages.success(request, 'Project was deleted successfully')
        return redirect('account')
    
    context = {
        "project":project,
    }

    return render(request, 'projects/delete-template.html', context=context)



@login_required(login_url='login')
def removeMember(request, pk):
    member = Profile.objects.get(id=pk)
    group_id = request.user.profile.group_id
    group = Group.objects.get(id=group_id)

    if request.method == "POST":
        group.removeMember(member)
        messages.success(request, f"You've kiced the memeber {member.username} out!")
    
        return redirect('account')
    
    context = {
        'member':member,
    }

    return render(request, 'projects/delete-template.html', context=context)



@login_required(login_url='login')
def quitTeam(request):
    profile = request.user.profile
    group = Group.objects.get(id=profile.group_id)

    if request.method == "POST":
        group.removeMember(profile)
        messages.success(request, f"You've quit the team of the project: {group.project} successfully.")

        utils.NotificationMessage(
            sender = profile,
            recipient = group.project.owner,
            subject = "Member quit",
            body = f"This letter is sent by system. Your Project member {profile} has left the team."
        )
        
        return redirect('account')
    
    context = {
        "group": group,
    }
    return render(request, 'projects/delete-template.html', context=context)
        


@login_required(login_url="login")
def apply(request, pk):
    project = Project.objects.get(id=pk)
    applier = request.user.profile
    newApp = utils.checkApplication(applier, project)

    if newApp:
        messages.success(request, "Your application has been sent to the project host.")
    else:
        messages.error(request, "You've applied for the project before.")
    
    return redirect('project', pk=project.id)



@login_required(login_url='login')
def applyBox(request):
    profile = request.user.profile
    group = Group.objects.get(id=profile.group_id)
    applyRequests = Application.objects.distinct() \
                            .filter( group=group )
    context = {
        "applyRequests":applyRequests,
        "project":group.project,
    }

    return render(request, 'projects/apply-box.html', context=context)


@login_required(login_url='login')
def verifyApply(request, pk):
    application = Application.objects.get(id=pk)
    group = application.group
    applier = application.sender
    host = group.project.owner

    if request.method == "POST":
        decision = request.POST.get('decision')
        if decision == 'reject':
            subject = 'Application Declined'
            body = f'Sorry, your application for porject {group.project} by the host'
            messages.success(request, f"You've declined the {applier}'s application")

        else:
            # Check Whether the applier is already in a project
            if applier.group_id:
                subject = 'Application Error'
                body = f"Your Application for {group.project} was failed because yor're already in other project."
                messages.info(request, f"The applier {applier} has already attend other project")
            
            # Check whether the group is full
            elif group.is_full:
                subject = 'Application Error'
                body = f"The project: {group.project} you applied is already full"
                messages.info(request, "Your project team is already full.")
            
            else:
                group.addMember(applier)
                applier.group_id = group.id
                applier.save()
                subject = "Application Accepted"
                body = f"Congratulation! Your application for project {group.project} was accepted by the host!"
                messages.success(request, f"You've accept {applier} application as your team member.")

        utils.NotificationMessage(
            recipient = applier,
            sender = host,
            subject = subject,
            body = body
        ) 

        application.delete()
        return redirect('apply-box')

    context={
        'apply':application,
    }
    return render(request, 'projects/verify-apply.html', context=context)
