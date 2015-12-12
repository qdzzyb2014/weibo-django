from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from .models import User
from .forms import LoginForm, RegistrationForm, EditProfileForm
# Create your views here.


def index(request):
    return render(request, 'main/index.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = auth.authenticate(email=email, password=password)
        if user:
            if user.is_active:
                auth.login(request, user)
                messages.success(request, 'Welcome!!!!!!!!!!!!!!!!')
                # return HttpResponseRedirect(reverse(index))
                return render_to_response('main/index.html',
                                          context_instance=RequestContext(request))
        else:
            messages.error(request, 'Invalid username or password!')
    form = LoginForm()
    return render(request, 'main/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(request.POST.get('password'))
            user.save()
            messages.success(request, 'Sign in has successed!!!!')
            return HttpResponseRedirect(
                reverse(login))
    else:
        form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})


@login_required(login_url='/main/login/')
def about(request):
    return HttpResponse('this is a about page.')


def logout_view(request):
    auth.logout(request)
    return render_to_response('main/index.html')


@login_required(login_url='/main/login/')
def user(request, username):
    try:
        user = User.objects.filter(username=username).first()
    except (KeyError, User.DoesNotExist):
        messages.error(request, 'This user does not exist!')
        return render(request, 'main/index.html')
    else:
        return render(request, 'main/user.html',
                      {'user': user, 'gravatar': user.gravatar(size=256)})


@login_required(login_url='/main/login/')
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            user = form.save()
            return HttpResponseRedirect(
                reverse('main:user', args={'username': user.username}))
    else:
        form = EditProfileForm()
    return render(request, 'main/edit_profile.html', {'form': form})
