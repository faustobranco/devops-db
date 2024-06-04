#!/usr/bin/env python3

import json
import os

class DynamicInventory(object):
    """
    Example of a class for returning Dynamic Inventory to an Ansible playbook.
    :return: Json with the inventory.
    :rtype: json.
    """
    def __init__(self):
        self.json_inventory = {}
#
        self.host_group = os.environ.get('host_group')
        self.host_tech = os.environ.get('host_tech')
        self.host_service = os.environ.get('host_service')
#
        self.json_inventory = self.LoadInventory()
#
        print(json.dumps(self.json_inventory))
# Empty inventory for testing.
    def EmptyInventory(self):
        """
        Returns an empty Inventory, in case of errors.
        :return: Json with the inventory.
        :rtype: json.
        """
        return {'_meta': {'hostvars': {}}}
#
# Example inventory for testing.
    def LoadInventory(self):
        """
        Example of a method for creating an inventory return Json.
        :return: Json with the inventory.
        :rtype: json.
        """
        return {
                "_meta": {
                    "hostvars": {
                        "srv-infrastructure-test-master-01": {
                            "ansible_host": "172.21.5.157",
                        },
                        "srv-infrastructure-jenkins-master-01": {
                            "ansible_host": "172.21.5.154",
                        },
                    }
                },
                "all": {
                    "children": [
                        "tests_Hosts"
                    ]
                },
                "tests_Hosts": {
                    "hosts": [
                        "srv-infrastructure-test-master-01",
                        "srv-infrastructure-jenkins-master-01"
                    ],
                    "vars": {
                        "host_group": self.host_group,
                        "host_tech": self.host_tech,
                        "host_service": self.host_service
                    }
                }
            }

if __name__ == "__main__":
    try:
        # Get the inventory.
        DynamicInventory()
    except Exception as e:
        print(json.dumps({"_meta": {"hostvars": {}}}))