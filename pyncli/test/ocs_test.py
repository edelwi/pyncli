# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        ocs_test
# Purpose:      tests
#
# Author:      Evgeniy Semenov
#
# Created:     15.03.2019
# Copyright:   (c) Evgeniy Semenov 2019
# Licence:     MIT
#-------------------------------------------------------------------------------

import unittest
import os
from datetime import datetime

pd=os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
os.sys.path.insert(0,pd)
import nc
from ocs.ocs import (PERMISSION_CREATE, PERMISSION_READ, PERMISSION_UPDATE,
                PERMISSION_DELETE, PERMISSION_SHARE, PERMISSION_ALL)
from pyncli.ocs import ocs
from pyncli.ldap.admexept import AdminException, OperationFailure, WrongParam

class TestFuncs(unittest.TestCase):

    def test___human_size_0(self):
        self.assertEqual( ocs.human_size(100),'100')

    def test___human_size_1(self):
        self.assertEqual( ocs.human_size(1000),'1000')

    def test___human_size_2(self):
        self.assertEqual( ocs.human_size(10000),'9.77k')

    def test___human_size_3(self):
        self.assertEqual( ocs.human_size(100000),'97.66k')

    def test___human_size_4(self):
        self.assertEqual( ocs.human_size(1000000),'976.56k')

    def test___human_size_5(self):
        self.assertEqual( ocs.human_size(10000000),'9.54m')

    def test___human_size_6(self):
        self.assertEqual( ocs.human_size(100000000),'95.37m')

    def test___human_size_7(self):
        self.assertEqual( ocs.human_size(1000000000),'953.67m')

    def test___human_size_8(self):
        self.assertEqual( ocs.human_size(10000000000),'9.31g')

    def test___human_size_9(self):
        self.assertEqual( ocs.human_size(100000000000),'93.13g')

    def test___human_size_10(self):
        self.assertEqual( ocs.human_size(1000000000000),'931.32g')

    def test___human_size_11(self):
        self.assertEqual( ocs.human_size(10000000000000),'9.09t')

    def test___human_size_12(self):
        self.assertEqual( ocs.human_size(100000000000000),'90.95t')

    def test___human_size_13(self):
        self.assertEqual( ocs.human_size(1000000000000000),'909.49t')

    def test___human_size_14(self):
        self.assertEqual( ocs.human_size(10000000000000000),'9094.95t')

    def test___human_size_15(self):
        self.assertEqual( ocs.human_size('ooo'),'ooo')

    def test___human_permissions_0(self):
        self.assertEqual( ocs.human_permissions('X'),'')

    def test___human_permissions_1(self):
        self.assertEqual( ocs.human_permissions(-3),'')

    def test___human_permissions_2(self):
        self.assertEqual( ocs.human_permissions(33),'')

    def test___human_permissions_3(self):
        for k,v in ocs.PERMISSIONS.items():
            self.assertEqual( ocs.human_permissions(v),k)

    def test___human_permissions_4(self):
        self.assertEqual( ocs.human_permissions(3),
            'PERMISSION_READ | PERMISSION_UPDATE')

    def test___human_permissions_5(self):
        self.assertEqual( ocs.human_permissions(5),
            'PERMISSION_CREATE | PERMISSION_READ')

    def test___human_permissions_6(self):
        self.assertEqual( ocs.human_permissions(9),
            'PERMISSION_READ | PERMISSION_DELETE')

    def test___human_permissions_7(self):
        self.assertEqual( ocs.human_permissions(17),
            'PERMISSION_READ | PERMISSION_SHARE')

    def test___human_permissions_8(self):
        self.assertEqual( ocs.human_permissions(31),
            'PERMISSION_CREATE | PERMISSION_READ | PERMISSION_UPDATE | PERMISSION_DELETE | PERMISSION_SHARE')

    def test___human_permissions_9(self):
        self.assertEqual( ocs.human_permissions(3,short=True),'ru')

    def test___human_permissions_10(self):
        self.assertEqual( ocs.human_permissions(6,short=True),'cu')

    def test___human_permissions_11(self):
        self.assertEqual( ocs.human_permissions(7,short=True), 'cru')

    def test___human_permissions_12(self):
        self.assertEqual( ocs.human_permissions(10,short=True), 'ud')

    def test___human_permissions_13(self):
        self.assertEqual( ocs.human_permissions(31,short=True), 'cruds')

