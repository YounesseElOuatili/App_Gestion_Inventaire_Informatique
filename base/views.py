from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as auth_logout
from django.views.generic.edit import FormView

@login_required(login_url='/login/')
def Dashboard(request):
    
    return render(request, 'liste_prod.html')

def logout(request):
    auth_logout(request)
    return HttpResponseRedirect('/login/')


class LoginView(FormView):

    authentication_form = None
    template_name = "registration/login.html"
    redirect_authenticated_user = False
    extra_context = None







