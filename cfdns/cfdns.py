#!/usr/bin/env python

import CloudFlare
import getopt
import re
import os
import signal
import sys
from requests import get
import ConfigParser


class CfDns :
    '''
    '''
    def __init__(self):
        try:
            if len(sys.argv) <= 1:
                self.usage()
            opts, args = getopt.getopt(sys.argv[1:], 'n:d:', [])
        except getopt.GetoptError:
            self.usage()
        
        self._dev = None
        self._dns_name = None
        self._zone_name = None
        
        for k,v in opts: 
            if k in ("-n"):
                self._dns_name =v 
            elif k in ("-d"):
                self._dev = v

        if self._dns_name != None:
            m = re.match(r"^([\w|-]+)((\.[\w|-]+)*)$", self._dns_name)
            if m != None:
                zone_name = m.group(2)
                m = re.match(r"^\.(.*)$", zone_name)
                self._zone_name = m.group(1)
        else: 
            exit("Error: dns name not set")
        
        cp = ConfigParser.ConfigParser()
        cfg_file = os.path.dirname(__file__) + '/cfdns.conf'
        cp.read(cfg_file)
        self._cf_user = cp.get("cloudflare", 'email')
        self._cf_key = cp.get("cloudflare", 'token')

    def update(self):
        self.mark_cfdns_running()

        cf = CloudFlare.CloudFlare(email=self._cf_user, token=self._cf_key)
       
        try:
            params = { 'name': self._zone_name}
            zones = cf.zones.get(params = params)
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            self.err('/zones %d %s - api call failed' % (e, e))
        except Exception as e:
            self.err('/zones.get - %s - api call failed' % (e))
        
        if len(zones) == 0:
            self.err('/zones.get - %s - zone not found' % (self._zone_name))
        if len(zones) != 1:
            self.err('/zones.get - %s - api call returned %d items' % (self._zone_name, len(zones)))
        
        zone = zones[0]
        zone_id = zone['id']

        try:
            params = {'name': self._dns_name, 'match': 'all', 'type': 'A'}
            dns_records = cf.zones.dns_records.get(zone_id, params = params)
        except CloudFlare.exceptions.CloudFlareAPIError as e:
            self.err('/zones/dns_records %s - %d %s - api call failed' % (self._dns_name, e, e))
        
        if self._dev != None:
            ip = self.get_dev_ip(self._dev)
        else:
            # get ip from remote
            ip = self.get_default_ip()

        for dns_record in dns_records:
            old_ip_address = dns_record['content']
            old_ip_type = dns_record['type']

            if old_ip_type != 'A':
                continue
            if old_ip_address == ip:
                self.err("Not need to update")
            dns_record_id = dns_record['id']
            dns_record = {
                'name': self._dns_name,
                'type': 'A',
                'content': ip
            }

            try:
                dns_record = cf.zones.dns_records.put(zone_id, dns_record_id, data=dns_record)
            except CloudFlare.exceptions.CloudFlareAPIError as e:
                self.err('/zones.dns_records.put %s - %d %s - api call failed' % (self._dns_name, e, e))
            
            print('UPDATED: %s %s -> %s' % (self._dns_name, old_ip_address, ip))
            self.mark_cfdns_not_running()
        


    def usage(self):
        print ("cfdns.py ")
        print ("  -n   dns name")
        print ("  -d   network device")


    def get_dev_ip(self, dev):
        cmd = "ip addr show dev "+ dev
        buf = os.popen(cmd, "r", 1)
        output = buf.readlines()
        for line in output:
            l = line.strip()
            m = re.match(r"^inet (\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})", l)
            if m == None:
                continue
            return m.group(1)
        return None

    def get_default_ip(self):
        ip = get('https://api.ipify.org').text
        return ip

    # is_cfdns_running
    # check whether cfdns is running and kill it .
    def is_cfdns_running(self):
        pid_file = os.path.dirname(__file__) + "/cfdns.pid"
        if os.path.exists(pid_file):
            with open(pid_file) as f:
                pid = f.read()
                f.close()
            os.kill(pid, signal.SIGTERM)
            os.unlink(pid_file)

    def mark_cfdns_running(self):
        self.is_cfdns_running()
        pid_file = os.path.dirname(__file__) + "/cfdns.pid"
        with open(pid_file, "w") as f:
            f.write(os.getpid())
            f.close()
    
    def mark_cfdns_not_running(self):
        pid_file = os.path.dirname(__file__) + "/cfdns.pid"
        os.unlink(pid_file)

    def err(self, errmsg):
        self.mark_cfdns_not_running()
        exit(errmsg)
     

cf = CfDns()
cf.update()
