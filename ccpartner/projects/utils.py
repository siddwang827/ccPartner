from .models import Project, Module
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def searchProjects(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')

    modules = Module.objects.filter(
        name__icontains = search_query
    )

    projects = Project.objects.distinct().filter(
        Q(title__icontains=search_query) |
        Q(description__icontains=search_query) |
        Q(modules__in=modules)
    )

    return projects, search_query



def paginateProject(request, projects, results):
    page = request.GET.get('page')
    results_num = results
    paginator = Paginator(list(projects), results_num)

    try: 
        projects = paginator.page(page)
    
    except PageNotAnInteger:
        # default page = 1
        page = 1
        projects = paginator.page(page)
    
    except EmptyPage:
        page = paginator.num_pages
        projects = paginator.page(page)

    # customize the range of the page to show
    page_num = int(page)
    last_page = paginator.num_pages

    leftIndex = 1 if (page_num-4) < 1 else (page_num-4)
    rightIndex = last_page if (page_num+4) > last_page else (page_num+4)

    custom_range = range(leftIndex, rightIndex+1)
    
    return custom_range, projects
