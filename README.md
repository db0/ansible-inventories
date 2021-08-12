# Ansible Collection - Db0 Inventories

This collection contains utilities for handling ansible inventories

The following inventory plugins are provided

## execution_host

This inventory plugin will parse a specialized inventory file
and create an ansible inventory output which contains only
one host per technology specified based on what is active at the time

This is useful when using ansible to perform REST API calls on some service via a jumphost. 
This plugin allows you to specify any amount of jumphosts to use as failovers, 
but will only execute the code on one of them.


### Sample inventory file and playbook


```
plugin: db0.inventories.execution_host
execution_hosts:
  netapp_executor:
  - nas-admin1
  - nas-admin2
  ilo_executor:
  - linux-admin1
  - linux-admin2
  switch_executor:
  - swadm1
  - swadm2
```

```
- hosts: ilo_executor
[...]
```

In this example, the ilo_executor will always return `linux-admin1` but if that goes down, it will return `linux-admin2`

### Considerations

Currently this inventory if hardcoded to use `/usr/bin/python3` as the ansible interpreter
