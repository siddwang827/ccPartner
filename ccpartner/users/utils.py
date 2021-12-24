from django.db.models import Q
from .models import *


def searchProfiles(request):
    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')
        print(f'{search_query=}')

    profiles = Profile.objects.distinct().filter(
        Q(name__icontains=search_query) |
        Q(bio__icontains=search_query) | 
        Q(background__icontains=search_query) 
    )