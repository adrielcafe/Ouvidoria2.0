# -*- coding: utf-8 -*-
from o2.models import User, OmbudsmanOffice, Ticket, ContactInfo, Log, Comment
from django.shortcuts import render
from django.template.context import Context
from django.http.response import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from mongoengine.django.shortcuts import get_document_or_404
from django.utils.datetime_safe import datetime
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from urllib2 import urlopen
from StringIO import StringIO
from o2.util import calculate_age, SubscribeUserInOmbudsmanOffice,\
    UnsubscribeUserInOmbudsmanOffice
from o2.settings import STATIC_URL, FIWARE_AUTH_USERNAME, FIWARE_AUTH_PASSWORD
from mongoengine.django.auth import make_password, Group, check_password
from slugify import slugify
from django.utils import simplejson
from django.conf import settings
from mongoengine.context_managers import no_dereference
from PIL import Image
from o2.cdmi import create_container, authentication_request, list_container,\
    store_text, check_capabilities, delete_container

def handler404(request):
    return render(request, '404.html', {}, status = 404)

def index(request):
    auth_reponse = authentication_request(FIWARE_AUTH_USERNAME, FIWARE_AUTH_PASSWORD)
    token = auth_reponse['access']['token']['id']
    for i in auth_reponse['access']['serviceCatalog']:
        if i['name'] == 'swift':
            auth_url = i['endpoints'][0]['publicURL']
            break
    auth = auth_url[auth_url.find("AUTH_"):]

    #container = list_container(token, auth, 'UsersPicture')
    #text = store_text(token, auth, 'o2', 'text1', 'teste 1')
    #print container
    
    context = Context({'current_page': 'index'});
    return render(request, 'index.html', context)
    
def users(request):
    context = Context({'page_title': 'Pessoas', 'current_page': 'users'});
    return render(request, 'users.html', context)

def user_login(request):
    if request.user.is_authenticated():
        if request.user.group.name == 'ombudsman':
            slug = OmbudsmanOffice.objects.get(admin = request.user.to_dbref()).slug
            return HttpResponseRedirect('/ombudsman/{0}'.format(slug))
        else:
            return HttpResponseRedirect('/user/{0}'.format(request.user.username))
    elif 'username' in request.POST and 'password' in request.POST:
        user = authenticate(username = request.POST['username'], password = request.POST['password'])
        if user and user.is_active:
            if user.group.name == 'ombudsman':
                user.ombudsman = OmbudsmanOffice.objects.get(admin = user.to_dbref())
            login(request, user)
            response = {
                'valid': 1, 
                'url': '/ombudsman/{0}'.format(user.ombudsman.slug) if request.user.group.name == 'ombudsman' else '/user/{0}'.format(user.username)
            }
            return HttpResponse(simplejson.dumps(response), mimetype='application/json')
        else:
            response = {
                'valid': 0, 
                'message': 'Usuário e/ou senha incorreto'
            }
            return HttpResponse(simplejson.dumps(response), mimetype='application/json')
        
    context = Context({'page_title': 'Entrar'})
    return render(request, 'login.html', context)

@login_required
def user_edit(request):
    if not request.user.group.name == 'users':
        raise Http404
    
    if request.method == 'POST':
        p = request.FILES if 'picture' in request.FILES else request.POST
        
        if 'current-password' in p:
            '''if request.user.check_password(p['current-password']):
                User.objects(id = request.user.id).update_one(
                    set__password = make_password(p['new-password'])
                )
                return HttpResponse('ok')
            else:                
                return HttpResponse('error')'''
            pass
        elif 'picture' in p:            
            file = StringIO()
            img = Image.open(StringIO(p['picture'].read()))
            img = img.resize((200, 200))
            img.save(file, 'JPEG', quality = 90)
            file.seek(0)
            
            path = default_storage.save('users/{0}.jpg'.format(request.user.username), ContentFile(file.read()))

            User.objects(id = request.user.id).update_one(
                set__picture = '/media/{0}'.format(path)
            )
        elif 'email' in p:
            User.objects(id = request.user.id).update_one(
                set__first_name = p['first-name'],
                set__last_name = p['last-name'],
                set__email = p['email'],
                set__birth_date = datetime.strptime(p['birth-date'], '%d/%m/%Y') if p['birth-date'] else None,
                set__gender = p['gender'],
                set__about = p['about'],
                set__contact_info__website = p['contact-info-website'],
                set__contact_info__country = p['contact-info-country'],
                set__contact_info__state = p['contact-info-state'],
                set__contact_info__city = p['contact-info-city']
            )
            if not request.user.group:
                User.objects(id = request.user.id).update_one(
                    set__group = Group.objects.get(name = 'users')
                )
            return HttpResponseRedirect('/user/{0}'.format(request.user.username))
        
    context = Context({'page_title': 'Editar Perfil', 'current_page': 'users'});
    return render(request, 'user_edit.html', context)

