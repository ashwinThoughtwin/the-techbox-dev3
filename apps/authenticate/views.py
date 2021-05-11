# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from .forms import LoginForm, SignUpForm
from django.views import View
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.utils.translation import gettext_lazy as _
from django.utils import translation


class LoginView(View):
    def get(self,request):
        form = LoginForm()
        if request.user.is_authenticated:
            return redirect('home')
        else:
            return render(request,'accounts/login.html',{'form':form})

    def post(self,request):
        form = LoginForm(request.POST or None)
        msg = None
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("home")
            else:    
                msg = 'Invalid credentials'    
        else:
            msg = 'Error validating the form'
        return render(request, "accounts/login.html", {"form": form, "msg" : msg})

class SignupView(View):
    def get(self,request):
        form = SignUpForm(request.POST)
        return render(request, "accounts/signup.html", {"form": form})

    def post(self,request):
        msg     = None
        success = False
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            raw_password = form.cleaned_data.get("password1")
            user = authenticate(username=username, password=raw_password)
            msg     = 'User created Success'
            success = True
        else:
            msg = 'Form is not valid'    
        return render(request, "accounts/signup.html", {"form": form, "msg" : msg, "success" : success })


def logout_request(request):
    logout(request)
    return redirect("login")




class SetLanguage(View):

    def post(self,request):
        cur_language = translation.get_language()
        lasturl = request.META.get('HTTP_REFERER')
        lang = request.POST['language']
        translation.activate(lang)
        request.session[translation.LANGUAGE_SESSION_KEY] = lang
        return  HttpResponseRedirect("/"+lang)

        