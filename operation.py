# -*- coding: utf-8 -*-

import manager

###############################################################################


if __name__ == "__main__":
    manager = manager.Manager()

    #record = {'mac': mac, 'name': name, 'dept': dept}
    #manager.add(record) #

    #ip = None
    #manager.remove(ip) #

    record = {'ip': '10.4.101.101', 'mac': '1234-1234-1234'}
    manager.update(record) #

    #manager.save()
    manager.quit()
