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
        member.group_id = None
        
        if group.member_1 == member:
            group.member_1 = None
        if group.member_2 == member:
            group.member_2 = None
        if group.member_3 == member:
            group.member_3 = None
        
        group.save()
        member.save()
        messages.success(request, f"You've kiced the memeber {member.username} out!")
    
        return redirect('account')
    
    context = {
        'member':member,
    }

    return render(request, 'projects/delete-template.html', context=context)
