#!/usr/local/python
# -*- coding: utf-8 -*-

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {'metadata_version': '1.0',
                    'status': ['preview'],
                    'supported_by': 'jeff andiorio'}

DOCUMENTATION = r'''
---
module: dnac_group.py
short_description: Manage groups within Cisco DNA Center
description:  Based on 1.1+ version of DNAC API
author:
- Jeff Andiorio (@jandiorio)
version_added: '2.4'
requirements:
- DNA Center 1.1+

'''

EXAMPLES = r'''
- name: Add a new group
  dnac_group:
    hostname: dnac
    username: admin
    password: SomeSecretPassword
    name: NewGroupName
    path: /Global/NewGroupName


'''

RETURN = r'''
#
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.urls import fetch_url, open_url
from ansible.module_utils.basic import json
from anisble.module_utils._text import to_native
#from dnac import DNACModule, dnac_argument_spec
# import DnacSession


def get_group():
    # if state = query and/or parentID lookup
    pass

def create_group():
    pass

def delete_group():
    pass

def run_module():

    module_args = dict(
        hostname=dict(type='str', required=True, aliases=['host']),
        username=dict(type='str', default='admin', aliases=['user']),
        password=dict(type='str', required=True, no_log=True),
        timeout=dict(type='int', default=30),
        use_proxy=dict(type='bool', default=True),
        use_ssl=dict(type='bool', default=True),
        validate_certs=dict(type='bool', default=True),
        path=dict(type='str',default='api/v1/group')
        group_name=dict(type='str', aliases=['name'], required=True),
        state=dict(type='str', default='present', choices=['absent', 'present', 'query'],required=True),
        group_path=dict(type='str', required=True),
        group_type=dict(type='str', default='SITE', choices=['SITE', 'BUILDING', 'FLOOR'],required=True),
        group_parent_name=dict(type='str', default='Global',required=True )
    )

    result = dict(
        changed=False,
    )

    module = AnsibleModule(
        argument_spec = module_args,
        supports_check_mode=False
    )
    host = module.params['hostname']
    username = module.params['username']
    password = module.params['password']
    group_name = module.params['group_name']
    group_path = module.params['group_path']
    group_type = module.params['group_type']
    state = module.params['state']
    parent_name = module.params['parent_name']

    # manipulate or modify the state as needed (this is going to be the
    # part where your module will do what it needs to do)
    protocol = None
    if module.params['use_ssl'] is not None and module.params['use_ssl'] is False:
        protocol = 'http'
    else:
        protocol = 'https'

    url = '{0}://{1}/{2}'.format(protocol, module.parms['host'].rstrip('/'), module.params['path'].lstrip('/'))
    headers = {'Content-Type': 'application/json'}
    authheaders = {'Content-Type': 'application/json'}

    module.fail_json(msg=url)

    try:
        authurl = '{0}://{1}/api/system/v1/auth/login'.format(protocol, module.params['host'])
        authresp = open_url(authurl,
                            headers=authheaders,
                            method='GET',
                            use_proxy=module.params['use_proxy'],
                            timeout=module.params['timeout'],
                            validate_certs=module.params['validate_certs'],
                            url_username=module.params['username'],
                            url_password=module.params['password'],
                            force_basic_auth=True
                            )
    except Exception as e:
        module.fail_json(msg=e)

    if to_native(authresp.read()) != "success":  # DNA Center returns 'success' in the body
        module.fail_json(msg="Authentication failed: {}".format(authresp.read()))

    respheaders = authresp.getheaders()
    cookie = None
    for i in respheaders:
        if i[0] == 'Set-Cookie':
            cookie_split = i[1].split(';')
            cookie = cookie_split[0]

    if cookie is None:
        module.fail_json(msg="Cookie not assigned from DNA Center")

    headers['Cookie'] = cookie

    try :
        resp, info = fetch_url( module, url,
                                data=payload,
                                headers=headers,
                                method=module.params['method'].upper(),
                                use_proxy=module.params['use_proxy'],
                                force=True,
                                timeout=module.params['timeout'],)
    except Exception as e:
        module.fail_json(msg=e)

    module.exit_json(**result)

def main():
    run_module()

if __name__ == '__main__':
    main()
