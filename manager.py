# -*- coding: utf-8 -*-

import os
import sys
import ondb
import shadow
import switch

###############################################################################


class Manager:
    '''
    handle office network

    '''

    def __init__(self):
        try:
            os.system('clear')
            print '******************************************'
            print '*       Office Network Automation        *'
            print '*            Kevin 2017-08-23            *'
            print '******************************************'

            print 'Initiate DB ... ',
            sys.stdout.flush()
            self.db = ondb.ONDB(shadow.db)
            print '[ Done ]'

            print 'Initiate Switches ... ',
            sys.stdout.flush()
            self.objs = []
            for obj in shadow.objs:
               init_str = 'switch.%s(obj)' % (obj.get('type')) 
               self.objs.append(eval(init_str))
            print '[ Done ]'

            print 'Initiate IP address ...',
            sys.stdout.flush()
            self.reserved_ip = shadow.reserved_ip
            print '[ Done ]'
        except Exception, e:
            print e

    def save(self):
        try:
            print 'Saving to switch ... ',
            sys.stdout.flush()
            self.objs[0].save()
            print '[ Done ]'
            return True
        except Exception, e:
            print e

    def quit(self):
        try:
            for obj in self.objs: obj.logout()
            print 'Bye!'
            return True
        except Exception, e:
            print e

    def maintain_arp(self):
        try:
            arp_table = self.objs[0].get_arp_table()
            for arp_item in arp_table:
                record = {'ip': arp_item[0], 'mac': arp_item[1]}
                print '%s  %s ... ' % (arp_item[0], arp_item[1]),
                self.db.update_arp_table(record)
                print 'Done.'
        except Exception, e:
            print e

    def maintain_interface(self, iplst=None):
        '''
        if iplst == None: maintain all ip
        else: maintain iplst

        '''
        try:
            iplist = []
            if iplst is not None:
                for ip in iplst: iplist.append(ip)
            else:
                for i in range(1, 255): iplist.append('10.4.100.%s' % (i))
                for i in range(1,253): iplist.append('10.4.101.%s' % (i))
            for ip in iplist:
                if ip in self.reserved_ip: continue #infrastructure
                if not self.objs[0].is_ping_ok(ip): continue #inactive
                for obj in self.objs[1:]:
                    print 'Searching %s in %s ... ' % (ip, obj.ip),
                    sys.stdout.flush()
                    rslt = obj.find_terminal_port(ip)
                    if rslt is None:
                        print 'Not found.'
                        continue
                    else:
                        print 'Found on %s:%s' % (rslt[0], rslt[1])
                        info = {'ip': ip, 'switch': rslt[0],
                        'interface': rslt[1]}
                        self.db.update_interface_table(info)
                        break
            return True
        except Exception, e:
            print e

    def add(self, record=None):
        '''
        record={'mac', 'name', 'dept'}

        '''
        try:
            if '厂家' in record.get('dept'): tag = shadow.mac_cj
            else: tag = shadow.mac_jf

            arp_table = self.objs[0].get_arp_table()
            ip = None
            for item in arp_table:
                if tag in item: ip = item[0]
            if ip is None: return False

            self.objs[0].update_arp(ip, record.get('mac')) #update switch
            self.db.update_arp_table(record) #update DB arp_table
            mac_record = {'mac': record.get('mac'),
                'name': record.get('name'),
                'dept': record.get('dept')}
            self.db.update_mac_table(mac_record) #update DB mac_table
            return [ip, record.get('mac')]
        except Exception, e:
            print e

    def remove(self, ip=None):
        '''
        not really delete, just tag a defined mac(ref. shadow.py),
        and old mac is not deleted.

        '''
        try:
            if ip is None: return False
            if ip in self.reserved_ip: return False #disallow to do
            for arp_item in self.objs[0].get_arp_table():
                if ip == arp_item.get('ip'):
                    old_mac = arp_item.get('mac')
            if '10.4.100.' in ip:
                mac = shadow.mac_jf #jufang
            elif '10.4.101.' in ip:
                mac = shadow.mac_cj #changjia
            else: return False
            self.objs[0].update_arp(record.get('ip'), mac) #update switch
            self.db.update_arp_table({'ip': ip, 'mac': mac}) #update DB arp_table
        except Exception, e:
            print e

    def update(self, record=None):
        '''
        update an IP-MAC pair to a new IP-NEW_MAC
        record={'ip', 'mac'}

        '''
        try:
            if record is None: return False
            ip = record.get('ip')
            new_mac = record.get('mac')
            if ip in self.reserved_ip: return False #disallow

            old_mac = None
            arp_table = self.objs[0].get_arp_table()
            for item in arp_table:
                if ip == item[0]: old_mac = item[1]

            #self.objs[0].update_arp(ip, new_mac)
            #self.db.update_arp_table(record) #update DB arp_table

            print self.db.read_mac_from_mac_table(old_mac)
        except Exception, e:
            print e

    #def temp_update_mac(list):
        #for item in list:
        #mac = list[0]

