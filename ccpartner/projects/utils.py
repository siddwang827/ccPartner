from .models import Application, Project, Module
from django.db.models import Q
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from users.models import Message

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
    ).filter(Q(is_active=True))

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



def checkApplication(applier, project):
    application, created = Application.objects.get_or_create(
        group = project.group,
        sender = applier,
        is_apply = True,
    )
    return created

def quitRequest(member, group):
    quitApplication, created = Application.objects.get_or_create(
        group = group,
        sender = member,
        is_apply = False,
    )
    return created


def NotificationMessage(sender, recipient, subject, body, is_apply_related=False):
    
    param = {
        "sender": sender,
        "recipient": recipient,
        "name": sender.username,
        "subject": subject,
        "body": body,
        "is_apply_related": is_apply_related,
    }

    Message.objects.create(**param)

    return 