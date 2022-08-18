from .models import Profiles, Skills
from django.db.models import Q


from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage



def paginateProfiles(request,profiles,results):
    
    page = request.GET.get('page')

    paginator = Paginator(profiles,results)

    try:
        profiles = paginator.page(page)
    except PageNotAnInteger:
        page = 1
        profiles = paginator.page(page)
    except EmptyPage:
        page = paginator.num_pages
        profiles = paginator.page(page)

    LeftIndex = (int(page) - 1)

    if LeftIndex < 1 :
        LeftIndex = 1

    RightIndex = (int(page) + 2)

    if RightIndex > paginator.num_pages:
        RightIndex = paginator.num_pages + 1
    custom_range = range(LeftIndex, RightIndex)

    return custom_range,profiles

def searchProfiles(request):

    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')   

    skills = Skills.objects.filter(name__icontains=search_query)

    profile = Profiles.objects.distinct().filter(Q(name__icontains=search_query) |
    Q(short_intro__icontains=search_query) |
    Q(skills__in=skills))

    return profile,search_query



