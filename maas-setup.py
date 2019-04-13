#!/usr/bin/env python
# coding: utf-8
import yaml 

from maas.client import login
from maas.client.enum import InterfaceType,LinkMode

with open("maas-lci.yaml", 'r') as stream:
    try:
        nodes=(yaml.safe_load(stream))
    except yaml.YAMLError as exc:
        print(exc)

for node in nodes["nodes_list"]:
    print ("%s : %s"%(node["mac"],node["name"]))

client=login("http://localhost:5240/MAAS", username="maaster", password="GomJabbar")
subnet=client.subnets.get('192.168.0.0/24')

for machine in client.machines.list():
    try:
        bridge=machine.interfaces.create(InterfaceType.BRIDGE, name='br-maas', parent=machine.interfaces.get_by_name('eno2'))
        bridge.vlan=subnet.vlan
        bridge.links.create(mode=LinkMode.AUTO,subnet=subnet)
        bridge.save()
    except Exception as exc:
        print(exc)
