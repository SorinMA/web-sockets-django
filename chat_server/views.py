
"""
def room(request, roomName, userName):
    return render(request, 'chat_server/room_page.html', {
        'room_name_json': mark_safe(json.dumps(roomName)),
        'user_name_json': mark_safe(json.dumps(userName))
    }) """

# chat/views.py
from django.shortcuts import render
from django.utils.safestring import mark_safe
from django.http import HttpResponse
import json

allUsers = []

def index(request):
    return render(request, 'chat_server/index.html', {'errMsg': ''})

def room(request, room_name, user_name):
    if user_name + room_name in allUsers:
        return render(request, 'chat_server/index.html', {'errMsg': 'this username is aleardy used in this chat room'})
    else:
        try:
            print("|"+ user_name + room_name + "|")
            allUsers.append(user_name + room_name)
        except:
            return render(request, 'chat_server/index.html',
                          {'errMsg': 'Server is full'})
        return render(request, 'chat_server/room_page.html', {
            'room_name_json': mark_safe(json.dumps(room_name)),
            'user_name_json': mark_safe(json.dumps(user_name))
        })

def room_disconnect(request):
    print("DISCONEEEECT")
    if request.method == 'POST':
        body_unicode = request.body.decode('utf-8')
        body = json.loads(body_unicode)
        print("|" + body['user_name'] + body['room_name'] + "|------")
        try:
            print("|" + body['user_name'] + body['room_name'] + "|------")
            allUsers.remove(body['user_name'] + body['room_name'])
        except:
            return HttpResponse("Not ok!")
    return HttpResponse("OK!")
