from o2.models import User, ContactInfo, Log, Comment, Ticket, OmbudsmanOffice
from tastypie_mongoengine import fields as fields_mongo
from tastypie_mongoengine.resources import MongoEngineResource
from tastypie.resources import ALL, ALL_WITH_RELATIONS
from mongoengine.django.auth import Group

class LogResource(MongoEngineResource):
    class Meta:
        object_class = Log
        
class ContactInfoResource(MongoEngineResource):
    class Meta:
        object_class = ContactInfo
        
class CommentResource(MongoEngineResource):
    class Meta:
        object_class = Comment

class UsersResource(MongoEngineResource):    
    class Meta:
        queryset = User.objects(group = Group.objects.get(name = 'users'), is_active = True).all()
        allowed_methods = ['get']
        excludes = ['password', 'picture', 'contact_info']
        filtering = {
            'obj_id': ALL,
            'username': ALL,
            'email': ALL,
            'first_name': ALL,
            'last_name': ALL,
            'gender': ALL
        }
        
class TicketsResource(MongoEngineResource):
    belongs_to = fields_mongo.ReferenceField(to = 'o2.api.resources.OmbudsmanOfficeResource', attribute = 'belongs_to', full = True)
    created_by = fields_mongo.ReferenceField(to = 'o2.api.resources.UsersResource', attribute = 'created_by', full = True)
    comments = fields_mongo.EmbeddedListField(of = 'o2.api.resources.CommentResource', attribute = 'comments', full = False, null = True)
    log = fields_mongo.EmbeddedDocumentField(embedded = 'o2.api.resources.LogResource', attribute = 'log')
    
    class Meta:
        queryset = Ticket.objects.all()
        allowed_methods = ['get']
        filtering = {
            'obj_id': ALL,
            'title': ALL,
            'slug': ALL,
            'category': ALL,
            'belongs_to': ALL_WITH_RELATIONS,
            'created_by': ALL_WITH_RELATIONS
        }
        
class OmbudsmanOfficeResource(MongoEngineResource):
    admin = fields_mongo.ReferenceField(to = 'o2.api.resources.UsersResource', attribute = 'admin', full = True)
    ombudsman = fields_mongo.ReferencedListField(of = 'o2.api.resources.UsersResource', attribute = 'ombudsman', full = False, null = True)
    users = fields_mongo.ReferencedListField(of = 'o2.api.resources.UsersResource', attribute = 'users', full = False, null = True)
    log = fields_mongo.EmbeddedDocumentField(embedded = 'o2.api.resources.LogResource', attribute = 'log')
    
    class Meta:
        queryset = OmbudsmanOffice.objects.all()
        allowed_methods = ['get']
        excludes = ['picture', 'credits']
        filtering = {
            'obj_id': ALL,
            'name': ALL,
            'slug': ALL,
            'type': ALL,
            'admin': ALL_WITH_RELATIONS,
            'ombudsman': ALL_WITH_RELATIONS,
            'users': ALL_WITH_RELATIONS
        }