from .models import Profiles, Skills
from django.db.models import Q



def searchProfiles(request):

    search_query = ''

    if request.GET.get('search_query'):
        search_query = request.GET.get('search_query')   

    skills = Skills.objects.filter(name__icontains=search_query)

    profile = Profiles.objects.distinct().filter(Q(name__icontains=search_query) |
    Q(short_intro__icontains=search_query) |
    Q(skills__in=skills))

    return profile,search_query