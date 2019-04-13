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

for node in nodes["nodes_list"]:
    try:
        machine=client.machines.create(architecture="amd64",
                mac_addresses=[node["mac"]],
                power_type="manual",hostname=node["name"],
                domain="int.carrefour.io")
        print (("%s is now commissionning. Please reboot it!") %(node["name"]))
    except Exception as exc:
        print(exc)
