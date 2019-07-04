#!/usr/bin/env python

import os
import json
import socket
import getopt
import sys


cache_file = os.path.dirname(__file__) +'/cache.dat'


class DdnsMon:
    def __init__(self):
        try:
            if len(sys.argv) <= 1:
                self.usage()
            opts, args = getopt.getopt(sys.argv[1:], 'd:p:l:', ['proto=','localport='])
        except getopt.GetoptError:
            self.usage()

        for k,v in opts:
            if k in ("-d"):
                self.domain = v
            elif k in ("-p"):
                self.port = v
            elif k in ("-l"):
                self.local_ip = v
            elif k in ("--proto"):
                self.proto = v
            elif k in ("--localport"):
                self.local_port = v
    
    def run(self):

        now_ip = socket.gethostbyname(self.domain)
        old_ip = self.get_cached_ip(self.domain, self.proto)
        if now_ip == old_ip:
            return
        if old_ip != None: 
            self.remove_rules(old_ip)
        self.add_rules(now_ip)

        self.set_cached_ip(self.domain, self.proto, now_ip)
        print ("iptables rules updated. %s => %s \n" % (self.domain, now_ip))

       
    def remove_rules(self, old_ip):
        cmd = "iptables -D INPUT -m state --state NEW -p %s --dport %s -j ACCEPT" % (self.proto, self.local_port)
        os.system(cmd)
        print (cmd)

        cmd = "iptables -t nat -D PREROUTING -p %s --dport %s -j DNAT --to-destination %s:%s" %(self.proto, self.local_port, old_ip, self.port)
        os.system(cmd)
        print (cmd)

        cmd = "iptables -t nat -D POSTROUTING -d %s -p %s --dport %s -j SNAT --to-source %s" % (old_ip, self.proto, self.port, self.local_ip)
        os.system(cmd)
        print (cmd)
    
    def add_rules(self, now_ip):
        cmd = "iptables -A INPUT -m state --state NEW -p %s --dport %s -j ACCEPT" % (self.proto, self.local_port)
        os.system(cmd)
        print (cmd)

        cmd = "iptables -t nat -A PREROUTING -p %s --dport %s -j DNAT --to-destination %s:%s" %(self.proto, self.local_port, now_ip, self.port)
        os.system(cmd)
        print (cmd)

        cmd = "iptables -t nat -A POSTROUTING -d %s -p %s --dport %s -j SNAT --to-source %s" % (now_ip, self.proto, self.port, self.local_ip)
        os.system(cmd)
        print (cmd)

    def get_cached_ip(self, domain, proto):
        try:
            f = open(cache_file, 'r')
            json_data = f.read()
            data = json.loads(json_data)
            k = domain + "-" + proto
            if k in data: 
                return data[k]
            return  None
        except Exception:
            return None
    
    def set_cached_ip(self, domain, proto, ip):
        try:
            f = open(cache_file, 'r')
            json_data = f.read()
            data = json.loads(json_data)
            f.close()
        except Exception:
            data = {}
        
        try: 
            f = open(cache_file, 'w')
            k = domain + "-" + proto
            data[k] = ip
            json_data = json.dumps(data)
            print (json_data)
            f.write(json_data)
            f.close()
        except Exception: 
            return False

    def usage(self):
        print ("ddns_mon.py ")
        print ("------------------------------")
        print ("  -d           domain")
        print ("  -l           local ip")
        print ("  -p           port ")
        print ("  --proto      tcp / udp")
        print ("  --localport local port ")
        sys.exit()
        

if __name__ == "__main__":
    o = DdnsMon()
    o.usage()