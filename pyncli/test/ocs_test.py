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
from copy import deepcopy

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
        self.assertIsNone( ocs.human_size('ooo'))

    def test___human_permissions_0(self):
        self.assertIsNone( ocs.human_permissions('X'))

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

    def test__eq__0(self):
        self.assertEqual(self.g, ocs.Group(group_id=50,permissions=PERMISSION_ALL))

    def test__ne__0(self):
        self.assertNotEqual(self.g, ocs.Group(group_id=51,permissions=PERMISSION_ALL))

    def test__ne__1(self):
        self.assertNotEqual(self.g, ocs.Group(group_id=50,permissions=PERMISSION_READ))

    def test__ne__2(self):
        self.assertNotEqual(self.g, 'q')

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
            backend='Database', subadmin=[], quota=self.quota_1,
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
        self.assertListEqual( self.user.subadmin, [])

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

class TestUser3(unittest.TestCase):
    def setUp(self):
        self.grp_1 = ocs.Group('HR')
        self.grp_2 = ocs.Group('staff')
        self.quota_1 = ocs.UserQuota(quota=10737418240,used=2431492563,
                free=8305925677, total=10737418240, relative=22.65)
        self.bc = ocs.BackendCapabilities(setDisplayName=1, setPassword=1)
        self.user=ocs.User(id='alex', enabled=1,
            storageLocation='/home/nextcloud/alex@example.com',
            lastLogin=0,
            backend='Database', subadmin=['HR'], quota=self.quota_1,
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
        self.assertListEqual( self.user.subadmin, ['HR'])

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
	<Group> "HR" [Subadmin]
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

    def test_get_status(self):
        rsp=ocs.Ocs_xml(self.resp2,data_class_name='')
        self.assertEqual(rsp.get_status(), "Status: failure, code: 997, message: Current user is not logged in")

class TestOcs_xml_GroupFolder(unittest.TestCase):
    def setUp(self):
        self.resp = '''<ocs>
 <meta>
  <status>ok</status>
  <statuscode>100</statuscode>
  <message>OK</message>
  <totalitems></totalitems>
  <itemsperpage></itemsperpage>
 </meta>
 <data>
  <element>
   <id>1</id>
   <mount_point>{IT}</mount_point>
   <groups>
    <element group_id="IT" permissions="31"/>
   </groups>
   <quota>-3</quota>
   <size>39136618129</size>
  </element>
  <element>
   <id>2</id>
   <mount_point>{FIS}</mount_point>
   <groups>
    <element group_id="FIS" permissions="31"/>
   </groups>
   <quota>32212254720</quota>
   <size>11052652856</size>
  </element>
  <element>
   <id>19</id>
   <mount_point>{SECURITY}</mount_point>
   <groups>
    <element group_id="SECURITY" permissions="31"/>
   </groups>
   <quota>21474836480</quota>
   <size>6834174935</size>
  </element>
  <element>
   <id>22</id>
   <mount_point>{TEST_NC1}</mount_point>
   <groups>
    <element group_id="TEST_NC1" permissions="31"/>
   </groups>
   <quota>8589934592</quota>
   <size>113153</size>
  </element>
 </data>
</ocs>
'''
        self.obj=ocs.Ocs_xml(self.resp,data_class_name='GroupFolder')

    def tearDown(self):
        self.resp=None
        self.obj=None

    def test__init__0(self):
        gf1=ocs.GroupFolder(id='1',mount_point='{IT}',
            groups=[ocs.Group(group_id="IT",permissions=PERMISSION_ALL)],
            quota='-3',size='39136618129')
        gf2=ocs.GroupFolder(id='2',mount_point='{FIS}',
            groups=[ocs.Group(group_id="FIS",permissions=PERMISSION_ALL)],
            quota='32212254720',size='11052652856')
        gf3=ocs.GroupFolder(id='19',mount_point='{SECURITY}',
            groups=[ocs.Group(group_id="SECURITY",permissions=PERMISSION_ALL)],
            quota='21474836480',size='6834174935')
        gf4=ocs.GroupFolder(id='22',mount_point='{TEST_NC1}',
            groups=[ocs.Group(group_id="TEST_NC1",permissions=PERMISSION_ALL)],
            quota='8589934592',size='113153')

        self.assertEqual(self.obj.status,'ok')
        self.assertEqual(self.obj.statuscode,'100')
        self.assertEqual(self.obj.message,'OK')
        self.assertListEqual(self.obj.data, [gf1,gf2,gf3,gf4])

    def test__str__(self):
        st='''<Ocs_xml> ok (100): OK
<GroupFolder> (1) "{IT}" quota: -3, size: 36.45g
  <Group> "IT" [cruds]
<GroupFolder> (2) "{FIS}" quota: 30.00g, size: 10.29g
  <Group> "FIS" [cruds]
<GroupFolder> (19) "{SECURITY}" quota: 20.00g, size: 6.36g
  <Group> "SECURITY" [cruds]
<GroupFolder> (22) "{TEST_NC1}" quota: 8.00g, size: 110.50k
  <Group> "TEST_NC1" [cruds]\n'''
        self.assertEqual(str(self.obj),st)

class TestOcs_xml_Group(unittest.TestCase):
    def setUp(self):
        self.resp = '''<ocs>
 <meta>
  <status>ok</status>
  <statuscode>100</statuscode>
  <message>OK</message>
  <totalitems></totalitems>
  <itemsperpage></itemsperpage>
 </meta>
 <data>
  <groups>
   <element>FIS</element>
   <element>IT</element>
   <element>PHD</element>
   <element>SECURITY</element>
   <element>TEST_NC1</element>
  </groups>
 </data>
</ocs>
'''
        self.obj=ocs.Ocs_xml(self.resp,data_class_name='Group')

    def tearDown(self):
        self.resp=None
        self.obj=None

    def test__init__0(self):
        g1=ocs.Group(group_id="FIS")
        g2=ocs.Group(group_id="IT")
        g3=ocs.Group(group_id="PHD")
        g4=ocs.Group(group_id="SECURITY")
        g5=ocs.Group(group_id="TEST_NC1")
        self.assertEqual(self.obj.status,'ok')
        self.assertEqual(self.obj.statuscode,'100')
        self.assertEqual(self.obj.message,'OK')
        self.assertListEqual(self.obj.data, [g1,g2,g3,g4,g5])

    def test__str__(self):
        st='''<Ocs_xml> ok (100): OK
<Group> "FIS" [None]
<Group> "IT" [None]
<Group> "PHD" [None]
<Group> "SECURITY" [None]
<Group> "TEST_NC1" [None]\n'''
        self.assertEqual(str(self.obj),st)


class TestOcs_xml_CreateGroupFolder(unittest.TestCase):
    def setUp(self):
        self.resp = '''<ocs>
 <meta>
  <status>ok</status>
  <statuscode>100</statuscode>
  <message>OK</message>
  <totalitems></totalitems>
  <itemsperpage></itemsperpage>
 </meta>
 <data>
  <id>13</id>
  <groups/>
 </data>
</ocs>
'''
        self.obj=ocs.Ocs_xml(self.resp,data_class_name='CreateGroupFolder')

    def tearDown(self):
        self.resp=None
        self.obj=None

    def test__init__0(self):
        cgf=ocs.CreateGroupFolder(id="13")
        self.assertEqual(self.obj.status,'ok')
        self.assertEqual(self.obj.statuscode,'100')
        self.assertEqual(self.obj.message,'OK')
        self.assertListEqual(self.obj.data, [cgf])

    def test__str__(self):
        st='''<Ocs_xml> ok (100): OK
<CreateGroupFolder> id: 13\n'''
        self.assertEqual(str(self.obj),st)

class TestOcs_xml_GroupMembers(unittest.TestCase):
    def setUp(self):
        self.resp = '''<ocs>
 <meta>
  <status>ok</status>
  <statuscode>100</statuscode>
  <message>OK</message>
  <totalitems></totalitems>
  <itemsperpage></itemsperpage>
 </meta>
 <data>
  <users>
   <element>tester1@example.com</element>
   <element>tester2@example.com</element>
   <element>tester3@example.com</element>
   <element>tester4@example.com</element>
   <element>tester5@example.com</element>
  </users>
 </data>
</ocs>

'''
        self.obj=ocs.Ocs_xml(self.resp,data_class_name='GroupMembers')

    def tearDown(self):
        self.resp=None
        self.obj=None

    def test__init__0(self):
        u1=ocs.GroupMembers(user_id="tester1@example.com")
        u2=ocs.GroupMembers(user_id="tester2@example.com")
        u3=ocs.GroupMembers(user_id="tester3@example.com")
        u4=ocs.GroupMembers(user_id="tester4@example.com")
        u5=ocs.GroupMembers(user_id="tester5@example.com")

        self.assertEqual(self.obj.status,'ok')
        self.assertEqual(self.obj.statuscode,'100')
        self.assertEqual(self.obj.message,'OK')
        self.assertListEqual(self.obj.data, [u1,u2,u3,u4,u5])

    def test__str__(self):
        st='''<Ocs_xml> ok (100): OK
user_id: tester1@example.com
user_id: tester2@example.com
user_id: tester3@example.com
user_id: tester4@example.com
user_id: tester5@example.com\n'''
        self.assertEqual(str(self.obj),st)

class TestOcs_xml_GroupFolder_2(unittest.TestCase):
    def setUp(self):
        self.resp = '''<ocs>
 <meta>
  <status>ok</status>
  <statuscode>100</statuscode>
  <message>OK</message>
  <totalitems></totalitems>
  <itemsperpage></itemsperpage>
 </meta>
 <data>
  <id>13</id>
  <groups/>
 </data>
</ocs>
'''
        self.obj=ocs.Ocs_xml(self.resp,data_class_name='GroupFolder')

    def tearDown(self):
        self.resp=None
        self.obj=None

    def test__init__0(self):
        gf1=ocs.GroupFolder(id='13')
        self.assertEqual(self.obj.status,'ok')
        self.assertEqual(self.obj.statuscode,'100')
        self.assertEqual(self.obj.message,'OK')
        self.assertListEqual(self.obj.data, [gf1])

    def test__str__(self):
        st='''<Ocs_xml> ok (100): OK
<GroupFolder> (13) "None" quota: None, size: None\n'''
        self.assertEqual(str(self.obj),st)

class TestOcs_xml_User(unittest.TestCase):
    def setUp(self):
        self.resp = '''<ocs>
 <meta>
  <status>ok</status>
  <statuscode>100</statuscode>
  <message>OK</message>
  <totalitems></totalitems>
  <itemsperpage></itemsperpage>
 </meta>
 <data>
  <enabled>1</enabled>
  <id>tester1@example.com</id>
  <storageLocation>/home/nextcloud/tester1@example.com</storageLocation>
  <lastLogin>1544530113000</lastLogin>
  <backend>LDAP</backend>
  <subadmin/>
  <quota>
   <free>8305925677</free>
   <used>2431492563</used>
   <total>10737418240</total>
   <relative>22.65</relative>
   <quota>10737418240</quota>
  </quota>
  <email/>
  <displayname>Пупкин Василий Алибабаевич</displayname>
  <phone>+3333333333</phone>
  <address>Russia, St. Petersburg</address>
  <website>https://www.example.com</website>
  <twitter>@_twitt_me_</twitter>
  <groups>
   <element>testers</element>
   <element>staff</element>
  </groups>
  <language>ru</language>
  <locale></locale>
  <backendCapabilities>
   <setDisplayName></setDisplayName>
   <setPassword></setPassword>
  </backendCapabilities>
 </data>
</ocs>

'''
        self.obj=ocs.Ocs_xml(self.resp,data_class_name='User')

    def tearDown(self):
        self.resp=None
        self.obj=None

    def test__init__0(self):
        user1=ocs.User(id='tester1@example.com', enabled='1',
            storageLocation='/home/nextcloud/tester1@example.com',
            lastLogin='1544530113000',
            backend='LDAP', subadmin=[],
            quota=ocs.UserQuota(quota='10737418240',used='2431492563',
                free='8305925677', total='10737418240', relative='22.65') ,
            email=None, displayname='Пупкин Василий Алибабаевич',
            phone='+3333333333', address='Russia, St. Petersburg',
            website='https://www.example.com', twitter='@_twitt_me_',
            groups=[ocs.Group('testers'),ocs.Group('staff')],
            language='ru', locale=None,
            backendCapabilities=ocs.BackendCapabilities(setDisplayName=None,
                setPassword=None)
            )

        self.assertEqual(self.obj.status,'ok')
        self.assertEqual(self.obj.statuscode,'100')
        self.assertEqual(self.obj.message,'OK')
        self.assertListEqual(self.obj.data, [user1])

    def test__str__(self):
        st='''<Ocs_xml> ok (100): OK
<User> (tester1@example.com) "Пупкин Василий Алибабаевич" enabled: True, e-mail: None
	backend: LDAP, storage location: /home/nextcloud/tester1@example.com, last logon: 2018-12-11T15:08:33
	quota: Quota: 10.00g, used: 2.26g, free: 7.74g, total: 10.00g, relative: 22.65
	phone: +3333333333, twitter: @_twitt_me_, website: https://www.example.com
	address: Russia, St. Petersburg
	language: ru, locale: None
	<Group> "testers"
	<Group> "staff"
	<BackendCapabilities> setDisplayName: False,  setPassword: False\n'''
        self.assertEqual(str(self.obj),st)

class TestOcs_xml_Apps(unittest.TestCase):
    def setUp(self):
        self.resp = '''<ocs>
 <meta>
  <status>ok</status>
  <statuscode>100</statuscode>
  <message>OK</message>
  <totalitems></totalitems>
  <itemsperpage></itemsperpage>
 </meta>
 <data>
  <apps>
   <element>encryption</element>
   <element>theming</element>
   <element>nextcloud_announcements</element>
   <element>files_trashbin</element>
   <element>files_pdfviewer</element>
   <element>files_texteditor</element>
   <element>notifications</element>
   <element>comments</element>
   <element>files_external</element>
   <element>activity</element>
   <element>survey_client</element>
   <element>systemtags</element>
   <element>accessibility</element>
   <element>updatenotification</element>
   <element>serverinfo</element>
   <element>admin_audit</element>
   <element>files_sharing</element>
   <element>password_policy</element>
   <element>federation</element>
   <element>gallery</element>
   <element>user_ldap</element>
   <element>sharebymail</element>
   <element>files_versions</element>
   <element>logreader</element>
   <element>firstrunwizard</element>
   <element>support</element>
   <element>files_videoplayer</element>
   <element>bruteforcesettings</element>
   <element>calendar</element>
   <element>user_saml</element>
   <element>user_external</element>
   <element>tasks</element>
   <element>notes</element>
   <element>groupfolders</element>
   <element>contacts</element>
  </apps>
 </data>
</ocs>
'''
        self.obj=ocs.Ocs_xml(self.resp,data_class_name='Apps')

    def tearDown(self):
        self.resp=None
        self.obj=None

    def test__init__0(self):
        apps1=['encryption','theming','nextcloud_announcements','files_trashbin',
            'files_pdfviewer','files_texteditor','notifications','comments',
            'files_external','activity','survey_client','systemtags',
            'accessibility','updatenotification','serverinfo','admin_audit',
            'files_sharing','password_policy','federation','gallery',
            'user_ldap','sharebymail','files_versions','logreader',
            'firstrunwizard','support','files_videoplayer','bruteforcesettings',
            'calendar','user_saml','user_external','tasks','notes',
            'groupfolders','contacts',]

        self.assertEqual(self.obj.status,'ok')
        self.assertEqual(self.obj.statuscode,'100')
        self.assertEqual(self.obj.message,'OK')
        self.assertListEqual(self.obj.data, apps1)

    def test__str__(self):
        st='''<Ocs_xml> ok (100): OK
encryption
theming
nextcloud_announcements
files_trashbin
files_pdfviewer
files_texteditor
notifications
comments
files_external
activity
survey_client
systemtags
accessibility
updatenotification
serverinfo
admin_audit
files_sharing
password_policy
federation
gallery
user_ldap
sharebymail
files_versions
logreader
firstrunwizard
support
files_videoplayer
bruteforcesettings
calendar
user_saml
user_external
tasks
notes
groupfolders
contacts\n'''
        self.assertEqual(str(self.obj),st)

class TestOcs_xml_Subadmins(unittest.TestCase):
    def setUp(self):
        self.resp = '''<ocs>
 <meta>
  <status>ok</status>
  <statuscode>100</statuscode>
  <message>OK</message>
  <totalitems></totalitems>
  <itemsperpage></itemsperpage>
 </meta>
 <data>
  <element>admin@example.com</element>
  <element>admin2@example.com</element>
 </data>
</ocs>

'''
        self.obj=ocs.Ocs_xml(self.resp,data_class_name='Subadmins')

    def tearDown(self):
        self.resp=None
        self.obj=None

    def test__init__0(self):
        admins=['admin@example.com','admin2@example.com']
        self.assertEqual(self.obj.status,'ok')
        self.assertEqual(self.obj.statuscode,'100')
        self.assertEqual(self.obj.message,'OK')
        self.assertListEqual(self.obj.data, admins)

    def test__str__(self):
        st='''<Ocs_xml> ok (100): OK
admin@example.com
admin2@example.com\n'''
        self.assertEqual(str(self.obj),st)

if __name__ == '__main__':
    unittest.main()
