from django.shortcuts import render
from .models import Profiles

# Create your views here.

def profiles(request):
    profile = Profiles.objects.all()
    contex = {'profile':profile}
    return render(request, 'users/profiles.html', contex)

def userProfile(request, pk):
    profile = Profiles.objects.get(id=pk)
    contex = {'profile':profile}
    return render(request, 'users/user-profile.html', contex)