class TestGroupMembers(unittest.TestCase):
    def setUp(self):
        self.gm=ocs.GroupMembers('member')

    def tearDown(self):
        self.gm=None

    def test___init__0(self):
        self.assertEqual( self.gm.user_id, 'member')

    def test___str__0(self):
        self.assertEqual( str(self.gm), 'user_id: member')

class TestCreateGroupFolder(unittest.TestCase):
    def setUp(self):
        self.cgf=ocs.CreateGroupFolder(10)

    def tearDown(self):
        self.cgf=None

    def test___init__0(self):
        self.assertEqual( self.cgf.id, 10)

    def test___str__0(self):
        self.assertEqual( str(self.cgf), '<CreateGroupFolder> id: 10')

class TestGroup(unittest.TestCase):
    def setUp(self):
        self.g=ocs.Group(group_id=50,permissions=PERMISSION_ALL)

    def tearDown(self):
        self.g=None

    def test___init__0(self):
        self.assertEqual( self.g.group_id, 50)
        self.assertEqual( self.g.permissions, 31)

    def test___str__0(self):
        self.assertEqual( str(self.g), '<Group> "50" [cruds]')

    def test___info__0(self):
        self.assertEqual( self.g.info, '<Group> "50"')

class TestGroupFolder(unittest.TestCase):
    def setUp(self):
        self.gf=ocs.GroupFolder(id=10,mount_point='share',groups=['IT','Admins'], quota=-3, size=54546540)

    def tearDown(self):
        self.gf=None

    def test___init__0(self):
        self.assertEqual( self.gf.id, 10)
        self.assertEqual( self.gf.mount_point, 'share')
        self.assertListEqual( self.gf.groups, ['IT','Admins'])
        self.assertEqual( self.gf.quota, -3)
        self.assertEqual( self.gf.size, 54546540)

    def test___str__0(self):
        self.assertEqual( str(self.gf), '''<GroupFolder> (10) "share" quota: -3, size: 52.02m
  IT
  Admins''')


class TestUser(unittest.TestCase):
    def setUp(self):
        self.grp_1 = ocs.Group('IT')
        self.grp_2 = ocs.Group('tester')
        self.user=ocs.User(id='user', enabled=True,
            storageLocation='/home/nextcloud/user@example.com',
            lastLogin='1544530113000',
            backend='LDAP', subadmin=[], quota=None, email='user@example.com',
            displayname='Pupkin Vasiliy', phone='+79010010101',
            address='Russia, Sochi', website='https://www.leningrad.spb.ru',
            twitter='@new_account', groups=[self.grp_1, self.grp_2],
            language='ru', locale='ru', backendCapabilities=None)

    def tearDown(self):
        self.user=None
        self.grp_1=None
        self.grp_2=None

    def test___init__0(self):
        self.assertEqual( self.user.id, 'user')
        self.assertEqual( self.user.enabled, True)
        self.assertEqual( self.user.storage_location,
            '/home/nextcloud/user@example.com')
        self.assertEqual( self.user.last_login,
            datetime(2018, 12, 11, 15, 8, 33))
        self.assertEqual( self.user.backend, 'LDAP')
        self.assertListEqual( self.user.subadmin, [])

        #self.assertEqual( self.user.quota, ocs.UserQuota(-3))  #!
        self.assertIsNone( self.user.quota)
        self.assertEqual( self.user.email, 'user@example.com')
        self.assertEqual( self.user.displayname, 'Pupkin Vasiliy')
        self.assertEqual( self.user.website, 'https://www.leningrad.spb.ru')
        self.assertEqual( self.user.twitter, '@new_account')
        self.assertListEqual( self.user.groups,
            [self.grp_1, self.grp_2])
        self.assertEqual( self.user.language, 'ru')
        self.assertEqual( self.user.locale, 'ru')
        self.assertIsNone( self.user.backend_capabilities)


    def test___str__0(self):
        self.assertEqual( str(self.user), '''<User> (user) "Pupkin Vasiliy" enabled: True, e-mail: user@example.com
	backend: LDAP, storage location: /home/nextcloud/user@example.com, last logon: 2018-12-11T15:08:33
	quota: None	phone: +79010010101, twitter: @new_account, website: https://www.leningrad.spb.ru
	address: Russia, Sochi
	language: ru, locale: ru
	<Group> "IT"
	<Group> "tester"
	None''')

