from django.views.generic import DetailView, UpdateView, CreateView
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http.response import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from .models import Message, UserProfile, Room, Room_message
from .serializers import MessageSerializer, UserSerializer, RoomSerializer
from django.contrib.auth.decorators import login_required


def index(request):
    if request.user.is_authenticated:
        return redirect('chats')
    if request.method == 'GET':
        return render(request, 'index.html', {})
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
        else:
            return HttpResponse('{"error": "Вы не зарегистрированы"}')
        return redirect('chats')


@csrf_exempt
def user_list(request, pk=None):

    if request.method == 'GET':
        if pk:
            users = User.objects.filter(id=pk)
        else:
            users = User.objects.all()
        serializer = UserSerializer(users, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            user = User.objects.create_user(username=data['username'], password=data['password'])
            UserProfile.objects.create(user=user)
            user.save()
            return JsonResponse(data, status=201)
        except Exception:
            return JsonResponse({'error': "Что-то пошло не по плану"}, status=400)


@login_required
def update_me(request, pk):
    data = JSONParser().parse(request)
    userprofile = UserProfile.objects.get(id=pk)
    user = User.objects.get(id=pk)
    try:
        user.update(username=data['username'])
        userprofile.update(user=user)
        user.save()
        return JsonResponse(data, status=201)
    except Exception:
        return JsonResponse({'error': "Что-то пошло не по плану"}, status=400)


@csrf_exempt
def room_list(request, pk=None):

    if request.method == 'GET':
        if pk:
            rooms = Room.objects.filter(id=pk)
        else:
            rooms = Room.objects.all()
        serializer = RoomSerializer(rooms, many=True, context={'request': request})
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        try:
            Room.objects.create(room_name=data['room_name'])
            return JsonResponse(data, status=201)
        except Exception:
            return JsonResponse({'error': "Что-то пошло не по плану"}, status=400)


def room(request, pk):
    
    return render(request, 'room.html', {
        'id_roomname': pk
    })

@csrf_exempt
def message_list(request, sender=None, receiver=None):

    if request.method == 'GET':
        messages = Message.objects.filter(sender_id=sender, receiver_id=receiver, is_read=False)
        serializer = MessageSerializer(messages, many=True, context={'request': request})
        for message in messages:
            message.is_read = True
            message.save()
        return JsonResponse(serializer.data, safe=False)

    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=201)
        return JsonResponse(serializer.errors, status=400)


def register_view(request):

    if request.user.is_authenticated:
        return redirect('chats')
    return render(request, 'register.html', {})


def roomcreate_view(request):

    return render(request, 'room_create.html', {})


def about_view(request, pk):
    if request.method == 'POST':
        data = JSONParser().parse(request)
        userprofile = UserProfile.objects.get(id=pk)
        user = User.objects.get(id=pk)
        try:
            user.update(username=data['username'])
            userprofile.update(user=user)
            user.save()
            return JsonResponse(data, status=201)
        except Exception:
            return JsonResponse({'error': "Что-то пошло не по плану"}, status=400)
    return render(request, 'about.html', {'id_user': pk})


def chat_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, 'chat.html',
                      {'users': User.objects.exclude(username=request.user.username)})


def message_view(request, sender, receiver):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, "messages.html",
                      {'users': User.objects.exclude(username=request.user.username),
                       'receiver': User.objects.get(id=receiver),
                       'messages': Message.objects.filter(sender_id=sender, receiver_id=receiver) |
                                   Message.objects.filter(sender_id=receiver, receiver_id=sender)})


def rooms_view(request):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, 'rooms.html',
                      {'rooms': Room.objects.all()})


def room_message_view(request, sender, pk):
    if not request.user.is_authenticated:
        return redirect('index')
    if request.method == "GET":
        return render(request, "room_messages.html",
                      {'users': User.objects.exclude(username=request.user.username),
                       'receiver': Room_message.objects.get(id=pk),
                       'messages': Room_message.objects.filter(send_id=sender, room_id=pk) |
                                   Room_message.objects.filter(send_id=pk, room_id=sender)})


@login_required
def subscribe_me(request, pk):
    user = request.user
    room = Room.objects.get(id=pk)
    if room not in user.room_set.all():
        room.participants.add(user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))


@login_required
def unsubscribe_me(request, pk):
    user = request.user
    room = Room.objects.get(id=pk)
    if room in user.room_set.all():
        room.participants.add(user)
        return redirect(request.META.get('HTTP_REFERER'))
    else:
        return redirect(request.META.get('HTTP_REFERER'))
