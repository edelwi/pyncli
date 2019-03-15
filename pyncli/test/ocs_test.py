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

pd=os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
os.sys.path.insert(0,pd)
import nc
from ocs.ocs import (PERMISSION_CREATE, PERMISSION_READ, PERMISSION_UPDATE,
                PERMISSION_DELETE, PERMISSION_SHARE, PERMISSION_ALL)
from pyncli.ocs import ocs

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

if __name__ == '__main__':
    unittest.main()
