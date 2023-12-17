# import urllib

from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.db.models import Q

from . import models
from . import forms


# Create your views here.

def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(f"{username}, {password}")
        try:
            User.objects.get(username=username)
        except ObjectDoesNotExist:
            messages.add_message(request, messages.ERROR, "User does not exist!")

        user = authenticate(request, username=username, password=password)
        print(user)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.add_message(request, messages.ERROR, "Password is wrong")

    context = {
    }
    return render(request, 'base/login_form.html', context)


def logout_page(request):
    logout(request)
    return redirect('home')


def register_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        user = None
        try:
            user = User.objects.get(username=username)
        except ObjectDoesNotExist:
            pass

        if user is not None:
            messages.add_message(request, messages.ERROR, "User Already exists!")
        else:
            if password2 == password1:
                r_user = User(username=username)
                r_user.set_password(password1)
                r_user.save()
                login(request, r_user)
                return redirect('home')
            else:
                messages.add_message(request, messages.ERROR, "Password fields don't match!")

    context = {}
    return render(request, 'base/login_register_form.html', context)


def home_page(request):
    q = request.GET.get('q') if request.GET.get('q') is not None else ''
    # q = urllib.parse.quote_plus(q)
    print(q)
    rooms = models.Room.objects.filter(
        Q(topic__name__icontains=q) |
        Q(host__username__iexact=q) |
        Q(name__icontains=q)
    ).order_by('-updated')
    topics = models.Topic.objects.all()
    topics_count = [(i.name, models.Room.objects.filter(topic=i.pk).count()) for i in topics]
    recent_activities = models.Message.objects.all().order_by("-updated")[:4]

    context = {
        'rooms': rooms,
        'topics': topics,
        'topics_count': sorted(topics_count, reverse=True, key=lambda x: x[1]),
        'recent_activities': recent_activities,
    }
    return render(request, 'base/home.html', context)


def room_page(request, pk):
    room = models.Room.objects.filter(pk=pk).first()
    room_messages = room.message_set.all().order_by('-updated')
    participants = room.participants.all()
    print(participants)

    if request.method == "POST":
        models.Message.objects.create(
            user=request.user,
            body=request.POST.get('msg'),
            room=room
        )
        room.participants.add(request.user)
        return redirect('room', pk=room.id)

    context = {
        'room': room,
        'room_messages': room_messages,
        'participants': participants,
    }
    return render(request, 'base/room.html', context)


@login_required(login_url='login')
def create_room(request):
    room_form = forms.RoomForm()
    if request.method == 'POST':
        form = forms.RoomForm(request.POST)
        if form.is_valid:
            room = form.save(commit=False)
            room.host = request.user
            room.save()
            return redirect("home")
    context = {
        'room_form': room_form,
    }
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def update_room(request, pk):
    room = models.Room.objects.get(id=pk)
    room_form = forms.RoomForm(instance=room)

    if request.method == 'POST':
        form = forms.RoomForm(request.POST, instance=room)
        if form.is_valid:
            form.save()
            return redirect("home")
    context = {'room_form': room_form}
    return render(request, 'base/room_form.html', context)


@login_required(login_url='login')
def delete_obj(request, pk):
    room = models.Room.objects.get(id=pk)

    if request.method == 'POST':
        room.delete()
        return redirect('home')

    return render(request, 'base/delete.html', {
        "obj": room
    })


def delete_message(request, pk):
    msg = models.Message.objects.get(id=pk)
    room_id = msg.room.pk
    msg.delete()
    return redirect('room', room_id)


def profile_page(request, pk):
    user = User.objects.get(pk=pk)
    rooms_count = user.rooms_host.all().count()
    host_rooms = user.rooms_host.all()
    msg_count = user.message_set.all().count()
    context = {
        'user': user,
        'rooms_count': rooms_count,
        'msg_count': msg_count,
        'host_rooms': host_rooms,
    }
    return render(request, 'base/profile.html', context)
