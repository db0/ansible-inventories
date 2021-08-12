#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = r'''
name: execution_host
plugin_type: inventory
short_description: Returns first active execution host
description: Returns first active execution host for each technology, according to the order given
options:
 plugin:
  description: Name of the plugin
  required: true
  choices: ['db0.inventories.execution_host']
 execution_hosts:
  description: List of technologies to separate the host into. Each technology will be a group name in the inventory. Each entry has to be a list of hostnames.
  required: true
'''
from ansible.module_utils._text import to_native
from ansible.module_utils._text import to_text
from ansible.plugins.inventory import BaseInventoryPlugin
from ansible.errors import AnsibleError, AnsibleParserError
import socket


class InventoryModule(BaseInventoryPlugin):

	NAME = 'db0.inventories.execution_host'

	def verify_file(self, path):
		''' return true/false if this is possibly a valid file for this plugin to consume '''
		valid = False
		if super(InventoryModule, self).verify_file(path):
			valid = True
		return valid

	def parse(self, inventory, loader, path, cache):
		'''Return dynamic inventory from source '''
		super(InventoryModule, self).parse(inventory, loader, path, cache)
		# Read the inventory YAML file
		self._read_config_data(path)
		try:
			self.execution_hosts = self.get_option('execution_hosts')
		except Exception as e:
			raise AnsibleParserError(f'All options required! {e}')
		for tech in self.execution_hosts:
			# For each tech, we create an inventory group
			self.inventory.add_group(tech)
			for hostname in self.execution_hosts[tech]:
				# If a host is open to ssh, then we consider it an active and break out of the loop
				# If it is not, then we continue progressing to the other hosts.
				if check_ssh(hostname):
					self.inventory.add_host(host=hostname, group=tech)
					self.inventory.set_variable(hostname, 'ansible_python_interpreter', '/usr/bin/python3')
					break



def check_ssh(server_name, port=22):
	'''Checks if the specified hostname has an ssh port open'''
	try:
		test_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		test_socket.connect((server_name, port))
	except Exception as ex:
		# not up, log reason from ex if wanted
		return False
	else:
		test_socket.close()
	return True
