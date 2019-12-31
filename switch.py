# -*- coding: utf-8 -*-

import telnetlib

###############################################################################


class Switch(object):
    '''
    abstract base class

    '''

    def __init__(self, info=None):
        '''
        Initial telnet connection of host.
        info{type, ip, port, username, password, enpassword}

        '''
        self.ip = info.get('ip')
        self.tn = telnetlib.Telnet(self.ip, port=info.get('port'), timeout=15)

    def logout(self):
        '''Logout the host without save to disk.'''
        self.tn.close()
        return True

    def refresh_port(self, port=None):
        '''
        Shutdown and no shutdown an access port.
        ip used for assure the right device
        '''
        return False

    def _is_trunk(self, port):
        '''determine a port if it is trunk.'''
        return True

    def find_terminal_port(self, ip=None):
        '''
        ping ip first to refresh arp table,
        then find mac on which access port.
        ''' 
        return None

###############################################################################


class H3C(Switch):
    '''
    mainly used for gateway, if not, add new function

    '''

    def __init__(self, info=None):
        '''
        login and into enable mode, without display cache

        '''
        try:
            super(H3C, self).__init__(info)
            self.tn.read_until('sername:')
            self.tn.write(info.get('username').encode('ascii') + '\n')
            self.tn.read_until('assword:')
            self.tn.write(info.get('password').encode('ascii') + '\n')
            self.tn.read_until('>')
            self.tn.write('screen-length disable'.encode('ascii') + '\n')
            self.tn.read_until('>')
            self.tn.write('system-view'.encode('ascii') + '\n')
            self.tn.read_until(']')
        except Exception, e:
            print e

    def logout(self):
        '''
        quit without save to disk

        '''
        try:
            self.tn.write('quit'.encode('ascii') + '\n')
            self.tn.read_until('>')
            self.tn.write('quit'.encode('ascii') + '\n')
            super(H3C, self).logout()
            return True
        except Exception, e:
            print e

    def refresh_port(self, port=None):
        '''
        yet not really implement

        '''
        try:
            super(H3C, self).refresh_port(port)
        except Exception, e:
            print e

    def _is_trunk(self, port):
        '''
        yet not really implement

        '''
        try:
            super(H3C,self)._is_trunk(port)
        except Exception, e:
            print e

    def find_terminal_port(self, ip=None):
        '''
        yet not really implement

        '''
        try:
            super(H3C, self).find_terminal_port(ip)
        except Exception, e:
            print e

    def save(self):
        '''
        save but dont quit

        '''
        try:
            self.tn.write('save'.encode('ascii') + '\n')
            self.tn.read_until(']:')
            self.tn.write('Y'.encode('ascii') + '\n')
            self.tn.read_until('):')
            self.tn.write('\n')
            self.tn.read_until(']:')
            self.tn.write('Y'.encode('ascii') + '\n')
            self.tn.read_until(']')
            return True
        except Exception, e:
            print e

    def get_arp_table(self):
        '''
        return arp_table via list_of_list[[ip][mac]]

        '''

        try:
            self.tn.write('display arp vlan 102'.encode('ascii') + '\n')
            response = self.tn.read_until(']')
            lines = response.split('\r\n')
            for line in lines:
                if 'Aging' in line: break #locating
            arp_table = []
            for line in lines[lines.index(line)+1:-1]: #remain arp line
                item = line.split()
                arp_table.append([item[0], item[1]])
            return arp_table
        except Exception, e:
            print e

    def update_arp(self, ip=None, mac=None):
        '''
        map an ip and a mac, but do NOT save

        '''
        try:
            mac = mac.strip().lower()
            mac = mac.replace('-', '')
            mac = mac.replace('.', '')
            mac = mac[0:4] + '-' + mac[4:8] + '-' + mac[8:12]
            str = 'arp static %s %s 102 GigabitEthernet1/0/25' % (ip, mac)
            self.tn.write(str.encode('ascii') + '\n')
            self.tn.read_until('#')
            return True
        except Exception, e:
            print e

    def is_ping_ok(self, ip=None):
        '''return OK if not 100% ping packet loss'''
        try:
            str = 'ping -c 2 %s' % (ip)
            self.tn.write(str.encode('ascii') + '\n')
            response = self.tn.read_until(']')
            if '100.00% packet loss' in response: return False
            else: return True
        except Exception, e:
            print e

###############################################################################


