from django.utils import timezone
from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import auth, messages
from django.template import RequestContext
from .forms import LoginForm, RegistrationForm
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
            user.date_of_birth = timezone.now()
            user.save()
            messages.success(request, 'Sign in has successed!!!!')
            return HttpResponseRedirect(
                reverse(login))
    else:
        form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})


def about(request):
    return HttpResponse('this is a about page.')
