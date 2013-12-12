import pymysql
from django.db import models
from vms.models import Vm

# MySQL parameters 
MYSQL_HOST         = "localhost"
MYSQL_PORT         = 3306
MYSQL_USER         = "dashboard"
MYSQL_PASSWD       = "mysql"
MYSQL_DASHBOARD_DB = "dashboard"

# Classes
#def enum(*sequential, **named):
#    enums = dict(zip(sequential, range(len(sequential))), **named)
#    return type('Enum', (), enums)

class ServiceTemplate(models.Model):
    service_template_name = models.CharField(max_length=50)
    def __unicode__(self):  # Python 3: def __str__(self):
        return self.service_template_name

class Service(models.Model):
    service_template = models.ForeignKey(ServiceTemplate)
    service_vm = models.ForeignKey(Vm)
    #SERVICE_STATES = (
    #    (0, 'Stop'),
    #    (1, 'Start'),
    #)
    #service_state = models.IntegerField(max_length=1, choices=SERVICE_STATES)

    def __unicode__(self):  # Python 3: def __str__(self):
        return self.service_template.service_template_name

    # Insert/Update statement
    def save(self, **kwargs):
	cur = None
        vm_id = 0
        conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DASHBOARD_DB)
	# Create Service
        try:
            if self.pk is None: 
                # get vm id
                cur = conn.cursor()
                cur.execute("SELECT id FROM nodes WHERE name = %s LIMIT 1" % conn.escape(self.service_vm.vm_name))
                r1 = cur.fetchone()
                #vm_id = r1[0]
                cur.close()
                # get service id
                cur = conn.cursor()
                cur.execute("SELECT id FROM node_classes WHERE name = %s LIMIT 1" % conn.escape(self.service_template.service_template_name))
                r2 = cur.fetchone()
                #service_id = r2[0]
                cur.close()
                # create
                cur = conn.cursor()
                query = 'INSERT INTO node_class_memberships (node_id, node_class_id, created_at, updated_at) VALUES ("' + str(r1[0]) + '", "' + str(r2[0]) + '", sysdate(), sysdate())'
                cur.execute(query)
                #cur.execute(" id FROM nodes_classes WHERE name = %s LIMIT 1" % conn.escape(self.service_template.service_template_name))
                conn.commit()
        finally:
            if cur:
                cur.close()
            conn.close()
        super(Service, self).save()

    # Delete statement -> delete Service
    def delete(self):
        cur = None
        conn = pymysql.connect(host=MYSQL_HOST, port=MYSQL_PORT, user=MYSQL_USER, passwd=MYSQL_PASSWD, db=MYSQL_DASHBOARD_DB)
        try:
            # get vm id
            cur = conn.cursor()
            cur.execute("SELECT id FROM nodes WHERE name = %s LIMIT 1" % conn.escape(self.service_vm.vm_name))
            r1 = cur.fetchone()
            cur.close()
            # get service id
            cur = conn.cursor()
            cur.execute("SELECT id FROM node_classes WHERE name = %s LIMIT 1" % conn.escape(self.service_template.service_template_name))
            r2 = cur.fetchone()
            cur.close()
            # create
            cur = conn.cursor()
            query = 'DELETE FROM node_class_memberships WHERE node_id = "' + str(r1[0]) + '" and node_class_id =  "' + str(r2[0]) + '"'
            cur.execute(query)
            #cur.execute(" id FROM nodes_classes WHERE name = %s LIMIT 1" % conn.escape(self.service_template.service_template_name))
            conn.commit()
        finally:
            if cur:
                cur.close()
            conn.close()
        super(Service, self).delete()

