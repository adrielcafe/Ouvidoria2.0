# -*- coding: utf-8 -*-
from django.http.response import HttpResponse
from django.utils import simplejson
from o2.models import OmbudsmanOffice, User
from mongoengine.django.auth import make_password

def user_username(request):
    value = request.GET['value']
    obj = None
    
    try:
        obj = User.objects.get(username = value)
    except: 
        pass
    
    if obj and request.user and obj.id == request.user.id:
        valid = 1
    elif obj:
        valid = 0
    else:
        valid = 1
    
    response = {
        'value': value, 
        'valid': valid, 
        'message': 'Nome de usuário já existe'
    }
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')

def user_email(request):
    value = request.GET['value']
    obj = None
    
    try:
        obj = User.objects.get(email = value)
    except: 
        pass
    
    if obj and request.user and obj.id == request.user.id:
        valid = 1
    elif obj:
        valid = 0
    else:
        valid = 1
        
    response = {
        'value': value, 
        'valid': valid, 
        'message': 'Email já está cadastrado'
    }
    return HttpResponse(simplejson.dumps(response), mimetype='application/json')