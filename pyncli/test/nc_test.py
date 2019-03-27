# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        nc_test
# Purpose:      tests
#
# Author:      Evgeniy Semenov
#
# Created:     05.02.2019
# Copyright:   (c) Evgeniy Semenov 2019
# Licence:     MIT
# -------------------------------------------------------------------------------

import unittest
import os

pd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, pd)
import nc
from ocs.ocs import (
    PERMISSION_CREATE,
    PERMISSION_READ,
    PERMISSION_UPDATE,
    PERMISSION_DELETE,
    PERMISSION_SHARE,
    PERMISSION_ALL,
)


class TestFuncs(unittest.TestCase):
    def test___str_to_permissions_0(self):
        self.assertEqual(
            nc.str_to_permissions(""),
            nc.str_to_permissions(nc.PERMISSION_DEFAULT_STR),
        )

    def test___str_to_permissions_1(self):
        self.assertEqual(nc.str_to_permissions("r"), PERMISSION_READ)

    def test___str_to_permissions_2(self):
        self.assertEqual(nc.str_to_permissions("c"), PERMISSION_CREATE)

    def test___str_to_permissions_3(self):
        self.assertEqual(nc.str_to_permissions("u"), PERMISSION_UPDATE)

    def test___str_to_permissions_4(self):
        self.assertEqual(nc.str_to_permissions("d"), PERMISSION_DELETE)

    def test___str_to_permissions_5(self):
        self.assertEqual(nc.str_to_permissions("s"), PERMISSION_SHARE)

    def test___str_to_permissions_6(self):
        self.assertEqual(nc.str_to_permissions("a"), PERMISSION_ALL)

    def test___str_to_permissions_7(self):
        self.assertEqual(
            nc.str_to_permissions("rc"), PERMISSION_READ + PERMISSION_CREATE
        )

    def test___str_to_permissions_8(self):
        self.assertEqual(
            nc.str_to_permissions("rcu"),
            PERMISSION_READ + PERMISSION_CREATE + PERMISSION_UPDATE,
        )

    def test___str_to_permissions_9(self):
        self.assertEqual(
            nc.str_to_permissions("rcud"),
            PERMISSION_READ
            + PERMISSION_CREATE
            + PERMISSION_UPDATE
            + PERMISSION_DELETE,
        )

    def test___str_to_permissions_10(self):
        self.assertEqual(nc.str_to_permissions("rcuds"), PERMISSION_ALL)

    def test___str_to_permissions_11(self):
        self.assertEqual(nc.str_to_permissions("rcuda"), PERMISSION_ALL)

    def test___str_to_permissions_12(self):
        self.assertEqual(
            nc.str_to_permissions("ru"), PERMISSION_READ + PERMISSION_UPDATE
        )

    def test___str_to_permissions_13(self):
        self.assertEqual(
            nc.str_to_permissions("rs"), PERMISSION_READ + PERMISSION_SHARE
        )

    def test___str_to_permissions_14(self):
        self.assertEqual(
            nc.str_to_permissions(5),
            nc.str_to_permissions(nc.PERMISSION_DEFAULT_STR),
        )

    def test__is_ascii_1(self):
        self.assertTrue(nc.is_ascii("a"))

    def test__is_ascii_2(self):
        self.assertTrue(nc.is_ascii("ljhflmksfl76875676545#!a"))

    def test__is_ascii_3(self):
        self.assertFalse(nc.is_ascii("qweцh"))

    def test__is_ascii_4(self):
        self.assertEqual(nc.is_ascii(5), None)

    def test__is_ascii_5(self):
        self.assertTrue(nc.is_ascii(""))

    def test__is_login_1(self):
        self.assertTrue(nc.is_login("petrov"))

    def test__is_login_2(self):
        self.assertFalse(nc.is_login("petrov "))

    def test__is_login_3(self):
        self.assertFalse(nc.is_login("petrov ivan"))

    def test__is_login_4(self):
        self.assertFalse(nc.is_login(" "))

    def test__is_login_5(self):
        self.assertFalse(nc.is_login(""))

    def test__is_login_6(self):
        self.assertTrue(nc.is_login("pupkin@example.com"))

    def test__is_login_7(self):
        self.assertFalse(nc.is_login("pupkin@examplecom"))

    def test__is_login_8(self):
        self.assertFalse(nc.is_login("pupkin@"))

    def test__is_login_9(self):
        self.assertFalse(nc.is_login("pupkin@e"))

    def test__is_login_10(self):
        self.assertFalse(nc.is_login("pupkin@@example.com"))

    def test__is_login_12(self):
        self.assertFalse(nc.is_login("pupkin@ex@a.com"))

    def test__is_login_13(self):
        self.assertFalse(nc.is_login("pupkin@e.c@"))

    def test__is_login_14(self):
        self.assertTrue(nc.is_login("pupkin@e.c"))

    def test__is_login_15(self):
        self.assertTrue(nc.is_login("hu"))

    def test__is_login_16(self):
        self.assertTrue(nc.is_login("pupkin.v.v@example.com"))

    def test__is_login_17(self):
        self.assertTrue(nc.is_login("pupkin.vova@example.ru"))

    ##    def test__is_login_18(self): # кажется у нас такой был
    ##        self.assertFalse(nc.is_login('pupkin..v@example.com'))

    def test__is_login_19(self):
        self.assertFalse(nc.is_login("pupkin$e.c"))

    def test__get_quote_bytes_1(self):
        self.assertEqual(nc.get_quote_bytes(""), nc.DEFAULT_QUOTA)

    def test__get_quote_bytes_2(self):
        self.assertEqual(nc.get_quote_bytes("234"), 234)

    def test__get_quote_bytes_3(self):
        self.assertEqual(nc.get_quote_bytes("8053063685"), 8053063685)

    def test__get_quote_bytes_4(self):
        self.assertEqual(nc.get_quote_bytes("700k"), 716800)

    def test__get_quote_bytes_5(self):
        self.assertEqual(nc.get_quote_bytes("700m"), 716800 * 1024)

    def test__get_quote_bytes_6(self):
        m = 1073741824
        self.assertAlmostEqual(nc.get_quote_bytes("7.5g"), round(7.5 * m))

    def test__get_quote_bytes_7(self):
        m = 1099511627776
        self.assertAlmostEqual(nc.get_quote_bytes("0.5t"), round(0.5 * m))

    def test__get_quote_bytes_8(self):
        m = 1099511627776
        self.assertAlmostEqual(nc.get_quote_bytes("853t"), round(853 * m))


if __name__ == "__main__":
    unittest.main()
