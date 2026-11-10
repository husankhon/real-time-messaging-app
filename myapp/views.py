from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.text import slugify
from .models import ChatRoom, ChatMessage


def index(request):
    chat_rooms = ChatRoom.objects.all()
    return render(request, 'myapp/index.html', {
        'chat_rooms': chat_rooms
    })


def chatroom(request, slug):
    room = get_object_or_404(ChatRoom, slug=slug)
    messages = ChatMessage.objects.filter(room=room).select_related('user')[:50]
    return render(request, 'myapp/room.html', {
        'room': room,
        'messages': messages,
    })


@login_required(login_url='login')
def create_room(request):
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        if name:
            slug = slugify(name)
            # make slug unique if it already exists
            original_slug = slug
            counter = 1
            while ChatRoom.objects.filter(slug=slug).exists():
                slug = f'{original_slug}-{counter}'
                counter += 1
            room = ChatRoom.objects.create(name=name, slug=slug)
            return redirect('chatroom', slug=room.slug)
    return redirect('index')


def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'myapp/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            next_url = request.POST.get('next') or request.GET.get('next') or 'index'
            return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'myapp/login.html', {
        'form': form,
        'next': request.GET.get('next', ''),
    })


def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return redirect('index')