def user_view(request, username):    
    obj = get_document_or_404(User, username = username, group = Group.objects.get(name = 'users'), is_active = True)
    obj.ombudsman_user = OmbudsmanOffice.objects(users__contains = obj.to_dbref())
    obj.ombudsman_admin = OmbudsmanOffice.objects(admin = obj.to_dbref())
    obj.ombudsman_ombudsman = OmbudsmanOffice.objects(ombudsman__contains = obj.to_dbref())
    if obj.about:
        obj.about = obj.about.replace('\r\n', '<br>')
    if obj.birth_date:
        obj.age = calculate_age(obj.birth_date)
    context = Context({'page_title': u'{0} {1}'.format(obj.first_name, obj.last_name), 'current_page': 'users', 'obj': obj});
    return render(request, 'user_view.html', context)

def user_profile(request):
    if request.user.is_authenticated():
        return user_view(request, request.user.username)
    else:
        return HttpResponseRedirect('/')
    
def user_picture(request, username):
    path = get_document_or_404(User, username = username).picture
    if not path:
        path = '{0}img/user-avatar.jpg'.format(STATIC_URL)
    url = 'http://{0}{1}'.format(request.META['HTTP_HOST'], path)
    #return HttpResponse(urlopen(url).read(), mimetype="image/jpg")
    return HttpResponseRedirect(url)

def ombudsman(request):
    context = Context({'page_title': 'Ouvidorias', 'current_page': 'ombudsman'});
    return render(request, 'ombudsman.html', context)

def ombudsman_new(request):
    if request.user.is_authenticated() and request.user.group.name == 'ombudsman':    
        return HttpResponseRedirect('/')
    if request.method == 'POST':
        p = request.POST

        if 'picture' in request.FILES:
            file = StringIO()
            img = Image.open(StringIO(request.FILES['picture'].read()))
            img = img.resize((200, 200))
            img.save(file, 'JPEG', quality = 90)
            file.seek(0)
            img_path = default_storage.save('ombudsman/{0}.jpg'.format(p['username']), ContentFile(file.read()))
            img_path = '/media/{0}'.format(img_path)
        else:
            img_path = ''
        
        ombudsman = OmbudsmanOffice()
        ombudsman.name = p['name']
        ombudsman.slug = ''
        ombudsman.about = p['about']
        ombudsman.categories = p['categories'].split(',')
        ombudsman.type = p['type']
        ombudsman.credits = 100
        ombudsman.picture = img_path
        ombudsman.contact_info = ContactInfo()
        ombudsman.contact_info.country = p['contact-info-country']
        ombudsman.contact_info.state = p['contact-info-state']
        ombudsman.contact_info.city = p['contact-info-city']
        ombudsman.contact_info.address = p['contact-info-address']
        ombudsman.contact_info.website = p['contact-info-website']
        ombudsman.contact_info.phones = [p['contact-info-phone-1'], p['contact-info-phone-2']]
        ombudsman.users = []
        ombudsman.ombudsman = []
        ombudsman.log = Log()
        ombudsman.save()
            
        user = User()
        user.username = p['username']
        user.password = make_password(p['password'])
        user.email = p['email']
        user.group = Group.objects.get(name = 'ombudsman')
        user.save()

        slug = slugify('{0}-{1}'.format(ombudsman.name, ombudsman.obj_id))
        
        ombudsman.update(
            set__slug = slug,
            set__admin = user.to_dbref()
        )
        
        return HttpResponseRedirect('/ombudsman/{0}'.format(slug))
    
    context = Context({'page_title': 'Nova Ouvidoria', 'current_page': 'ombudsman'});
    return render(request, 'ombudsman_new.html', context)

