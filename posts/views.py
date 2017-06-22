# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

# Create your views here.
#views.py
from posts.forms import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_protect
from django.shortcuts import render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext
from django.template.loader import get_template
from django.http import HttpResponse
from posts.models import Client, Project, Message
from django.contrib.auth.models import User

@csrf_protect
def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
            username=form.cleaned_data['username'],
            password=form.cleaned_data['password1'],
            email=form.cleaned_data['email'],
            )
            user.save()
            client = Client.objects.create(
            user=user,
            firstname=form.cleaned_data['firstname'],
            lastname=form.cleaned_data['lastname'],
            usertype=form.cleaned_data['usertype'],
            )
            return HttpResponseRedirect('/posts/register/success/')
    else:
        form = RegistrationForm()
    variables = {
    'form': form
    }
    template = get_template('registration/register.html')
    return HttpResponse(template.render(variables, request))

def register_success(request):
    template = get_template('registration/success.html')
    variables = {}
    return HttpResponse(template.render(variables, request))

def logout_page(request):
    logout(request)
    return HttpResponseRedirect('/posts/accounts/login/')

@login_required
def home(request):
    variables={
    'user': request.user
    }
    template = get_template('home.html')
    return HttpResponse(template.render(variables,request))

@csrf_protect
def create(request):
    user=request.user
    if request.method == 'POST':
        form = CreateForm(request.POST)
        if form.is_valid():
            project = Project.objects.create(
            user=user,
            projectname=form.cleaned_data['projectname'],
            description=form.cleaned_data['description'],
            value=form.cleaned_data['value'],
            )
            return HttpResponseRedirect('/posts/create/success/')
    else:
        form = CreateForm()
    variables = {
    'form': form
    }
    template = get_template('emprendedor/create.html')
    return HttpResponse(template.render(variables, request))

def create_success(request):
    template = get_template('emprendedor/success.html')
    variables = {}
    return HttpResponse(template.render(variables, request))

@csrf_protect
def show(request):
    user=request.user
    template = get_template('emprendedor/show.html')
    variables = {'projects':Project.objects.filter(user=user)}
    return HttpResponse(template.render(variables,request))

@csrf_protect
def project(request, project_id):
    template = get_template('emprendedor/project.html')
    variables = {'project':Project.objects.get(id=project_id)}
    return HttpResponse(template.render(variables,request))

@csrf_protect
def message(request, project_id):
    user=request.user
    project=Project.objects.get(id=project_id)
    userproxy=project.user
    if request.method == 'POST':
        recipient=User.objects.get(id=userproxy.id)
        form = MessageForm(request.POST)
        if form.is_valid():
            message = Message.objects.create(
            sender=user,
            recipient=recipient,
            project=project,
            title=form.cleaned_data['title'],
            message=form.cleaned_data['message'],
            )
            return HttpResponseRedirect('/posts/message/success/')
    else:
        form = MessageForm()
    variables={
    'form': form,
    'project':Project.objects.get(id=project_id),
    }
    template = get_template('emprendedor/message.html')
    return HttpResponse(template.render(variables, request))

def message_send(request):
    template = get_template('emprendedor/send.html')
    variables = {}
    return HttpResponse(template.render(variables, request))

@csrf_protect
def inbox(request):
    user=request.user
    template = get_template('emprendedor/inbox.html')
    variables = {'messages':Message.objects.filter(recipient=user)}
    return HttpResponse(template.render(variables,request))

@csrf_protect
def answer(request, message_id):
    user=request.user
    message=Message.objects.get(id=message_id)
    userproxy=message.sender
    projectproxy=message.project
    if request.method == 'POST':
        recipient=User.objects.get(id=userproxy.id)
        project=Project.objects.get(id=projectproxy.id)
        form = AnswerForm(request.POST)
        if form.is_valid():
            message = Message.objects.create(
            sender=user,
            recipient=recipient,
            project=project,
            title=message.title,
            message=form.cleaned_data['answer'],
            )
            return HttpResponseRedirect('/posts/message/success/')
    else:
        form = AnswerForm()
    variables={
    'form': form,
    'message':Message.objects.get(id=message_id),
    }
    template = get_template('emprendedor/answer.html')
    return HttpResponse(template.render(variables, request))
