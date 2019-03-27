# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        protogroup_test
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
from pyncli.ldap.protogroup import protogroup
from pyncli.ldap.admexept import (
    NotEnoughParams,
    EmptyParam,
    WrongParam,
    TooLong,
)


class TestPGropMetods(unittest.TestCase):
    def test___init_1(self):
        self.assertRaises(EmptyParam, protogroup, "", "")

    def _test___init_2(self):
        self.assertRaises(EmptyParam, protogroup, "some_group", "")

    def test___init_4(self):
        u = protogroup("some_group", org_unit="ou=some_ou,dc=example,dc=com")
        self.assertEqual(u.__class__.__name__, "protogroup")

    def test___init_5(self):
        self.assertRaises(
            TooLong, protogroup, "ю" * 65, "ou=some_ou,dc=example,dc=com"
        )

    def test___init_6(self):
        self.assertRaises(TooLong, protogroup, "ю" * 5, "й" * 1025)


class TestPGropMetods2(unittest.TestCase):
    def setUp(self):
        self.protogroup = protogroup(
            "some_group", org_unit="ou=some_ou,dc=example,dc=com"
        )

    def tearDown(self):
        self.protogroup = None

    def test___init_7(self):
        self.assertEqual(self.protogroup.__class__.__name__, "protogroup")

    def test___init_8(self):
        self.assertEqual(self.protogroup.name, "some_group")

    def test___init_9(self):
        self.assertEqual(
            self.protogroup.org_unit, "ou=some_ou,dc=example,dc=com"
        )

    def test___init_10(self):
        self.assertEqual(
            self.protogroup.dn, "CN=some_group,ou=some_ou,dc=example,dc=com"
        )

    def test___init_11(self):
        self.assertEqual(
            self.protogroup.get_dn(),
            "CN=some_group,ou=some_ou,dc=example,dc=com",
        )


if __name__ == "__main__":
    unittest.main()
