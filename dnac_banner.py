#/usr/bin/env python3

ANSIBLE_METADATA = {
    'metadata_version': '1.0',
    'status' : ['development'],
    'supported_by' : 'jandiorio'
}

"""
Copyright (c) 2018 World Wide Technology, Inc.
     All rights reserved.
     Revision history:
     22 Mar 2018  |  .1 - prototype release
"""

from ansible.module_utils.basic import AnsibleModule
#import ansible.module_utils.dnac
from ansible.module_utils.dnac import DnaCenter,dnac_argument_spec
import json

# -----------------------------------------------
#  main
# -----------------------------------------------

def main():
    module_args = dnac_argument_spec
    module_args.update(
        #api_path = dict(required=True, default='api/v1/commonsetting/global/-1', type='str'),
        banner_message=dict(type='str', required=True),
        api_path=dict(required=False, default='api/v1/commonsetting/global/', type='str')
        )

    result = dict(
        changed=False,
        original_message='',
        message='')

    module = AnsibleModule(
        argument_spec = module_args,
        supports_check_mode = False
        )

    #  Build the payload dictionary
    payload = [
        {"instanceType":"banner",
        "instanceUuid": "",
        "namespace":"global",
        "type": "banner.setting",
        "key":"device.banner",
        "value":[module.params['banner_message']],
        "groupUuid":"-1",
        "inheritedGroupUuid": "",
        "inheritedGroupName": ""
        }
        ]

    # instansiate the dnac class
    dnac = DnaCenter(module)
    #
    # # check if the configuration is already in the desired state
    settings = dnac.get_common_settings(payload)
    settings = settings.json()
    #settings = json.loads(settings)

    for setting in settings['response']:
        if setting['key'] == 'device.banner':
            if setting['value'] != '':
                if setting['value'] != payload[0]['value']:
                    response = dnac.set_common_settings(payload)
                    if response.status_code not in [200, 201, 202]:
                        result['changed'] = False
                        result['status_code'] = response.status_code
                        result['msg'] = response.json()
                        module.fail_json(msg="Status Code not 200", **result)
                    else:
                        result['changed'] = True
                        result['msg'] = response.json()
                        result['status_code'] = response.status_code
                        module.exit_json(**result)
                else:
                    result['changed'] = False
                    result['msg'] = 'Already in desired state.'
                    module.exit_json(**result)

    #return response

main()

if __name__ == "__main__":
  main()