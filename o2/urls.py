# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from tastypie.api import Api
from o2.api.resources import UsersResource, TicketsResource, OmbudsmanOfficeResource
from django.conf import settings

o2_api = Api(api_name = 'v1')
o2_api.register(UsersResource())
o2_api.register(TicketsResource())
o2_api.register(OmbudsmanOfficeResource())

admin.autodiscover()

handler404 = 'o2.views.handler404'

urlpatterns = patterns('',
    url(r'^$', 'o2.views.index', name='index'),
    
    url(r'^users/$', 'o2.views.users', name='users'),
    url(r'^user/login/$', 'o2.views.user_login', name='user_login'),
    url(r'^user/edit/$', 'o2.views.user_edit', name='user_edit'),
    url(r'^user/profile/$', 'o2.views.user_profile', name='user_profile'),
    url(r'^user/(?P<username>.+)/picture/$', 'o2.views.user_picture', name='user_picture'),
    url(r'^user/(?P<username>.+)/$', 'o2.views.user_view', name='user_view'),
    
    url(r'^ombudsman/new/$', 'o2.views.ombudsman_new', name='ombudsman_new'),
    url(r'^ombudsman/edit/$', 'o2.views.ombudsman_edit', name='ombudsman_edit'),
    url(r'^ombudsman/(?P<ombudsman_slug>.+)/ticket/(?P<ticket_slug>.+)/$', 'o2.views.ticket_view', name='ticket_view'),
    url(r'^ombudsman/(?P<slug>.+)/picture/$', 'o2.views.ombudsman_picture', name='ombudsman_picture'),
    url(r'^ombudsman/(?P<slug>.+)/$', 'o2.views.ombudsman_view', name='ombudsman_view'),
    url(r'^ombudsman/$', 'o2.views.ombudsman', name='ombudsman'),
    
    url(r'^about/$', 'o2.views.about', name='about'),
    url(r'^help/$', 'o2.views.helpme', name='help'),
    url(r'^faq/$', 'o2.views.faq', name='faq'),
    url(r'^contact/$', 'o2.views.contact', name='contact'),
    
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='auth_logout'),
    
    url(r'^api/', include(o2_api.urls)),
    
    url(r'^admin/', include(admin.site.urls)),
    
    url(r'^i18n/', include('django.conf.urls.i18n')),
    
    url(r'^validators/user/username/$', 'o2.validators.user_username', name='validator_user_username'),
    url(r'^validators/user/email/$', 'o2.validators.user_email', name='validator_user_email'),
    
    url(r'', include('social.apps.django_app.urls', namespace='social')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}))