class TestUser2(unittest.TestCase):
    def setUp(self):
        self.grp_1 = ocs.Group('HR')
        self.grp_2 = ocs.Group('staff')
        self.quota_1 = ocs.UserQuota(quota=10737418240,used=2431492563,
                free=8305925677, total=10737418240, relative=22.65)
        self.bc = ocs.BackendCapabilities(setDisplayName=1, setPassword=1)
        self.user=ocs.User(id='alex', enabled=1,
            storageLocation='/home/nextcloud/alex@example.com',
            lastLogin=0,
            backend='Database', subadmin=[self.grp_1], quota=self.quota_1,
            email='alex_hr@example.com',
            displayname='Ivanov Alex', phone='+79010010102',
            address='Russia, Surgut', website='https://www.example.ru',
            twitter='@alex_hr', groups=[self.grp_1, self.grp_2],
            language='en', locale='en',
            backendCapabilities=self.bc
            )

    def tearDown(self):
        self.user=None
        self.grp_1=None
        self.grp_2=None
        self.quota_1=None
        self.bc

    def test___init__0(self):

        self.assertEqual( self.user.id, 'alex')
        self.assertEqual( self.user.enabled, True)
        self.assertEqual( self.user.storage_location,
            '/home/nextcloud/alex@example.com')
        self.assertEqual( self.user.last_login,
            datetime(1970, 1, 1, 0, 0))
        self.assertEqual( self.user.backend, 'Database')
        self.assertListEqual( self.user.subadmin, [self.grp_1])

        self.assertEqual( self.user.quota, self.quota_1)
        self.assertEqual( self.user.email, 'alex_hr@example.com')
        self.assertEqual( self.user.displayname, 'Ivanov Alex')
        self.assertEqual( self.user.website, 'https://www.example.ru')
        self.assertEqual( self.user.twitter, '@alex_hr')
        self.assertListEqual( self.user.groups,
            [self.grp_1, self.grp_2])
        self.assertEqual( self.user.language, 'en')
        self.assertEqual( self.user.locale, 'en')
        self.assertEqual( self.user.backend_capabilities, self.bc)

    def test___str__0(self):
        self.assertEqual( str(self.user), '''<User> (alex) "Ivanov Alex" enabled: True, e-mail: alex_hr@example.com
	backend: Database, storage location: /home/nextcloud/alex@example.com, last logon: 1970-01-01T00:00:00
	quota: Quota: 10.00g, used: 2.26g, free: 7.74g, total: 10.00g, relative: 22.65
	phone: +79010010102, twitter: @alex_hr, website: https://www.example.ru
	address: Russia, Surgut
	language: en, locale: en
	<Group> "HR"
	<Group> "staff"
	<BackendCapabilities> setDisplayName: True,  setPassword: True''')

