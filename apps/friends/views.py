from django.shortcuts import render, redirect
from . import models
from django.contrib import messages
from .models import User

# Create your views here.
def current_user(request):
    if 'user_id' in request.session:
        return User.objects.get(id=request.session['user_id'])

def index(request):
    return render(request, 'friends/index.html')

# def main(request):
#     return render(request, 'friends/index.html')

def register(request):
    if request.method == 'POST':
        result = User.objects.validate_registration(request.POST)
        if result['status'] == False:
            #create flash messages
            for error in result['errors']:
                messages.error(request, error)

            #redirect to home page
            return redirect('/')
        else:
            #put the user_id into session
            request.session['user_id'] = result['user'].id
            return redirect('/friends')


def authenticate(request):
    if request.method == 'POST':
        result = User.objects.validate_login(request.POST)
        if result['status'] == False:
            #generate error message
            messages.error(request, result['error'] )
            return redirect('/')
        else:
            #save the user_id into session
            request.session['user_id'] = result['user'].id
            return redirect('/friends')

def friends(request):
    user = User.objects.get(id=request.session['user_id'])
    friends = []
    not_friends = []
    all_other_users = User.objects.exclude(id=request.session['user_id'])
    for other_user in all_other_users:
        if other_user in user.friends.all():
            friends.append(other_user)
        elif other_user not in user.friends.all():
            not_friends.append(other_user)
    context = {
        'current_user' : current_user(request),
        'friends' : friends,
        'not_friends' : not_friends
    }
    return render(request, 'friends/friend.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def user(request, id):
    user = User.objects.get(id=id)
    context = {
    'user' : user
    }
    return render(request, 'friends/user.html', context)

def add(request, id):
    user = User.objects.get(id=request.session['user_id'])
    new_friend = User.objects.get(id=id)
    user.friends.add(new_friend)
    return redirect('/friends')

def remove(request, id):
    user = User.objects.get(id=request.session['user_id'])
    unfriend = User.objects.get(id=id)
    user.friends.remove(unfriend)
    return redirect('/friends')
