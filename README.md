cobbler-csv
===========

Import cobbler server entries based on a CSV file, and also includes a trigger
to sync Spacewalk Custom Info with Cobbler after initial import.  Delete
/var/lib/cobbler/triggers/change/post-trigger if you don't want to use it.

Packages are available in the [COPR repo](https://copr.fedoraproject.org/coprs/stbenjam/cobbler-csv/).

<pre>
-----------------------------------------------------------
Creating new system www1...

Setting hostname:
www1.example.com

Setting kernel_opts:
{
    "quiet": null,
    "acpi": false
}

Setting kernel_opts_post:
{
    "quiet": null,
    "acpi": true
}

Setting ks_meta:
{
    "potato": true
}

Setting name_servers:
['8.8.8.8', '8.8.4.4']

Setting name_servers_search:
example.com

Setting profile:
default

Setting system_name:
www1

System saved!
-----------------------------------------------------------
Syncing cobbler...
Done.
-----------------------------------------------------------
</pre>

Configuration
=============

The configuration file is /etc/cobbler-csv.conf.

Cobbler Configuration
---------------------

<pre><code>
[cobbler]
api\_url = http://localhost/cobbler\_api
use\_rhn\_auth = false
use\_shared\_secret = true
username = cobbler
password = password
</pre></code>

There are multiple ways to authenticate to cobbler.

  * If you're using an RHN Satellite or Spacewalk, you can use the RHN's taskomatic user to authenticate.
  * If you're running this from the cobbler server, you can access the shared secret stored on the system
  * You can provide normal cobbler API credentials


Mapping Configuration
--------------------

The mapping in cobbler-csv.conf matches the column names in your CSV file to the cobbler parameters
mentioned.

MIT License
===========

Copyright (c) 2014 Stephen Benjamin

Permission is hereby granted, free of charge, to any person obtaining
a copy of this software and associated documentation files (the "Software"),
to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense,
and/or sell copies of the Software, and to permit persons to whom the Software
is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
 all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.

