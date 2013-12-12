import XenAPI
import pymysql
from django.db import models

# XenServer parameters
XEN_URL       = 'https://10.0.0.1:443/'
XEN_USER      = 'root'
XEN_PWD       = 'root'
#XEN_TEMPLATE  = 'debtest'

# MySQL parameters 
MYSQL_HOST         = "localhost"
MYSQL_PORT         = 3306
MYSQL_USER         = "dashboard"
MYSQL_PASSWD       = "mysql"
MYSQL_DASHBOARD_DB = "dashboard"

# Classes
def enum(*sequential, **named):
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

# Virtual machine template
class VmTemplate(models.Model):
    vm_template_name = models.CharField(max_length=50)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.vm_template_name

# Virtual machine definition
class Vm(models.Model):
    vm_template = models.ForeignKey(VmTemplate)
    vm_name = models.CharField(max_length=50)
    VM_STATES = (
        (0, 'Stop'),
        (1, 'Start'),
    )
    vm_state = models.IntegerField(max_length=1, choices=VM_STATES)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.vm_name

    # Insert/Update statement
    def save(self, **kwargs):
	# Connect to xenserver
	session = XenAPI.Session(XEN_URL)
        session.xenapi.login_with_password(XEN_USER, XEN_PWD)
        # Insert
        if self.pk is None: 
	    # Create VM in XenServer
            template = session.xenapi.VM.get_by_name_label(str(self.vm_template.vm_template_name))[0]
            session.xenapi.VM.clone(template, str(self.vm_name))
            # Create VM node in Puppet-Dashboard
            cur = None
            conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DASHBOARD_DB)
            try:
                cur = conn.cursor()
                query  = 'INSERT INTO nodes (name, created_at, updated_at) VALUES ("' + self.vm_name + '", sysdate(), sysdate())'
                cur.execute(query)
                #cur.execute('INSERT INTO nodes (name, description, created_at, updated_at) VALUES ("vm01", "my VM 01", sysdate(), sysdate())')
                conn.commit()
            finally:
                if cur:
                    cur.close()
                conn.close()
        # Update
        vm = session.xenapi.VM.get_by_name_label(str(self.vm_name))[0]
        state = session.xenapi.VM.get_record(vm)
	# Start VM
	if self.vm_state == 1: 
            if state["power_state"] == "Halted":
                session.xenapi.VM.start(vm, False, True)
            elif state["power_state"] == "Paused":
                session.xenapi.VM.unpause(vm)
            elif state["power_state"] == "Suspended":
                session.xenapi.VM.resume(vm, False, True)
        # Stop VM
	else: 
            if state["power_state"] == "Suspended":
                session.xenapi.VM.resume(vm, False, True)
                session.xenapi.VM.clean_shutdown(vm)
            elif state["power_state"] == "Paused":
                session.xenapi.VM.unpause(vm)
                session.xenapi.VM.clean_shutdown(vm)
            elif state["power_state"] == "Running":
                session.xenapi.VM.clean_shutdown(vm)
        super(Vm, self).save()

    # Delete statement -> delete VM
    def delete(self):
	# Delete from XenServer
	session = XenAPI.Session(XEN_URL)
        session.xenapi.login_with_password(XEN_USER, XEN_PWD)
        vm = session.xenapi.VM.get_by_name_label(str(self.vm_name))[0]
        session.xenapi.VM.destroy(vm)
	session.xenapi.session.logout()
	# Delete from Puppet-Dashboard
        cur = None
        conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DASHBOARD_DB)
        try:
            # get vm id
            cur = conn.cursor()
            cur.execute("SELECT id FROM nodes WHERE name = %s LIMIT 1" % conn.escape(self.vm_name))
            r = cur.fetchone()
            cur.close()
            # Delete
            cur = conn.cursor()
            query = 'DELETE FROM node_class_memberships WHERE node_id = "' + str(r[0]) + '"'
            cur.execute(query)
            cur.close()
            cur = conn.cursor()
            query = 'DELETE FROM nodes WHERE name = "' + self.vm_name + '"'
            cur.execute(query)
            conn.commit()
        finally:
            if cur:
                cur.close()
            conn.close()
	super(Vm, self).delete()

    # VM IP address
    def vm_ip(self):
	session = XenAPI.Session(XEN_URL)
        session.xenapi.login_with_password(XEN_USER, XEN_PWD)
        vm = session.xenapi.VM.get_by_name_label(str(self.vm_name))[0]
        vgm = session.xenapi.VM.get_guest_metrics(vm)
        try:
            os = session.xenapi.VM_guest_metrics.get_networks(vgm)
            if "0/ip" in os.keys():
                return os["0/ip"]
            return None
        except:
            return None
	finally:
	    session.xenapi.session.logout()

    # VM state information
    def vm_info(self):
	session = XenAPI.Session(XEN_URL)
        session.xenapi.login_with_password(XEN_USER, XEN_PWD)
        vm = session.xenapi.VM.get_by_name_label(str(self.vm_name))[0]
        state = session.xenapi.VM.get_record(vm)
	session.xenapi.session.logout()
        return state["power_state"]

