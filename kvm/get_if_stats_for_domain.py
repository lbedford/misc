#!/usr/bin/python2.7
"""Script to get interface statistics from a libvirt domain."""

import argparse
import libvirt
import os
import sys
import datetime
import xml.etree.ElementTree as ET

def get_lib_virt_domain(domain):
  """Connect to libvirt and look for a domain by name."""
  conn = libvirt.openReadOnly('qemu:///system')
  if conn == None:
    print 'Failed to open connection to the hypervisor'
    return conn

  try:
    dom = conn.lookupByName(domain)
  except libvirt.libvirtError:
    print 'Failed to find the domain %s' % (domain)
    return None
  return dom

def get_domain_interface_stats(dom, interface):
  """Parse the XML of a domain to get the active interfaces."""
  xml = dom.XMLDesc(0)
  tree = ET.fromstring(xml)
  interfaces = []
  for network in tree.find('devices').findall('interface'):
    interfaces.append(network.find('target').attrib['dev'])
  return dom.interfaceStats(interfaces[interface])

def get_domain_uptime(domain):
  """Calculate domain uptime from start time of kvm process."""
  with open('/var/run/libvirt/qemu/%s.pid' % domain) as pid_file:
    for line in pid_file:
      pid = line
  start_time = os.stat('/proc/%s' % pid).st_ctime
  return datetime.datetime.now() - datetime.datetime.fromtimestamp(
      start_time)

def parse_arguments():
  """Parse the command line arguments."""
  parser = argparse.ArgumentParser(
      description='Get network interface stats for a domain.')
  parser.add_argument('domain')
  parser.add_argument('--interface', default=0, type=int)
  args = parser.parse_args()
  if 'domain' not in args:
    parser.print_help()
    return None
  return args

def main():
  """Get arguments, get domain, get interface, print stats."""
  args = parse_arguments()
  if not args:
    sys.exit(1)
  domain_name = args.domain
  dom = get_lib_virt_domain(domain_name)
  if not dom:
    sys.exit(2)
  if_stats = get_domain_interface_stats(dom, args.interface)
  print if_stats[0] # rx_bytes
  print if_stats[4] # tx_bytes
  print get_domain_uptime(domain_name)
  print domain_name
  

if __name__ == "__main__":
  main()
