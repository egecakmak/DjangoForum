from django.core.exceptions import ValidationError
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
# from .models import Thread, Post, Message, MessageContainer
from .models import Thread, Post
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.core.validators import validate_email
import datetime


def index(request):
    threads = Thread.objects.all().order_by('update_date')
    context = {'threads': threads, 'threads_list': Thread.objects.all().order_by('update_date')}
    if 'login_failed' in request.session and request.session['login_failed'] is True:
        context['login_message'] = "Wrong username or password!"
        del request.session['login_failed']
    if request.user is not None:
        context['username'] = request.user.username
    else:
        context['username'] = ""
    return render(request, 'forum/index.html', context)


def users(request):
    users = User.objects.order_by('-id')
    context = {'users': users}
    return render(request, 'forum/users.html', context)


def signin(request):
    if request.method == 'POST':
        uname = request.POST['uname']
        psw = request.POST['psw']
        user = authenticate(username=uname, password=psw)
        if user is not None:
            login(request, user)
        else:
            request.session['login_failed'] = True
    return redirect('forum:index')


def signup(request):
    if request.user.is_authenticated:
        return redirect('forum:index')
    else:
        if request.method == 'POST':
            if request.POST.get("cancel_button"):
                return redirect('forum:index')
            else:
                context = {}
                requested_username = request.POST['requested_username']
                requested_password = request.POST['requested_password']
                requested_password_repeat = request.POST['requested_password_repeat']
                requested_email = request.POST['requested_email']
                try:
                    validate_email(requested_email)
                    if User.objects.filter(username=requested_username).exists():
                        context['error_message'] = "Requested username is already taken."
                        raise ValueError
                    if User.objects.filter(email=requested_email).exists():
                        context['error_message'] = "Given email is used by another user."
                        raise ValueError
                    if requested_password != requested_password_repeat:
                        context['error_message'] = "Passwords do not match."
                        raise ValueError
                    new_user = User.objects.create_user(requested_username, requested_email, requested_password)
                except ValueError as error:
                    return render(request, 'forum/signup.html', context)
                except ValidationError:
                    context['error_message'] = "Given email address is not valid."
                    return render(request, 'forum/signup.html', context)
                else:
                    requested_firstname = request.POST['requested_first_name']
                    requested_lastname = request.POST['requested_last_name']
                    new_user.first_name = requested_firstname
                    new_user.last_name = requested_lastname
                    new_user.save()
                    user = authenticate(username=requested_username, password=requested_password)
                    if user is not None:
                        login(request, user)
                    return redirect('forum:index')
        else:
            return render(request, 'forum/signup.html')


def start_thread(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            thread_title = request.POST['thread_title']
            thread_text = request.POST['thread_text']
            new_thread = Thread.objects.create(title=thread_title, pub_date=datetime.datetime.now(),
                                               update_date=datetime.datetime.now(),
                                               owner=request.user)
            new_post = Post.objects.create(post=thread_text, thread=new_thread, user=request.user,
                                           pub_date=datetime.datetime.now())
            new_thread.save()
            new_post.save()
            return redirect('forum:index')
        else:
            return render(request, 'forum/startThread.html')
    else:
        return redirect('forum:index')


def threads(request):
    return render(request, 'forum/threads.html', {'threads_list': Thread.objects.all().order_by('update_date')})


def thread(request, thread_id):
    if request.user.is_authenticated and request.method == "POST":
        comment = request.POST['post_text']
        thread_user = Thread.objects.all().get(id=thread_id)
        post = Post.objects.create(post=comment, thread=thread_user, user=request.user,
                                   pub_date=datetime.datetime.now())
        post.save()
    thread_to_return = Thread.objects.get(id=thread_id)
    posts_to_return = Post.objects.all().filter(thread=thread_to_return).order_by('pub_date')
    context = {'thread': thread_to_return, 'posts': posts_to_return}
    return render(request, 'forum/thread.html', context)


def delete_post(request, post_id, thread_id):
    post = Post.objects.all().filter(id=post_id)
    post.delete()
    return redirect('forum:thread', thread_id=thread_id)


def edit_post(request, post_id, thread_id):
    if request.method == "POST":
        post = Post.objects.all().filter(id=post_id)
        edited_text = request.POST['edit_text']
        post.update(post=edited_text)
    return redirect('forum:thread', thread_id=thread_id)

# def messages(request):
#     message_containers_1 = MessageContainer.objects.all().filter(side_1=request.user)
#     message_containers_2 = MessageContainer.objects.all().filter(side_2=request.user)
#     message_containers = message_containers_1.union(message_containers_2)
#     context = {'message_containers' : message_containers}
#     return render(request,'forum/messages.html',context)
#
# def conversations(request, message_container_id):
#     all_messages = Message.objects.all().filter(message_container=MessageContainer.objects.all().get(id=message_container_id)).order_by('pub_date')
#     context = {'all_messages' : all_messages}
#     return render(request,'forum/conversations.html', context)