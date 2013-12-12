import unittest
import XenAPI
from django.test import TestCase
from vm.models import Vm

# XenServer parameters
XEN_URL       = 'https://192.168.0.17:443/'
XEN_USER      = 'root'
XEN_PWD       = 'root'
XEN_TEMPLATE = 'debtest'
XEN_TEST_VM1 = 'testVm1'
XEN_TEST_VM2 = 'testVm2'
#XEN_TEST_VM3 = 'testVm3'

class VmTest(unittest.TestCase):

    def setUp(self):
        self.test_vm1 = Vm.objects.create(vm_name = XEN_TEST_VM1, vm_state = 0)
        self.test_vm2 = Vm.objects.create(vm_name = XEN_TEST_VM2, vm_state = 1)
#        self.test_vm3 = Vm.objects.create(vm_name = XEN_TEST_VM3, vm_state = 0)
#        self.test_vm3.delete()

    def tearDown(self):
        self.test_vm1.delete()
	# Shutdown and delete second VM
	session = XenAPI.Session(XEN_URL)
        session.xenapi.login_with_password(XEN_USER, XEN_PWD)
        vm2 = session.xenapi.VM.get_by_name_label(XEN_TEST_VM2)[0]
        session.xenapi.VM.shutdown(vm2)
        self.test_vm2.delete()

    def test_create_vm(self):
	# connect to xenserver
	session = XenAPI.Session(XEN_URL)
        session.xenapi.login_with_password(XEN_USER, XEN_PWD)
        vm1 = session.xenapi.VM.get_by_name_label(XEN_TEST_VM1)
        #vm = session.xenapi.VM.get_by_name_label("NotExistingVM")
	self.assertNotEqual([], vm1)

    def test_start_vm(self):
	# connect to xenserver
	session = XenAPI.Session(XEN_URL)
        session.xenapi.login_with_password(XEN_USER, XEN_PWD)
        vm2 = session.xenapi.VM.get_by_name_label(XEN_TEST_VM2)[0]
        state = session.xenapi.VM.get_record(vm2)
	self.assertEqual("Running", state["power_state"])

