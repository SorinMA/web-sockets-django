
"""
def room(request, roomName, userName):
    return render(request, 'chat_server/room_page.html', {
        'room_name_json': mark_safe(json.dumps(roomName)),
        'user_name_json': mark_safe(json.dumps(userName))
    }) """

# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
import json

def index(request):
    return render(request, 'chat_server/index.html', {})

def room(request, room_name):
    return render(request, 'chat_server/room_page.html', {
        'room_name_json': mark_safe(json.dumps(room_name))
    })