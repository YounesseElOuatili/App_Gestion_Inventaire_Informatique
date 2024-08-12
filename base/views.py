from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.views.generic.edit import FormView

@login_required(login_url='/login/')
def Dashboard(request):
    return render(request, 'dashboard.html')

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/login/')


class LoginView(FormView):

    authentication_form = None
    template_name = "registration/login.html"
    redirect_authenticated_user = False
    extra_context = None


def profile_view(request):
    # Assurez-vous que le modèle 'profile.html' existe
    return render(request, 'dashboard.html')