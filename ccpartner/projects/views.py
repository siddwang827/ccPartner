from django.contrib.auth import login
from django.shortcuts import render, redirect
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required

# Create your views here.

def projects(request):
    projects = Project.objects.all()

    context = {
        "projects":projects,
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


# @login_required(login_url='login')
# def deleteProject(request):
#     return render(request, 'projects/delete_template.html', context=context)