"""
config.py has the configuration for the cobbler-csv import tool.

Copyright 2014, Stephen Benjamin
Stephen Benjamin <stephen@bitbin.de>

"""

import os
import sys
import ConfigParser


class Config:

    def __init__(self, configFile="/etc/cobbler-csv.conf"):
        self._cp = ConfigParser.ConfigParser()
        self._cp.readfp(open(configFile))

        self._config = {}

        # Get cobbler configuration
        if self._cp.getboolean("cobbler", "use_rhn_auth"):
            self.get_rhn_credentials()
        elif self._cp.getboolean("cobbler", "use_shared_secret"):
            self.get_shared_secret()
        else:
            self._config['username'] = self._cp.get("cobbler", "username")
            self._config['password'] = self._cp.get("cobbler", "password")

        self._config['api_url'] = self._cp.get("cobbler", "api_url")

        self._config["cobbler_sync"] = self._cp.get("cobbler", "cobbler_sync")

        self._config["delimiter"] = self._cp.get("general", "delimiter")
        self._config["dialect"] = self._cp.get("general", "dialect")

    def get_rhn_credentials(self):
        """
        If we're using the rhn authorization module, we get the taskomatic
        user's password by importing the spacewalk modules
        """
        sys.path.append('/usr/share/rhn')
        try:
            from spacewalk.common.rhnConfig import initCFG, CFG
        except ImportError:
            raise ConfigError("This is not a Spacewalk server, but the" +
                              "configuration says I am.")

        initCFG()
        self._config['username'] = 'taskomatic_user'
        self._config['password'] = CFG.SESSION_SECRET_1

    def get_shared_secret(self):
        """
        Use cobbler shared secret for auth
        """
        fd = open("/var/lib/cobbler/web.ss")
        secret = fd.read()

        self._config['username'] = ""
        self._config['password'] = secret

    def get_mapping(self, item):
        return self._cp.get("mapping", item)

    def __getattr__(self, name):
        return self._config[name]


class ConfigError(Exception):
    """
    Exception when there's a problem with the configuration.
    """
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(self.value)

if __name__ == "__main__":
    config = Config("../etc/cobbler-csv.conf")
    print config.username
    print config.password
    print config.api_url
    print config.get_mapping("hostname")
