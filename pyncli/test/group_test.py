# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        group_test
# Purpose:      tests
#
# Author:      Evgeniy Semenov
#
# Created:     04.03.2017
# Copyright:   (c) Evgeniy Semenov 2017-2019
# Licence:     MIT
#-------------------------------------------------------------------------------

import unittest
import os

pd=os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
os.sys.path.insert(0,pd)
from pyncli.ldap.group import group
from pyncli.ldap.admexept import NotEnoughParams, EmptyParam, WrongParam, TooLong

class TestGropMetods(unittest.TestCase):

    def test___init_1(self):
        self.assertRaises(EmptyParam,group,u'',u'')

    def _test___init_2(self):
        self.assertRaises(EmptyParam,group,u'some_group',u'')

    def _test___init_3(self):
        self.assertRaises(TooLong,group,u'some_group',u'ou=some_ou,dc=example,dc=com',description=u'x'*1025)

    def test___init_4(self):
        u=group(u'some_group',org_unit=u'ou=some_ou,dc=example,dc=com')
        self.assertEqual(u.__class__.__name__,u'group') #description


    def test___init_5(self):
        self.assertRaises(TooLong,group,u'ю'*65,u'ou=some_ou,dc=example,dc=com')

    def test___init_6(self):
        self.assertRaises(TooLong,group,u'ю'*5,u'й'*1025)

##    @unittest.expectedFailure # does unittest change setattr?
##    def test_setattr_1(self):
##        grp=group(u'some_group',org_unit=u'ou=some_ou,dc=example,dc=com',description=u'Группа тестов')
##        grp.name='New group'
##        self.assertEqual(grp.name, u'New group')
##        self.assertEqual(grp.org_unit,u'ou=some_ou,dc=example,dc=com')
##        self.assertEqual(grp.dn,u'CN=New group,ou=some_ou,dc=example,dc=com')


class TestGropMetods2(unittest.TestCase):

    def setUp(self):
        self.group=group(u'some_group',org_unit=u'ou=some_ou,dc=example,dc=com',description=u'Группа тестов')

    def tearDown(self):
        self.group=None

    def test___init_7(self):
        self.assertEqual(self.group.__class__.__name__,u'group')


    def test___init_8(self):
        self.assertEqual(self.group.name,u'some_group')

    def test___init_9(self):
        self.assertEqual(self.group.org_unit,u'ou=some_ou,dc=example,dc=com')


    def test___init_10(self):
        self.assertEqual(self.group.dn,u'CN=some_group,ou=some_ou,dc=example,dc=com')

    def test___init_11(self):
        self.assertEqual(self.group.get_dn(),u'CN=some_group,ou=some_ou,dc=example,dc=com')

    def test___init_12(self):
        self.assertEqual(self.group.description,u'Группа тестов')

    def test___init_13(self):
        cr=u"INSERT INTO 'test'('description', 'dn', 'name', 'org_unit') VALUES ('Группа тестов', 'CN=some_group,ou=some_ou,dc=example,dc=com', 'some_group', 'ou=some_ou,dc=example,dc=com');"
        self.assertEqual(self.group.get_sql_insert('test'),cr)

    def test___init_14(self):
        cr=u"CREATE TABLE 'test'( 'description' TEXT, 'dn' TEXT, 'name' TEXT PRIMARY KEY, 'org_unit' TEXT);"
        self.assertEqual(self.group.get_sql_create_table('test'),cr)

    def test_brief_1(self):
        self.assertEqual(self.group.brief,u"name: some_group (Группа тестов)")

if __name__ == '__main__':
    unittest.main()