@login_required
def ombudsman_edit(request):
    if not request.user.group.name == 'ombudsman':
        raise Http404
    
    if request.method == 'POST':
        p = request.FILES if 'picture' in request.FILES else request.POST
        
        if 'action' in p and p['action'] == 'add_ombudsman':
            user = User.objects.get(username = p['username'])
            OmbudsmanOffice.objects(admin = request.user.to_dbref()).update_one(add_to_set__ombudsman = user)
            response = {'valid': 1}
            return HttpResponse(simplejson.dumps(response), mimetype='application/json')
        elif 'action' in p and p['action'] == 'remove_ombudsman':
            user = User.objects.get(username = p['username'])
            OmbudsmanOffice.objects(admin = request.user.to_dbref()).update_one(pull__ombudsman = user)
            response = {'valid': 1}
            return HttpResponse(simplejson.dumps(response), mimetype='application/json')
        elif set(['current-password', 'new-password']).issubset(p):
            if request.user.check_password(p['current-password']):
                User.objects(id = request.user.id).update_one(
                    set__password = make_password(p['new-password'])
                )
                response = {'valid': 1}
                return HttpResponse(simplejson.dumps(response), mimetype='application/json')
            else:
                response = {
                    'valid': 0, 
                    'message': 'Senha atual incorreta'
                }
                return HttpResponse(simplejson.dumps(response), mimetype='application/json')
            pass
        elif 'picture' in p:            
            file = StringIO()
            img = Image.open(StringIO(p['picture'].read()))
            img = img.resize((200, 200))
            img.save(file, 'JPEG', quality = 90)
            file.seek(0)
            
            path = default_storage.save('ombudsman/{0}.jpg'.format(request.user.username), ContentFile(file.read()))

            Ombudsman.objects(admin = request.user.to_dbref()).update_one(
                set__picture = '/media/{0}'.format(path),
                set__log__updated_in = datetime.now()
            )
        elif set(['name', 'type', 'categories']).issubset(p):
            ombudsman = OmbudsmanOffice.objects(admin = request.user.to_dbref()).fields('obj_id').limit(1)[0]
            slug = slugify('{0}-{1}'.format(p['name'], ombudsman.obj_id))
            OmbudsmanOffice.objects(admin = request.user.to_dbref()).update_one(
                set__name = p['name'],
                set__slug = slug,
                set__about = p['about'],
                set__categories = p['categories'].split(','),
                set__type = p['type'],
                set__contact_info__country = p['contact-info-country'],
                set__contact_info__state = p['contact-info-state'],
                set__contact_info__city = p['contact-info-city'],
                set__contact_info__address = p['contact-info-address'],
                set__contact_info__website = p['contact-info-website'],
                set__contact_info__phones = [p['contact-info-phone-1'], p['contact-info-phone-2']],
                set__log__updated_in = datetime.now()
            )
            User.objects(id = request.user.id).update_one(
                set__email = p['email']
            )
            if not request.user.group:
                User.objects(id = request.user.id).update_one(
                    set__group = Group.objects.get(name = 'ombudsman')
                )
            return HttpResponseRedirect('/ombudsman/{0}'.format(slug))
    
    obj = get_document_or_404(OmbudsmanOffice, admin = request.user.to_dbref())
    context = Context({'page_title': 'Editar Ouvidoria', 'current_page': 'ombudsman', 'ombudsman': obj});
    return render(request, 'ombudsman_edit.html', context)

def ombudsman_view(request, slug):
    if request.method == 'POST' and request.user.is_authenticated() and request.user.group.name == 'users':
        p = request.POST
        ombudsman = OmbudsmanOffice.objects(slug = slug).fields('users').limit(1)[0]
        if 'action' in p and p['action'] == 'join':
            SubscribeUserInOmbudsmanOffice(slug, request.user.to_dbref())
        elif 'action' in p and p['action'] == 'unjoin':
            UnsubscribeUserInOmbudsmanOffice(slug, request.user.to_dbref())
        elif set(['title', 'description', 'category']).issubset(p):
            ticket = Ticket()
            ticket.title = p['title']
            ticket.slug = ''
            ticket.description = p['description']
            ticket.category = p['category']
            ticket.belongs_to = ombudsman.to_dbref()
            ticket.created_by = request.user.to_dbref()
            ticket.comments = []
            ticket.log = Log()
            ticket.save()
            
            ticket_slug = slugify('{0}-{1}'.format(ticket.title, ticket.obj_id))
        
            ticket.update(
                set__slug = ticket_slug
            )
            
            return HttpResponseRedirect('/ombudsman/{0}/ticket/{1}'.format(ombudsman.slug, ticket_slug)) 
            
    with no_dereference(OmbudsmanOffice) as OmbudsmanOffice_all:
        obj = get_document_or_404(OmbudsmanOffice_all, slug = slug)
    obj.total_tickets = len(Ticket.objects(belongs_to = obj.id))
    obj.total_users = len(obj.users)
    if obj.about:
        obj.about = obj.about.replace('\r\n', '<br>')
    context = Context({'page_title': obj.name, 'current_page': 'ombudsman', 'obj': obj});
    return render(request, 'ombudsman_view.html', context)

def ombudsman_picture(request, slug):
    path = get_document_or_404(OmbudsmanOffice, slug = slug).picture
    if not path:
        path = '{0}img/ombudsman-avatar.jpg'.format(STATIC_URL)
    url = 'http://{0}{1}'.format(request.META['HTTP_HOST'], path)
    #return HttpResponse(urlopen(url).read(), mimetype="image/jpg")
    return HttpResponseRedirect(url)

def ticket_view(request, ombudsman_slug, ticket_slug):
    if request.method == 'POST' and request.user.is_authenticated():
        p = request.POST
        comment = Comment()
        comment.text = p['comment'].replace('\r\n', '<br>')
        comment.created_by = request.user.to_dbref()
        comment.created_in = datetime.now()
    
        Ticket.objects(slug = ticket_slug).update_one(push__comments = comment)
        
    with no_dereference(Ticket) as Ticket_all:
        obj = get_document_or_404(Ticket_all, slug = ticket_slug)
    obj.description = obj.description.replace('\r\n', '<br>')
    
    context = Context({'page_title': obj.title, 'current_page': 'ombudsman', 'obj': obj});
    return render(request, 'ticket_view.html', context)

def about(request):
    context = Context({'page_title': 'Sobre', 'current_page': 'about'});
    return render(request, 'about.html', context)

def helpme(request):
    context = Context({'page_title': 'Ajuda'});
    return render(request, 'help.html', context)

def faq(request):
    context = Context({'page_title': 'FAQ'});
    return render(request, 'faq.html', context)

def contact(request):
    context = Context({'page_title': 'Contato'});
    return render(request, 'contact.html', context)