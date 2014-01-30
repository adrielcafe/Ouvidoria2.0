# -*- coding: utf-8 -*-
from mongoengine.django.auth import User, Group
from mongoengine.document import Document, EmbeddedDocument
from mongoengine.fields import StringField, SequenceField, DateTimeField,\
    ReferenceField, EmbeddedDocumentField, ListField, IntField
from django.utils.datetime_safe import datetime

class Log(EmbeddedDocument):
    created_in = DateTimeField(default=datetime.now);
    updated_in = DateTimeField(default=datetime.now);
    
class ContactInfo(EmbeddedDocument):
    country = StringField(max_length=80)
    state = StringField(max_length=80)
    city = StringField(max_length=80)
    address = StringField(max_length=80)
    website = StringField()
    phones = ListField(StringField(max_length=30))
    
class Comment(EmbeddedDocument):
    obj_id = SequenceField()
    text = StringField(max_length=2000, required=True)
    created_by = ReferenceField('User', dbref=True, required=True)
    created_in = DateTimeField(default=datetime.now);

class User(User):
    obj_id = SequenceField()
    about = StringField(max_length=500)
    gender = StringField(max_length=1)
    birth_date = DateTimeField()
    group = ReferenceField('mongoengine.django.auth.Group', dbref=True, default=Group.objects.get(name='users'))
    picture = StringField()
    contact_info = EmbeddedDocumentField(ContactInfo)
    
    meta = {
        'indexes': ['obj_id', 'username', 'email', 'first_name', 'last_name', 'gender', 'group'],
        'unique': True, 
        'sparse': True
    }

class Ticket(Document):
    obj_id = SequenceField()
    title = StringField(max_length=100, required=True)
    slug = StringField(unique=True, required=True)
    description = StringField(required=True)
    category = StringField(max_length=60, required=True)
    belongs_to = ReferenceField('OmbudsmanOffice', dbref=True, required=True)
    created_by = ReferenceField('User', dbref=True, required=True)
    comments = ListField(EmbeddedDocumentField(Comment))
    log = EmbeddedDocumentField(Log)
    
    meta = {
        'indexes': ['obj_id', 'title', 'slug', 'category', 'belongs_to', 'created_by']
    }
    
class OmbudsmanOffice(Document):
    obj_id = SequenceField()
    name = StringField(max_length=100, required=True)
    slug = StringField(unique=True, required=True)
    about = StringField(max_length=500, required=True)
    categories = ListField(StringField(max_length=60), default=['Geral'])
    type = StringField(max_length=60, required=True)
    credits = IntField()
    picture = StringField()
    admin = ReferenceField('User', dbref=True)
    ombudsman = ListField(ReferenceField('User', dbref=True))
    users = ListField(ReferenceField('User', dbref=True))
    contact_info = EmbeddedDocumentField(ContactInfo)
    log = EmbeddedDocumentField(Log)
    
    meta = {
        'indexes': ['obj_id', 'name', 'slug', 'type', 'admin', 'ombudsman', 'users', 'contact_info.country', 'contact_info.state', 'contact_info.city'],
        'unique': True, 
        'sparse': True
    }