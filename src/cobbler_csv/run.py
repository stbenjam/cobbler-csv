#!/usr/bin/env python

import sys
import json
import subprocess
from custom_exceptions import *
from config import Config
from csv_parser import CsvParser
from cobbler_system import CobblerSystem
from optparse import OptionParser, OptionGroup


def run():
    # Parse Command Line Options

    usage = "usage: %prog [options]"
    Parser = OptionParser(usage=usage)
    Parser.add_option("-f", "--file", dest="csv_file",
                      metavar="STRING", help="CSV File Location")

    Parser.add_option("-c", "--config", dest="config_file", default="/etc/cobbler-csv.conf",
                      metavar="STRING", help="Config file (default: /etc/cobbler-csv.conf)")
    (options, args) = Parser.parse_args()

    if len(sys.argv) == 1:
        Parser.print_help()
        sys.exit(1)

    config = Config(configFile=options.config_file)
    csv = CsvParser(options.csv_file, config)

    for system in csv:
        print "Creating new system %s...\n" % config.get_mapping("hostname").format(**system)

        cobbler_system = CobblerSystem(options.config_file)

        interface = { 'interface': 'eth0',
           'macaddress': config.get_mapping("macaddress").format(**system),
           'ipaddress':  config.get_mapping("ipaddress").format(**system),
           'subnet':     config.get_mapping("subnet").format(**system),
           'gateway':    config.get_mapping("gateway").format(**system),
           'static':     config.get_mapping("static").format(**system)
        }
       
        cobbler_system.set_interface(**interface)
 
        attributes = [k[4:] for k in dir(cobbler_system) if k[0:4] == "set_"]
         
        for attribute in attributes:
            try:
                value = config.get_mapping(attribute).format(**system)
                getattr(cobbler_system, "set_" + attribute)(value)
                print "Setting %s:\n%s\n" % (attribute, value)
            except:
                continue  # no biggie, not a required param

        cobbler_system.set_ks_meta(**dict([(k.lower().replace(" ", "_"), v) for k, v in system.iteritems()]))

        cobbler_system.save()
        print "System saved!"
        print "-----------------------------------------------------------"

    if config.cobbler_sync:
        """
        Sync cobbler
        """
        print "Syncing cobbler..."
        cobbler_system.sync()
        print "Done."
        print "-----------------------------------------------------------"