class TestUserQuota(unittest.TestCase):
    def setUp(self):
        self.quota = ocs.UserQuota(quota=10737418240,used=2431492563,
                free=8305925677, total=10737418240, relative=22.65)

    def tearDown(self):
        self.quota=None

    def test___init__0(self):
        self.assertEqual( self.quota.quota, 10737418240)
        self.assertEqual( self.quota.used, 2431492563)
        self.assertEqual( self.quota.free, 8305925677)
        self.assertEqual( self.quota.total, 10737418240)
        self.assertEqual( self.quota.relative, 22.65)

    def test___str__0(self):
        self.assertEqual( str(self.quota), '''Quota: 10.00g, used: 2.26g, free: 7.74g, total: 10.00g, relative: 22.65\n''')

class TestUserQuota2(unittest.TestCase):
    def setUp(self):
        self.quota = ocs.UserQuota(quota=5368709120,used=0,
                free=5368709120, total=5368709120, relative=0)

    def tearDown(self):
        self.quota=None

    def test___init__0(self):
        self.assertEqual( self.quota.quota, 5368709120)
        self.assertEqual( self.quota.used, 0)
        self.assertEqual( self.quota.free, 5368709120)
        self.assertEqual( self.quota.total, 5368709120)
        self.assertEqual( self.quota.relative, 0)

    def test___str__0(self):
        self.assertEqual( str(self.quota), '''Quota: 5.00g, used: 0, free: 5.00g, total: 5.00g\n''')

class TestBackendCapabilities(unittest.TestCase):
    def setUp(self):
        self.bc = ocs.BackendCapabilities(setDisplayName=1, setPassword=1)

    def tearDown(self):
        self.bc=None

    def test___init__0(self):
        self.assertTrue( self.bc.set_display_name)
        self.assertTrue( self.bc.set_password)

    def test___str__0(self):
        self.assertEqual( str(self.bc), '''<BackendCapabilities> setDisplayName: True,  setPassword: True''')

class TestBackendCapabilities2(unittest.TestCase):
    def setUp(self):
        self.bc = ocs.BackendCapabilities()

    def tearDown(self):
        self.bc=None

    def test___init__0(self):
        self.assertFalse( self.bc.set_display_name)
        self.assertFalse( self.bc.set_password)

    def test___str__0(self):
        self.assertEqual( str(self.bc), '''<BackendCapabilities> setDisplayName: False,  setPassword: False''')

class TestOcs_xml(unittest.TestCase):
    def setUp(self):
        self.resp = '''<ocs>
 <meta>
  <status>ok</status>
  <statuscode>100</statuscode>
  <message>OK</message>
  <totalitems></totalitems>
  <itemsperpage></itemsperpage>
 </meta>
 <data/>
</ocs>
'''
        self.resp2= '''<ocs>
 <meta>
  <status>failure</status>
  <statuscode>997</statuscode>
  <message>Current user is not logged in</message>
  <totalitems></totalitems>
  <itemsperpage></itemsperpage>
 </meta>
 <data/>
</ocs>
'''
    def tearDown(self):
        self.resp=None
        self.resp2=None

    def test__init__0(self):
        self.assertRaises(WrongParam,ocs.Ocs_xml,self.resp,data_class_name='WrongClassName')

    def test__init__1(self):
        self.assertRaises(WrongParam,ocs.Ocs_xml,"",data_class_name='')

    def test__init__2(self):
        self.assertRaises(WrongParam,ocs.Ocs_xml,555,data_class_name='')

    def test__init__3(self):
        rsp=ocs.Ocs_xml(self.resp,data_class_name='')
        self.assertEqual(rsp.status,'ok')
        self.assertEqual(rsp.statuscode,'100')
        self.assertEqual(rsp.message,'OK')

    def test__init__4(self):
        rsp=ocs.Ocs_xml(self.resp2,data_class_name='')
        self.assertEqual(rsp.status,'failure')
        self.assertEqual(rsp.statuscode,'997')
        self.assertEqual(rsp.message,'Current user is not logged in')

if __name__ == '__main__':
    unittest.main()
