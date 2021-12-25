from django.core.paginator import PageNotAnInteger, Paginator, EmptyPage
from django.db.models import Q
from .models import *


def searchProfiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        print(f'{search_query=}')

    hobbys = Hobby.objects.filter(
        name__icontains = search_query
    )

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(username__icontains=search_query) |
        Q(bio__icontains=search_query) | 
        Q(background__icontains=search_query) |
        Q(hobby__in=hobbys)
    )

    return profiles, search_query


def paginateProfile(request, profiles, results):
    page = request.GET.get('page')
    result_num = results
    paginator = Paginator(list(profiles), result_num)

    try: 
        profiles = paginator.page(page)
    
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)

    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    # customize the range of the page to show
    current_page = int(page)
    last_page = paginator.num_pages

    leftIndex = 1 if (current_page-4) < 1 else (current_page-4)
    rightIndex = last_page if (current_page+4) > last_page else (current_page+4)

    custom_range = range(leftIndex, rightIndex+1)

    return custom_range, profiles