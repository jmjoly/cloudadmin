cloudadmin
==========

Cloud Administration Software

Cloudadmin is a draft implementation of a cloud management
webservice, written in Django.

**Prerequisites:**

1. Cloudadmin requires Citrix XenServer 6.2.
2. Cloudadmin uses Puppet and Puppet-dashboard MySQL database.
3. Cloudadmin relies on Django 1.6 and Python 2.7.

**Installation:**

1. VM management:
Install XenAPI pyton library (from deb repositories in Debian or Ubuntu, or pip, or git).
Provide your XenServer credentials in vms/models.py.

2. Servive management:
Install pymysql python library (from pip or git)
Provide Puppet MySQL database credentials in services/models.py.

3. Web GUI:
Install Django 1.6. In application folder, run:

        python ./manage.py syncdb
        python ./manage.py runserver

**Use Considerations**

1. Either XenServer or Puppet template creation is not supported yet. VM templates or Puppet modules mut be created before registering the actual name in CloudAdmin.

2. Puppet nodes integration from VM creation on XenServer is not supported yet. The new VM public key must registered manually on Puppet Dashboard interface.
