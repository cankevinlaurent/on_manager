# -*- coding: utf-8 -*-

import manager

###############################################################################


if __name__ == "__main__":
    manager = manager.Manager()
    manager.maintain_arp() #get arp table from switch and store to DB
    manager.maintain_interface() #get interface from switch and store to DB
    manager.quit()
