from django.shortcuts import render, render_to_response,\
    get_object_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required
from django.template import RequestContext
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import User, Post
from .forms import LoginForm, RegistrationForm, EditProfileForm,\
    PostForm
# Create your views here.

PER_PAGE = 10  # per_page Paginator


def index(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = Post.objects.create(
                body=form.cleaned_data['body'],
                author=request.user)
            post.save()
            return HttpResponseRedirect(reverse('main:index'))
    form = PostForm()

    page = request.GET.get('page')
    paginator = Paginator(Post.objects.order_by('-timestamp'), PER_PAGE)
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'main/index.html',
                  {'form': form, 'posts': posts})


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
            return redirect(reverse('main:index'))
    else:
        form = RegistrationForm()
    return render(request, 'main/register.html', {'form': form})


@login_required(login_url='/login/')
def about(request):
    return HttpResponse('this is a about page.')


def logout_view(request):
    auth.logout(request)
    return render_to_response('main/index.html')


@login_required(login_url='/login/')
def user(request, username):
    try:
        user = User.objects.filter(username=username).first()
    except (KeyError, User.DoesNotExist):
        messages.error(request, 'This user does not exist!')
        return render(request, 'main/index.html')
    else:
        posts = user.post.order_by('-timestamp')
        return render(request, 'main/user.html',
                      {'user': user,
                       'gravatar': user.gravatar(size=256),
                       'posts': posts})


@login_required(login_url='/login/')
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST)
        if form.is_valid():
            request.user.realname = form.cleaned_data['realname']
            request.user.location = form.cleaned_data['location']
            request.user.about_me = form.cleaned_data['about_me']
            request.user.save()
            return HttpResponseRedirect(
                reverse('main:user', args=[request.user.username]))
    else:
        form = EditProfileForm()
    return render(request, 'main/edit_profile.html', {'form': form})


def post(request, id):
    post = get_object_or_404(Post, pk=id)
    return render(request, 'main/post.html', {'posts': [post]})


@login_required(login_url='/login/')
def follow(request, username):
    user = User.objects.filter(username=username).first()
    if request.user.is_following(user):
        messages.error(request, 'You are already following this user.')
        return redirect(reverse('main:user', kwargs={'username': username}))
    request.user.follow(user)
    messages.success(request, 'You are now following %s' % username)
    return redirect(reverse('main:user', kwargs={'username': username}))


@login_required(login_url='/login/')
def unfollow(request, username):
    user = User.objects.filter(username=username).first()
    request.user.unfollow(user)
    return redirect(reverse('main:user', kwargs={'username': username}))


@login_required(login_url='/login/')
def followers(request, username):
    user = User.objects.filter(username=username).first()
    followers = user.follower.all()
    messages.success(request, 'You are now unfollowing %s' % username)
    return render(request, 'main/followers.html', {'followers': followers})
