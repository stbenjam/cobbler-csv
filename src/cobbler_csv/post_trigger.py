#!/usr/bin/env python

import datetime
import sys
import xmlrpclib
from config import Config
from cobbler_system import CobblerSystem

def post_trigger(configFile="/etc/cobbler-csv.conf", hostname=None):
    config = Config(configFile=configFile)

    if hostname == None:
        if len(sys.argv) < 2:
            sys.exit(0)

        if sys.argv[1] != "system":
            print "Nothing to do! Not a system change"
            sys.exit(0)

        hostname = sys.argv[2]

    system = CobblerSystem(configFile, hostname=hostname)
    details = system.show()

    if details == []:
        sys.exit(0)
    else:
        ks_meta = details[0]["ks_meta"]

    rhn = xmlrpclib.Server('http://localhost/rpc/api', verbose=0)
    key = rhn.auth.login(config.satellite_username, config.satellite_password)
    system_ids = rhn.system.getId(key, hostname)

    existing = rhn.system.custominfo.listAllKeys(key)
    existing = [k['label'] for k in existing]

    for k in ks_meta.keys():
        if k not in existing:
            rhn.system.custominfo.createKey(key, k, "KS Metadata")

    for system_id in system_ids:
        rhn.system.setCustomValues(key,system_id["id"],ks_meta)
