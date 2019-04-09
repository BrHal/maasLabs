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

for node in nodes["nodes_list"]:
    try:
        machine=client.machines.create(architecture="amd64",
                mac_addresses=[node["mac"]],
                power_type="manual",hostname=node["name"],
                domain="int.carrefour.io").mark_broken()
        bridge=machine.interfaces.create(InterfaceType.BRIDGE, name='br-maas', parent=machine.interfaces.get_by_name('eth0'))
        bridge.vlan=subnet.vlan
        bridge.links.create(mode=LinkMode.AUTO,subnet=subnet)
        bridge.save()
        machine.mark_fixed()
        machine.commission()
    except Exception as exc:
        print(exc)
