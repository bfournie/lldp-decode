LLDP Introspection data decode tool

This tool will decode raw LLDP introspection data gathered by ironic and ouput
the decoded data in Name/Value pairs.

Getting Started

This tool must be run on an Openstack undercloud as a stack user and in
the context of the stackrc environment. It takes a Openstack baremetal
node ID, executes an Openstack to retrieve introspection data and generates
the output

Example:

(undercloud) [stack@host01 ~]$ source stackrc

(undercloud) [stack@host01 lldp-decode]$ ironic node-list
+--------------------------------------+-------+--------------------------------------+-------------+--------------------+-------------+
| UUID                                 | Name  | Instance UUID                        | Power State | Provisioning State | Maintenance |
+--------------------------------------+-------+--------------------------------------+-------------+--------------------+-------------+
| 618a604d-cc41-4c10-945b-c5e6b5f01020 | host2 | 5cbae7f7-7993-4032-bdde-a787bc6f84e9 | power on    | active             | False       |
| ccf4fa3c-9c57-4727-9b6a-396f54b63c1d | host3 | 21e69dbd-4f36-4114-b107-56d994918cd0 | power on    | active             | False       |
+--------------------------------------+-------+--------------------------------------+-------------+--------------------+-------------+

(undercloud) [stack@host01 lldp-decode]$ ./lldp-decode.py host3
Interface Data for Node host3
============================================================
Interface: p2p1
++++++++++++++++
MAC Address: a0:36:9f:52:7e:d8
switch_port_mau_type: Unknown
switch_capabilities_enabled: ['Bridge', 'Router']
switch_port_link_aggregation_support: True
switch_port_physical_capabilities: ['1000BASE-T fdx']
switch_port_id: ge-0/0/24
switch_port_autonegotiation_support: True
switch_capabilities_support: ['Bridge', 'Router']
switch_mgmt_addresses: ['10.10.191.229']
switch_port_link_aggregation_id: 663
switch_system_name: sw01-dist-1b-b12.rdu2
switch_port_link_aggregation_enabled: True
switch_port_description: host03.beaker.tripleo.lab.eng.rdu2 port 3 (Bond)
switch_port_untagged_vlan_id: 102
switch_port_vlans: [{'name': u'vlan101', 'id': 101}, {'name': u'vlan102', 'id': 102}, {'name': u'vlan104', 'id': 104}, {'name': u'vlan2001', 'id': 2001}, {'name': u'vlan2002', 'id': 2002}]
switch_chassis_id: 64:64:9b:32:f3:00
switch_port_autonegotiation_enabled: True
switch_port_mtu: 1514

<additional ports not shown>

Dependencies

This tool requires python library 'construct' - https://pypi.org/project/construct/
If not already installed, install it by:
pip install construct

