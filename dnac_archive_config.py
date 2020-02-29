#!/usr/bin/env python
# Copyright (c) 2018 World Wide Technology, Inc.
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

ANSIBLE_METADATA = {
    'metadata_version': '1.1',
    'status': ['preview'],
    'supported_by': 'community'
}

DOCUMENTATION = r'''

module: dnac_archive_config
short_description: Create an archive of the configuration.  
description:
    - Create an archive of the device configuration.  

version_added: "2.5"
author: "Jeff Andiorio (@jandiorio)"

options:
  host: 
    description: 
      - Host is the target Cisco DNA Center controller to execute against. 
    required: true

  port: 
    description: 
      - Port is the TCP port for the HTTP connection. 
    required: true
    default: 443
    choices: 
      - 80
      - 443

  username: 
    description: 
      - Provide the username for the connection to the Cisco DNA Center Controller.
    required: true
    
  password: 
    description: 
      - Provide the password for connection to the Cisco DNA Center Controller.
    required: true

  use_proxy: 
    description: 
      - Enter a boolean value for whether to use proxy or not.  
    required: false
    default: true
    choices:
        - true
        - false

  use_ssl: 
    description: 
      - Enter the boolean value for whether to use SSL or not.
    required: false
    default: true
    choices: 
      - true
      - false
    
  timeout: 
    description: 
      - The timeout provides a value for how long to wait for the executed command complete.
    required: false
    default: 30

  validate_certs: 
    description: 
      - Specify if verifying the certificate is desired.
    required: false
    default: true
    choices: 
      - true
      - false

  state: 
    description: 
      - State provides the action to be executed using the terms present, absent, etc.
    required: true
    default: present
    choices: 
      - present
      - absent

  device_name: 
    description: 
      - name of the device in the inventory database that you would like to update
    required: false

  device_mgmt_ip: 
    description: 
      - Management IP Address of the device you would like to update 
    required: false

  running_config: 
    description: 
        - Boolean for whether to backup the running configuration 
    required: false
    default: false
  
  startup_config: 
    description: 
      - Boolean for whether to backup the startup configuration 
    required: false
    default: false

  vlans: 
    description: 
      - Boolean for whether to backup the vlan database
    required: false
    default: false

  all: 
    description: 
      - Boolean for whether to backup all options (running, startup, vlans)
    required: false
    default: true

notes: 
    - Either device_name or device_mgmt_ip is required, but not both.  

'''

EXAMPLES = r'''

!! NEED EXAMPLE!!

'''

RETURN = r'''
#
'''

from ansible.module_utils.basic import AnsibleModule
from ansible.module_utils.network.dnac.dnac import DnaCenter,dnac_argument_spec

def main():
    _device_exists = False
    payload = ''
    module_args = dnac_argument_spec
    module_args.update(
        device_name=dict(type='str', required=False),
        device_mgmt_ip=dict(type='str',required=False),
        running_config=dict(type='str', required=False, default=False),
        startup_config=dict(type='str', required=False, default=False),
        vlans=dict(type='str', required=False, default=False),
        all=dict(type='str', required=False, default=True)
    )

    result = dict(
        changed=False,
        original_message='',
        message='')

    module = AnsibleModule(
        argument_spec = module_args,
        supports_check_mode = False
        )

    # Instantiate the DnaCenter class object
    dnac = DnaCenter(module)

    # Get device details based on either the Management IP or the Name Provided
    if module.params['device_mgmt_ip'] is not None:
        dnac.api_path = 'api/v1/network-device?managementIpAddress=' + module.params['device_mgmt_ip']
    elif module.params['device_name'] is not None:
        dnac.api_path = 'api/v1/network-device?hostname=' + module.params['device_name']

    device_results = dnac.get_obj()
    device_id = device_results['response'][0]['id']

    payload = {
        "deviceIds": [
            device_id
        ],
        "configFileType": {
            "runningconfig": module.params['running_config'],
            "startupconfig": module.params['startup_config'],
            "vlan": module.params['vlans'],
            "all": module.params['all']
        }
    }

    dnac.api_path = 'api/v1/archive-config'
    archive_config_results = dnac.create_obj(payload)
    if not archive_config_results.get('isError'):
        result['changed'] = True
        result['original_message'] = archive_config_results
        module.exit_json(msg='Device Config Archived Successfully.', **result)
    elif archive_config_results.get('isError'):
        result['changed'] = False
        result['original_message'] = archive_config_results
        module.fail_json(msg='Failed to Archive Device Configuration!', **result)

if __name__ == "__main__":
  main()
