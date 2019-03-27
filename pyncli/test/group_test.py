# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        group_test
# Purpose:      tests
#
# Author:      Evgeniy Semenov
#
# Created:     04.03.2017
# Copyright:   (c) Evgeniy Semenov 2017-2019
# Licence:     MIT
# -------------------------------------------------------------------------------

import unittest
import os

pd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, pd)
from pyncli.ldap.group import group
from pyncli.ldap.admexept import (
    NotEnoughParams,
    EmptyParam,
    WrongParam,
    TooLong,
)


class TestGropMetods(unittest.TestCase):
    def test___init_1(self):
        self.assertRaises(EmptyParam, group, "", "")

    def _test___init_2(self):
        self.assertRaises(EmptyParam, group, "some_group", "")

    def _test___init_3(self):
        self.assertRaises(
            TooLong,
            group,
            "some_group",
            "ou=some_ou,dc=example,dc=com",
            description="x" * 1025,
        )

    def test___init_4(self):
        u = group("some_group", org_unit="ou=some_ou,dc=example,dc=com")
        self.assertEqual(u.__class__.__name__, "group")  # description

    def test___init_5(self):
        self.assertRaises(
            TooLong, group, "ю" * 65, "ou=some_ou,dc=example,dc=com"
        )

    def test___init_6(self):
        self.assertRaises(TooLong, group, "ю" * 5, "й" * 1025)


##    @unittest.expectedFailure # does unittest change setattr?
##    def test_setattr_1(self):
##        grp=group(u'some_group',org_unit=u'ou=some_ou,dc=example,dc=com',description=u'Группа тестов')
##        grp.name='New group'
##        self.assertEqual(grp.name, u'New group')
##        self.assertEqual(grp.org_unit,u'ou=some_ou,dc=example,dc=com')
##        self.assertEqual(grp.dn,u'CN=New group,ou=some_ou,dc=example,dc=com')


class TestGropMetods2(unittest.TestCase):
    def setUp(self):
        self.group = group(
            "some_group",
            org_unit="ou=some_ou,dc=example,dc=com",
            description="Группа тестов",
        )

    def tearDown(self):
        self.group = None

    def test___init_7(self):
        self.assertEqual(self.group.__class__.__name__, "group")

    def test___init_8(self):
        self.assertEqual(self.group.name, "some_group")

    def test___init_9(self):
        self.assertEqual(self.group.org_unit, "ou=some_ou,dc=example,dc=com")

    def test___init_10(self):
        self.assertEqual(
            self.group.dn, "CN=some_group,ou=some_ou,dc=example,dc=com"
        )

    def test___init_11(self):
        self.assertEqual(
            self.group.get_dn(), "CN=some_group,ou=some_ou,dc=example,dc=com"
        )

    def test___init_12(self):
        self.assertEqual(self.group.description, "Группа тестов")

    def test___init_13(self):
        cr = "INSERT INTO 'test'('description', 'dn', 'name', 'org_unit') VALUES ('Группа тестов', 'CN=some_group,ou=some_ou,dc=example,dc=com', 'some_group', 'ou=some_ou,dc=example,dc=com');"
        self.assertEqual(self.group.get_sql_insert("test"), cr)

    def test___init_14(self):
        cr = "CREATE TABLE 'test'( 'description' TEXT, 'dn' TEXT, 'name' TEXT PRIMARY KEY, 'org_unit' TEXT);"
        self.assertEqual(self.group.get_sql_create_table("test"), cr)

    def test_brief_1(self):
        self.assertEqual(self.group.brief, "name: some_group (Группа тестов)")


if __name__ == "__main__":
    unittest.main()