class Cisco(Switch):

    def __init__(self, info=None):
        '''
        login and into enable mode, without display cache

        '''
        try:
            super(Cisco, self).__init__(info)
            self.tn.read_until('assword:')
            self.tn.write(info.get('password').encode('ascii') + '\n')
            self.tn.read_until('>')
            self.tn.write('terminal length 0'.encode('ascii') + '\n')
            self.tn.read_until('>')
            self.tn.write('enable'.encode('ascii') + '\n')
            self.tn.read_until('assword:')
            self.tn.write(info.get('enpassword').encode('ascii') + '\n')
            self.tn.read_until('#')
        except Exception, e:
            print e

    def logout(self):
        '''
        quit without save to disk

        '''
        try:
            self.tn.write('exit'.encode('ascii') + '\n')
            super(Cisco, self).logout()
            return True
        except Exception, e:
            print e

    def refresh_port(self, port=None):
        '''
        shutdown and re-up a given port

        '''
        try:
            self.tn.write('configure terminal'.encode('ascii') + '\n')
            self.tn.read_until('#')
            str = 'interface %s' % (port)
            self.tn.write(str.encode('ascii') + '\n')
            self.tn.read_until('#')
            self.tn.write('shutdown'.encode('ascii') + '\n')
            self.tn.read_until('#')
            self.tn.write('no shutdown'.encode('ascii') + '\n')
            self.tn.read_until('#')
            self.tn.write('exit'.encode('ascii') + '\n')
            self.tn.read_until('#')
            self.tn.write('exit'.encode('ascii') + '\n')
            self.tn.read_until('#')
            return True
        except Exception, e:
            print e

    def _is_trunk(self, port):
        '''determine a port if it is trunk'''
        try:
            self.tn.write('show interfaces trunk'.encode('ascii') + '\n')
            if port in self.tn.read_until('#'): return True
            else: return False
        except Exception, e:
            print e    

    def find_terminal_port(self, ip=None):
        '''
        Find ip on which port. The port must be an access port.
        return [ip, port]

        '''
        try:
            str = 'ping %s repeat 2 timeout 1' % (ip) #renew arp item
            self.tn.write(str.encode('ascii') + '\n')
            self.tn.read_until('#')
            str = 'show arp | include %s' % (ip)
            self.tn.write(str.encode('ascii') + '\n')
            response = self.tn.read_until('#')
            mac = None
            for arp_line in response.split('\r\n')[1:-1]: #arp result
                arp_line_split = arp_line.split()
                if ip == arp_line_split[1]: #find the needed ip
                    mac = arp_line_split[3] #get mac
                    break
            if mac is None: return None #find no given ip in arp table
            str = 'show mac address-table vlan 102 | include %s' %(mac)
            self.tn.write(str.encode('ascii') + '\n')
            response = self.tn.read_until('#')
            port = None
            for mac_line in response.split('\r\n')[1:-1]:
                mac_line_split = mac_line.split()
                if mac == mac_line_split[1]:
                    port = mac_line_split[3] #get port
                    break
            if port is None: return None #find no given mac in mac table
            if self._is_trunk(port): return None #port is trunk
            else: return [self.ip, port]
        except Exception, e:
            print e

###############################################################################


class Raisecom(Switch):

    def __init__(self, info=None):
        '''
        login and into enable mode, without display cache

        '''
        try:
            super(Raisecom, self).__init__(info)
            self.tn.read_until('ogin:')
            self.tn.write(info.get('username').encode('ascii') + '\n')
            self.tn.read_until('assword:')
            self.tn.write(info.get('password').encode('ascii') + '\n')
            self.tn.read_until('#')
            self.tn.write('terminal page-break dis'.encode('ascii') + '\n')
            self.tn.read_until('#')
        except Exception, e:
            print e

    def logout(self):
        '''
        quit without save

        '''
        try:
            self.tn.write('exit'.encode('ascii') + '\n')
            super(Raisecom, self).logout()
            return True
        except Exception, e:
            print e

    def refresh_port(self, port=None):
        '''
        shutdown and re up a given port

        '''
        try:
            self.tn.write('config terminal'.encode('ascii') + '\n')
            self.tn.read_until('#')
            str = 'interface %sort %s' % (port[0].lower(), port[1:])
            self.tn.write(str.encode('ascii') + '\n')
            self.tn.read_until('#')
            self.tn.write('shutdown'.encode('ascii') + '\n')
            self.tn.read_until('#')
            self.tn.write('no shutdown'.encode('ascii') + '\n')
            self.tn.read_until('#')
            self.tn.write('exit'.encode('ascii') + '\n')
            self.tn.read_until('#')
            self.tn.write('exit'.encode('ascii') + '\n')
            self.tn.read_until('#')
            return True
        except Exception, e:
            print e

    def _is_trunk(self, port):
        '''determine a port if it is trunk'''
        try:
           ports_str = 'P49'
           if port in ports_str: return True
           else: return False
        except Exception, e:
           print e

    def find_terminal_port(self, ip=None):
        '''
        Find ip on which port. The port must be an access port.
        return [ip, port]

        '''
        try:
            str = 'ping %s count 2 waittime 1' % (ip)
            self.tn.write(str.encode('ascii') + '\n')
            self.tn.read_until('#')
            str = 'show arp | include %s' %(ip)
            self.tn.write(str.encode('ascii') + '\n')
            response = self.tn.read_until('#')
            port = None
            for line in response.split('\r\n')[1:-1]:
                line_split = line.split()
                if ip == line_split[0]: #find needed ip in arp table
                    port = line_split[3] #get port
                    break
            if port is None: return None #find no needed ip in arp table
            if self._is_trunk(port): return None #port is trunk
            else: return [self.ip, port]
        except Exception, e:
            print e

