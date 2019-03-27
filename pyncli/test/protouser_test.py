# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        protouser_test
# Purpose:      tests
#
# Author:      Evgeniy Semenov
#
# Created:     27.01.2017
# Copyright:   (c) sem 2017-2019
# Licence:     MIT
# -------------------------------------------------------------------------------

import unittest
import os

pd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, pd)
from pyncli.ldap import protouser
from pyncli.ldap.admexept import (
    NotEnoughParams,
    EmptyParam,
    WrongParam,
    TooLong,
)


class TestUserMetods(unittest.TestCase):
    def test___init_1(self):
        self.assertRaises(EmptyParam, protouser.protouser, "")

    ##    def _test___init_2(self):
    ##        self.assertRaises(EmptyParam,protouser.protouser,u'Пупкин',u'')

    ##    @unittest.skip(u"преобразование в unicode похоже работает")
    ##    def test___init_3(self):
    ##        self.assertRaises(WrongParam,protouser.protouser,'Пупкин','126546')

    def test___init_4(self):
        u = protouser.protouser("pupok")
        self.assertEqual(u.__class__.__name__, "protouser")

    def test___init_5(self):
        self.assertRaises(TooLong, protouser.protouser, "ю" * 65)


##    def _test___init_6(self):
##        self.assertRaises(TooLong,protouser.protouser,u'ю'*5,u'й'*256)


class TestUserMetods2(unittest.TestCase):
    def setUp(self):
        self.protouser = protouser.protouser("pupok")

    def tearDown(self):
        self.protouser = None

    def test___init_5(self):
        self.assertEqual(self.protouser.__class__.__name__, "protouser")

    def test___init_6(self):
        self.assertEqual(self.protouser.login, "pupok")

    ##    def test___init_7(self):
    ##        self.assertEqual(self.protouser.uid,u'45564')

    def test___eq_1(self):
        u = protouser.protouser("pupok")
        self.assertEqual(self.protouser, u)

    def test___eq_2(self):
        u = protouser.protouser("pupok")
        self.assertTrue(self.protouser == u)

    def test___eq_3(self):
        u = protouser.protouser("1pupok")
        self.assertFalse(self.protouser == u)

    def test___eq_4(self):
        u = protouser.protouser("upupok")
        self.assertFalse(self.protouser == u)

    def test___ne_1(self):
        u = protouser.protouser("pupok")
        self.assertFalse(self.protouser != u)

    def test___ne_2(self):
        u = protouser.protouser("pupok2")
        self.assertTrue(self.protouser != u)

    def test_diff_1(self):
        protouser1 = protouser.protouser("pupok1")
        self.assertDictEqual(
            self.protouser.diff(protouser1), {"login": "pupok1"}
        )

    ##    def test_diff_2(self):
    ##        protouser1=protouser.protouser(u'pupok',u'455642')
    ##        self.assertDictEqual(self.protouser.diff(protouser1),{u'uid':u'455642'})

    def test_diff_ldap_attrs_1(self):
        protouser1 = protouser.protouser("pupo3k")
        self.assertDictEqual(
            self.protouser.diff_ldap_attrs(protouser1),
            {"sAMAccountName": "pupo3k"},
        )

    def test_diff_ldap_attrs_2(self):
        protouser1 = protouser.protouser("pupok8")
        self.assertDictEqual(
            self.protouser.diff_ldap_attrs(protouser1),
            {"sAMAccountName": "pupok8"},
        )


class TestUserMetods3(unittest.TestCase):
    def setUp(self):
        self.protouser = protouser.protouser("pupok.kuvirok")

    def tearDown(self):
        self.protouser = None

    def test___init_21(self):
        self.assertEqual(self.protouser.__class__.__name__, "protouser")

    def test___get_ldap_attrs_1(self):
        at = {"sAMAccountName": "pupok.kuvirok"}
        self.assertEqual(self.protouser.get_ldap_attrs(), at)

    def test___get_ldap_attrs_1(self):
        at = {"sAMAccountName": "pupok.kuvirok", "test": ""}
        self.assertNotEqual(self.protouser.get_ldap_attrs(), at)

    def test___diff_ldap_attrs_by_categories_1(self):
        protouser1 = protouser.protouser("pupok8")
        self.assertRaises(
            WrongParam,
            protouser.protouser.diff_ldap_attrs_by_categories,
            self.protouser,
            protouser1,
        )


if __name__ == "__main__":
    unittest.main()
