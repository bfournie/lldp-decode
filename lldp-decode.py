#!/usr/bin/env python
#    Licensed under the Apache License, Version 2.0 (the "License"); you may
#    not use this file except in compliance with the License. You may obtain
#    a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#    Unless required by applicable law or agreed to in writing, software
#    distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
#    WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
#    License for the specific language governing permissions and limitations
#    under the License.

import argparse
import binascii
import json
import logging
import os
import six
import sys
import subprocess

import lldp_parsers


def parse_opts(argv):
    parser = argparse.ArgumentParser(
        description='Decode raw LLDP introspection data')
    parser.add_argument('-o', '--output-dir', metavar='OUTPUT_DIR',
                        help="""Output dir for all the templates""",
                        default='')
    opts = parser.parse_args(argv[1:])

    return opts


def get_introspection_data(node):
    filename = "tmp-" + node

    cmd = "/bin/openstack baremetal introspection data save " + \
          node + " > " + filename

    try:
        p = subprocess.Popen(cmd, shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE)

    except OSError as e:
        print("Error running introspection data save, Error: %s" % e)
        exit()

    stdout, stderr = p.communicate()
    if p.returncode != 0:
        print(('Error running introspection data save.'
               'Stdout: "%(stdout)s". Stderr: %(stderr)s') %
              {'stdout': stdout, 'stderr': stderr})

    with open(filename, 'r') as f:
        contents = f.read()
        data = json.loads(contents)
        f.close()
        os.remove(filename)
        return data


def _parse_lldp_tlvs(tlvs, node):
    """Parse LLDP TLVs into dictionary of name/value pairs

    :param tlvs: list of raw TLVs
    :param node_info: node being introspected
    :returns nv: dictionary of name/value pairs. The
                 LLDP user-friendly names, e.g.
                 "switch_port_id" are the keys
    """

    # Generate name/value pairs for each TLV
    parser = lldp_parsers.LLDPBasicMgmtParser(node)

    for tlv_type, tlv_value in tlvs:
        try:
            data = bytearray(binascii.a2b_hex(tlv_value))
        except TypeError as e:
            print(
                "TLV value for TLV type %(tlv_type)d not in correct "
                "format, value must be in hexadecimal: %(msg)s",
                {'tlv_type': tlv_type, 'msg': e})
            continue

        if not parser.parse_tlv(tlv_type, data):
            print("LLDP TLV type %d not handled",
                   tlv_type)

    return parser.nv_dict

def _lldp_decode():

    root_logger = logging.getLogger(None)
    if not root_logger.handlers:
        root_logger.addHandler(logging.StreamHandler())

    #opts = parse_opts(sys.argv)
    if len(sys.argv) > 1:
        node = sys.argv[1]
    # node = "618a604d-cc41-4c10-945b-c5e6b5f01020"

    data = get_introspection_data(node)

    # inventory = data.get('inventory')
    interfaces = data['inventory']['interfaces']

    if not interfaces:
        raise Error(_('Hardware inventory is empty or missing'),
                    data=data)

    print("Interface Data for Node %s" % node)
    print("============================================================")

    for iface in interfaces:
        if_name = iface['name']

        tlvs = iface.get('lldp')
        if tlvs is None:
            print("No LLDP Data found for interface %s",
            if_name)
            continue

        print("Interface: %s" % if_name)
        print("++++++++++++++++")
        print("MAC Address: %s" % iface.get('mac_address'))

        nv = _parse_lldp_tlvs(tlvs, node)

        for name, value in nv.items():
            print("%(name)s: %(value)s" % {'name': name, 'value': value})

        print('')


_lldp_decode()