from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.http import JsonResponse
from django.shortcuts import render, redirect
from .forms import LoginForm, CreateUserForm, PostForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.contrib import messages
from .models import Post
from .models import UserIpAddress
from django.contrib.auth.decorators import user_passes_test
from datetime import datetime
from datetime import timedelta


def signup(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created')
            return redirect('signin')
        else:
            messages.error(request, 'problem with credentials')
            form = CreateUserForm()
    return render(request, 'blog/signup.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('signin')


def signin(request):
    form = LoginForm(request.POST)
    users_ip = UserIpAddress.objects.order_by('id')
    if request.method == 'POST':

        form = LoginForm(request.POST or None)
        form.username = request.POST['username']
        form.password = request.POST['password']
        user = authenticate(
            request,
            username=form.username,
            password=form.password)
        if user is not None:
            login(request, user)
            client_ip = request.META['REMOTE_ADDR']
            for u in users_ip:
                if u.id == user.id:
                    return redirect('home')

            user_ip = UserIpAddress()
            user_ip.user = user
            user_ip.add_ip_address(client_ip)
            return redirect('home')
        else:
            form = LoginForm()
            messages.error(request, 'error with credentials')
            return render(request, 'blog/signin.html', {'form': form})
    else:
        return render(request, 'blog/signin.html', {'form': form})


@login_required(login_url='signin')
def home(request):
    user_ip = UserIpAddress.objects.order_by('id')
    client_ip = request.META['REMOTE_ADDR']
    for u in user_ip:
        if u.id == request.user.id:
            if u.address != client_ip:
                UserIpAddress.objects.filter(
                    user_id=request.user.id).update(
                    address=client_ip)
                messages.error(
                    request, 'you accessed with a different ip address')
                break

    posts = Post.objects.order_by('published_date')
    user_detail = request.user.is_superuser
    return render(request, 'blog/home.html',
                  {'posts': posts, 'permission': user_detail})


@login_required(login_url='signin')
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        form.title = request.POST['title']
        form.text = request.POST['text']

        if form.is_valid():
            phrase = form.text
            block = 'hack'
            if block in phrase:
                messages.error(request, 'hack is not allowed word')
            else:
                post = Post()
                post.user = request.user
                post.title = form.title 
                post.text = form.text
                post.publish()
                post.writeOnChain()
                post.save()
                return redirect('home')
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})


@login_required(login_url='signin')
@user_passes_test(lambda u: u.is_superuser, login_url='signin')
def table_posts(request):
    my_obj = []
    posts = Post.objects.order_by('id')
    users = User.objects.order_by('id')
    for u in users:
        test = {'id': u.id, 'user': u.username, 'post': 0}
        for p in posts:

            if p.user_id == u.id:
                test['post'] = test['post'] + 1
        my_obj.append(test)

    return render(request, 'blog/table_posts.html', {'posts': my_obj})


@login_required(login_url='signin')
def last_hour_post(request):
    response = []
    last_hour_post = []
    time_threshold = datetime.now(timezone.utc) - timedelta(hours=+1)
    posts = Post.objects.order_by('id')

    for p in posts:
        if p.created_date > time_threshold:
            last_hour_post.append(p)

    for post in last_hour_post:
        response.append(
            {
                'title': post.title,
                'created_date': post.created_date,
                'text': post.text,
                'author': post.user.username,
                'published_date': post.published_date,
            }
        )
    return JsonResponse(response, safe=False)


@login_required(login_url='signin')
def user_page(request, id):
    my_user = {
        'post': []
    }
    users = User.objects.order_by('id')
    posts = Post.objects.order_by('id')

    for u in users:
        if u.id == id:
            name = u.username
            email = u.email
            my_user['name'] = name
            my_user['email'] = email
            for p in posts:
                if p.user_id == u.id:
                    my_user['post'].append(p)
            break
        else:
            my_user['name'] = 'user not found'

    return render(request, 'blog/user_page.html', {'user': my_user})


@login_required(login_url='signin')
def find_word(request, word):
    count = 0
    response = {}
    posts = Post.objects.order_by('id')
    phrase = ''

    for post in posts:
        phrase = phrase + ' ' + post.text.lower()

    split_phrase = phrase.split()
    count = str(split_phrase.count(word.lower()))

    response['wordinphrase'] = count
    return JsonResponse(response, safe=False)
