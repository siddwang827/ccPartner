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
            
            form.save_m2m()
            
            
            
            return redirect('project', project.id)
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
        project.featured_image.delete(save=True)
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
        utils.NotificationMessage(
            sender = request.user.profile, 
            recipient = member, 
            subject = "Project quit notification.", 
            body = f"This message is sent by system.\nYou've been removed from team of project: {group.project} by host.",
            )
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
        quitRequest = utils.quitRequest(member=profile, group=group)
        if quitRequest:
            messages.success(request, f"Your quit request had been sent to the host.")
        else:
            messages.error(request, f"You've already sent the quit application, please wait for the host to accept your request.")
        
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
                            .filter( group=group, is_apply=True )
    
    quitRequests = Application.objects.distinct() \
                            .filter( group=group, is_apply=False )
    context = {
        "applyRequests":applyRequests,
        "quitRequests": quitRequests,
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
            body = f'This message is sent by System.\nSorry, your application for porject {group.project} was declined by the host'
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
            body = body,
            is_apply_related = True,
        ) 

        application.delete()
        return redirect('apply-box')

    context={
        'apply':application,
    }
    return render(request, 'projects/verify-apply.html', context=context)


@login_required(login_url='login')
def verifyQuit(request, pk):
    quitRequest = Application.objects.get(id=pk)

    if request.method == "POST":
        decision = request.POST.get('decision')
        if decision == 'reject':
            messages.success(request, f"You've REJECTED the quit request from member: {quitRequest.sender}")
            subject = "Quit Request Rejected"
            body = "This Message is sent by system.\nYour quit request has been REJECTED by the host."
            
        
        elif decision == "confirm":
            messages.success(request, f"You've ACCEPTED the quit request from member: {quitRequest.sender}")
            subject = "Quit Request Confirmed"
            body = "This Message is sent by system.\nYour quit request has been ACCEPTED by the host, go to join another project group!"
            quitRequest.group.removeMember(quitRequest.sender)

        

        utils.NotificationMessage(
            sender = request.user.profile,
            recipient = quitRequest.sender,
            subject = subject,
            body = body,
            is_apply_related = True,
        )

        quitRequest.delete()
        return redirect('apply-box')

    context = {
        'quitRequest': quitRequest,
    }

    return render(request, "projects/verify-quit.html", context=context)