# -*- coding: utf-8 -*-

import sqlite3

###############################################################################


class ONDB:
    '''
    handle office network database

    '''

    def __init__(self, db=None):
        try:
            self.conn = sqlite3.connect(db)
            self.cursor = self.conn.cursor()
        except Exception, e:
            print e

    def close(self):
        try:
            if self.conn: self.conn.close()
            return True
        except Exception, e:
            print e

    def read_all(self):
        try:
            query = 'SELECT * FROM arp_table LEFT OUTER JOIN mac_table \
                LEFT OUTER JOIN interface_table ON \
                arp_table.mac = mac_table.mac AND \
                arp_table.ip = interface_table.ip'
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception, e:
            print e

    def read_mac_from_mac_table(self, mac=None):
        try:
            query = 'SELECT * FROM mac_table WHERE mac_table.mac = %s' % (mac)
            self.cursor.execute(query)
            return self.cursor.fetchall()
        except Exception, e:
            print e

    def update_arp_table(self, record=None):
        try:
            query = 'REPLACE INTO arp_table VALUES(?, ?)'
            self.cursor.execute(query, (record.get('ip'), record.get('mac')))
            self.conn.commit()
            return True
        except Exception, e:
            print e

    def update_mac_table(self, record=None):
        try:
           query = 'REPLACE INTO mac_table VALUES(?, ?, ?)'
           self.cursor.execute(query, (record.get('mac'), record.get('name'), 
               record.get('dept')))
           self.conn.commit()
           return True
        except Exception, e:
           print e

    def update_interface_table(self, record=None):
        try:
            query = 'REPLACE INTO interface_table VALUES(?, ?, ?)'
            self.cursor.execute(query, (record.get('ip'), record.get('switch'),
                record.get('interface')))
            self.conn.commit()
            return True
        except Exception, e:
            print e

