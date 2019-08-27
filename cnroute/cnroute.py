#!/usr/bin/env python

import sys
import getopt
import os
import re

class CNRoute:
    '''
    '''
    def __init__(self):
        try:
            if len(sys.argv) <= 1:
                self.usage()
            opts, args = getopt.getopt(sys.argv[1:], 'uar', ['gw='])
        except getopt.GetoptError:
            self.usage()

        self._route_file = os.path.dirname(__file__) + '/all_cn_cidr.txt'

        for k,v in opts:
            if k in ("-u"):
                cmd = "u"
            elif k in ("-a"):
                cmd = "a"
            elif k in ("-r"):
                cmd = "r"
            elif k in ("--gw"):
                if re.match("^\d", v):
                    self._gw_str = "via " + v
                else:
                    self._gw_str = "dev " + v
        
        if cmd == "u":
            self.update_cn_route()
        elif cmd == "a":
            try: 
                self._gw_str
            except NameError:
                print "Error: Gateway not set \n"

            self.add_cn_route()
        elif cmd == "r":
            try: 
                self._gw_str
            except NameError:
                print "Error: Gateway not set \n"

            self.rm_cn_route()


    def update_cn_route(self):
        cmd = "wget -O "+self._route_file+" https://ispip.clang.cn/all_cn_cidr.txt"
        os.system(cmd)
    
    def add_cn_route(self):
        with open(self._route_file, 'r') as f:
            for line in f.readlines():
                l = line.strip()
                cmd = "ip ro add "+l+" " + self._gw_str
                os.system(cmd)

    
    def rm_cn_route(self):
        with open(self._route_file, 'r') as f:
            for line in f.readlines():
                l = line.strip()
                cmd = "ip ro delete "+l+" " + self._gw_str
                os.system(cmd)
    
    def usage(self):
        print "cnroute "
        print "  -u   update"
        print "  -a   add cn routes"
        print "  -r   remove cn routes"
        print "  --gw  gateway(device or ip address) "

cnr = CNRoute()
