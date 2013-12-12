CloudAdmin
==========

CloudAdmin is a draft implementation of a heterogeneous cloud management webservice, written in Python/Django.

**Prerequisites**

1. CloudAdmin requires Citrix XenServer (tested on Version 6.2).
2. CloudAdmin uses Puppet and Puppet-Dashboard MySQL database (tested on Puppet-Dashboard 1.2). Follow the instructions from the official manual from http://docs.puppetlabs.com/dashboard/manual/1.2.
3. CloudAdmin relies on Django 1.6 and Python 2.7.

**Installation**

1. **VM management**: install XenAPI pyton library (from Debian/Ubuntu repositories, Python Pip, or Git). Provide your XenServer credentials in vms/models.py.

2. **Servive management**: install pymysql python library (from Python Pip or Git repository). Provide Puppet MySQL database credentials in services/models.py. Add to the [master] section of your puppet.conf, the following statement:

        storeconfigs=true

3. **Web GUI**: from the application folder, run:

        python ./manage.py syncdb
        python ./manage.py runserver

**Use Considerations**

1. Access the Web GUI at http://localhost:8000/admin. Currently, the only view available is the administration section.

2. Either XenServer or Puppet template creations are not supported yet. VM templates or Puppet modules must be created before registering the actual VM/Module name in CloudAdmin. For instance, in XenServer, you may create a VM named "test", then you may register a VM template named "test" on CloudAdmin.

3. Puppet node integration from VM creation on XenServer is not supported yet. The VM public key must manually registered on Puppet Dashboard interface.

4. Just be careful when using the CloudAdmin VM management, you are directly creating/modifying/deleting VMs.
