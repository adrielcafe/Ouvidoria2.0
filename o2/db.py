# -*- coding: utf-8 -*-
from mongoengine import connect, register_connection
from o2.models import User, ContactInfo, Log, Ombudsman, Called,\
    Comment
from mongoengine.django.auth import make_password
from django.utils.datetime_safe import datetime
from random import randint
from slugify import slugify

def drop_all():
    User.drop_collection()
    Called.drop_collection()
    Ombudsman.drop_collection()
    
def register_dummy():
    '''
    for i in range(100):
        try:
            user = User()
            user.username = 'user' + str(i)
            user.password = make_password('123456')
            user.email = 'user{0}@users.com'.format(i)
            user.first_name = 'first' + str(i)
            user.last_name = 'last' + str(i)
            user.about = 'about ' + str(i)
            user.sex = 'M' if i % 2 == 0 else 'F'
            user.birth_date = datetime.now()
            user.picture.put('E:\\Documentos\\Downloads\\avatar.jpg')
            user.contact_info = ContactInfo()
            user.contact_info.country = 'Brasil'
            user.contact_info.state = 'PE'
            user.contact_info.city = 'Recife'
            user.contact_info.phones = ['8111223344']
            user.log = Log()
            user.log.created_in = datetime.now()
            user.log.updated_in = datetime.now()
            user.save()
        except:
            pass
     
    for i in range(50):
        ombudsman = Ombudsman()
        try:
            ombudsman.name = 'Ouvidoria ' + str(i)
            ombudsman.slug = ''
            ombudsman.description = 'Description ' + str(i)
            ombudsman.categories = ['Categoria 1', 'Categoria 2', 'Categoria 3']
            ombudsman.picture.put('E:\\Documentos\\Downloads\\megaphone.jpg')
            ombudsman.admin = User.objects.get(obj_id = randint(1, 99)).to_dbref()
            ombudsman.moderators = [User.objects.get(obj_id = randint(1, 99)).to_dbref(), User.objects.get(obj_id = randint(1, 99)).to_dbref()]
            ombudsman.users = [User.objects.get(obj_id = randint(1, 99)).to_dbref(), User.objects.get(obj_id = randint(1, 99)).to_dbref(), User.objects.get(obj_id = randint(1, 99)).to_dbref()]
            ombudsman.institution_name = 'Institution ' + str(i)
            ombudsman.institution_email = 'institution{0}@institutions.com'.format(i)
            ombudsman.institution_about = 'About ' + str(i)
            ombudsman.institution_type = 'Privado' if randint(0, 99) % 2 == 0 else u'Público'
            ombudsman.contact_info = ContactInfo()
            ombudsman.contact_info.country = 'Brasil'
            ombudsman.contact_info.state = 'PE'
            ombudsman.contact_info.city = 'Recife'
            ombudsman.contact_info.address = 'Rua A, nº 123 - CEP: 12345-678'
            ombudsman.contact_info.website = 'http://site.com'
            ombudsman.contact_info.phones = ['8144332211', '8155667788']
            ombudsman.log = Log()
            ombudsman.log.created_in = datetime.now()
            ombudsman.log.updated_in = datetime.now()
            ombudsman.save()
            ombudsman.update(set__slug = slugify('{0}-{1}'.format(ombudsman.name, ombudsman.obj_id)))
        except:
            pass
        
        for j in range(5):
            try:
                called = Called()
                called.title = 'Chamado'
                called.slug = ''
                called.description = 'Description ' + str(j)
                called.category = ombudsman.categories[randint(0, 2)]
                called.belongs_to = ombudsman.to_dbref()
                called.created_by = ombudsman.users[randint(0, 2)].to_dbref()
                called.comments = []
                for l in range(3):
                    comment = Comment()
                    comment.text = 'Comentário ' + str(l)
                    comment.created_by = ombudsman.users[randint(0, 2)].to_dbref()
                    comment.created_in = datetime.now()
                    called.comments.append(comment) 
                called.log = Log()
                called.log.created_in = datetime.now()
                called.log.updated_in = datetime.now()
                called.save()
                called.update(set__slug = slugify('{0}-{1}'.format(called.title, called.obj_id)))
            except:
                pass
    '''