#!/usr/bin/env python

import re
import urllib2
import sys
import math
import os

def generate_potatso():
    results=fetch_ip_data()
    for country_code in results:
        filename = 'data/geoip-%s.data' % (country_code)
        if not os.path.exists(os.path.dirname(filename)):
            try:
                os.makedirs(os.path.dirname(filename))
            except OSError as exc: # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise
        with open(filename, "w") as f:
            for ip,_,mask in results[country_code]:
                f.write('%s/%s\n'%(ip,mask))
        
    print "Success."


def fetch_ip_data():
    # fetch data from apnic
    # url=r'http://ftp.apnic.net/apnic/stats/apnic/delegated-apnic-latest'
    # data=urllib2.urlopen(url).read()
    # return parse_ip_data(data)
     
    # fetch data from local file
    with open('apnic.data', 'r') as data_file:
        data = data_file.read()
        return parse_ip_data(data)

def parse_ip_data(data):
    print "parsing data..."
    cnregex=re.compile(r'apnic\|\w+\|ipv4\|[0-9\.]+\|[0-9]+\|[0-9]+\|a.*',re.IGNORECASE)
    data=cnregex.findall(data)
    geoip_data = {}

    for item in data:
        unit_items=item.split('|')
        country_code=unit_items[1]
        starting_ip=unit_items[3]
        num_ip=int(unit_items[4])
        
        imask=0xffffffff^(num_ip-1)
        #convert to string
        imask=hex(imask)[2:]
        mask=[0]*4
        mask[0]=imask[0:2]
        mask[1]=imask[2:4]
        mask[2]=imask[4:6]
        mask[3]=imask[6:8]
        
        #convert str to int
        mask=[ int(i,16 ) for i in mask]
        mask="%d.%d.%d.%d"%tuple(mask)
        
        #mask in *nix format
        mask2=32-int(math.log(num_ip,2))
        if not country_code in geoip_data:
            geoip_data[country_code] = []
        geoip_data[country_code].append((starting_ip,mask,mask2))
         
    return geoip_data


if __name__=='__main__':
    generate_potatso()

