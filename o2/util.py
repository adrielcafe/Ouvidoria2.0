# -*- coding: utf-8 -*-
from django.utils.datetime_safe import date
from libcdmi import cdmi
from o2.models import OmbudsmanOffice
import json
import StringIO
#import pycurl

def calculate_age(born):
    today = date.today()
    return today.year - born.year - int((today.month, today.day) < (born.month, born.day))

def SubscribeUserInOmbudsmanOffice(slug, user_dbref):
    OmbudsmanOffice.objects(slug = slug).update_one(
        add_to_set__users = user_dbref
    )
    
def UnsubscribeUserInOmbudsmanOffice(slug, user_dbref):
    OmbudsmanOffice.objects(slug = slug).update_one(
        pull__users = user_dbref
    )

def fiware_create_container(endpoint, credentials, container_name):
    conn = cdmi.CDMIConnection(endpoint, credentials)
    conn.container_proxy.create('/{0}'.format(container_name))
    print conn.container_proxy.read('/')
    
'''def fiware_get_token(username, password):
    data = {"auth": {
                "passwordCredentials": {
                    "username": username, 
                    "password": password
            }}}
    
    str = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, 'http://cloud.lab.fi-ware.eu:4730/v2.0/tokens')
    c.setopt(pycurl.HTTPHEADER, ['Content-type: application/json'])
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.POSTFIELDS, json.dumps(data))
    c.setopt(pycurl.WRITEFUNCTION, str.write)
    c.perform()
    
    initial_token = json.loads(str.getvalue())
    initial_token = initial_token['access']['token']['id']
    print 'initial_token', initial_token
    
    str = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, 'http://cloud.lab.fi-ware.eu:4730/v2.0/tenants')
    c.setopt(pycurl.HTTPHEADER, ['x-auth-token: {0}'.format(initial_token)])
    c.setopt(pycurl.WRITEFUNCTION, str.write)
    c.perform()

    tenant = json.loads(str.getvalue())
    tenant = tenant['tenants'][0]['id']
    print 'tenant', tenant
    
    data['auth']['passwordCredentials']['tenantId'] = tenant
    
    str = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, 'http://cloud.lab.fi-ware.eu:4730/v2.0/tokens')
    c.setopt(pycurl.HTTPHEADER, ['Content-type: application/json'])
    c.setopt(pycurl.POST, 1)
    c.setopt(pycurl.POSTFIELDS, json.dumps(data))
    c.setopt(pycurl.WRITEFUNCTION, str.write)
    c.perform()
    
    final_token = json.loads(str.getvalue())
    final_token = final_token['access']['token']['id']
    print 'final_token', final_token
    
    str = StringIO.StringIO()
    c = pycurl.Curl()
    c.setopt(pycurl.URL, 'http://130.206.82.9:8080/cdmi/{0}/test123'.format(tenant))
    c.setopt(pycurl.HTTPHEADER, ['Content-Type: application/cdmi-container', 'Accept: application/cdmi-container', 'X-Auth-Token: {0}'.format(final_token)])
    c.setopt(pycurl.PUT, 1)
    c.setopt(pycurl.WRITEFUNCTION, str.write)
    c.perform()
    
    print str.getvalue()
    
    return {'initial_token': initial_token, 'tenant': tenant, 'final_token': final_token }'''