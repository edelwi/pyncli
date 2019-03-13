# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        utill_test
# Purpose:      tests
#
# Author:      Evgeniy Semenov
#
# Created:     27.02.2018
# Copyright:   (c) Evgeniy Semenov 2018-2019
# Licence:     MIT
#-------------------------------------------------------------------------------

import unittest
import os
import datetime

pd=os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
os.sys.path.insert(0,pd)
import pyncli.ldap.utill as utill
from pyncli.ldap.admexept import NotEnoughParams, EmptyParam, WrongParam, TooLong

class Test_date_str_to_generalize_time(unittest.TestCase):

##    def test_1(self):
##        self.assertRaises(EmptyParam, utill.date_str_to_generalize_time, u'')


    def test_2(self):
        self.assertRaises(WrongParam,utill.date_str_to_generalize_time,0)

    def test_3(self):
        self.assertRaises(WrongParam,utill.date_str_to_generalize_time,u'pupkin')

    def test_4(self):
        self.assertRaises(WrongParam,utill.date_str_to_generalize_time,u'2017-10-01T')

    def test_5(self):
        self.assertEqual(utill.date_str_to_generalize_time(u'2017-10-01'),u'20171001000000.0Z')

    def test_6(self):
        self.assertEqual(utill.date_str_to_generalize_time(u'1955-12-21'),'19551221000000.0Z')

    def test_7(self):
        self.assertRaises(WrongParam, utill.date_str_to_generalize_time,u'2018-02-29')

    def test_8(self):
        self.assertEqual(utill.date_str_to_generalize_time(u'1955/02/21'),'19550221000000.0Z')

    def test_9(self):
        self.assertEqual(utill.date_str_to_generalize_time(u'21.02.1955'),'19550221000000.0Z')

    def test_10(self):
        self.assertEqual(utill.date_str_to_generalize_time('29.02.1952'),'19520229000000.0Z')

    def test_11(self):
        self.assertEqual(utill.date_str_to_generalize_time(u'29.03.2011'),'20110329000000.0Z')

    def test_12(self):
        self.assertEqual(utill.date_str_to_generalize_time(u'9.2.2011'),'20110209000000.0Z')

    def test_13(self):
        self.assertRaises(WrongParam,utill.date_str_to_generalize_time,u'2912.1992')

    def test_14(self):
        self.assertRaises(WrongParam,utill.date_str_to_generalize_time,u'29121992')

    def test_15(self):
        self.assertRaises(WrongParam,utill.date_str_to_generalize_time,u'29,12,1992')

class Test_is_generalized_time(unittest.TestCase):
    def test_1(self):
        self.assertTrue(utill.is_generalized_time(u''))


    def test_2(self):
        self.assertTrue(utill.is_generalized_time(''))

    def test_3(self):
        self.assertFalse(utill.is_generalized_time('jhkjhkj'))

    def test_4(self):
        self.assertFalse(utill.is_generalized_time('5465465465'))

    def test_5(self):
        self.assertTrue(utill.is_generalized_time('20171001000000.0Z'))

    def test_6(self):
        self.assertTrue(utill.is_generalized_time('19551221000000.0Z'))

    def test_7(self):
        self.assertFalse(utill.is_generalized_time(u'20180229000000.0Z'))

    def test_8(self):
        self.assertTrue(utill.is_generalized_time('19550221122031.0Z'))

class Test_generalized_time_to_datetime(unittest.TestCase):
    def test_1(self):
        self.assertRaises(EmptyParam, utill.generalized_time_to_datetime, u'')

    def test_2(self):
        self.assertRaises(EmptyParam, utill.generalized_time_to_datetime, '')

    def test_3(self):
        self.assertRaises(WrongParam, utill.generalized_time_to_datetime, u'20183333')

    def test_4(self):
        self.assertRaises(WrongParam, utill.generalized_time_to_datetime, '20180229000000.0Z')

    def test_5(self):
        self.assertEqual(utill.generalized_time_to_datetime('20180129000000.0Z'),datetime.datetime(2018,1,29,0,0,0) )

    def test_6(self):
        self.assertEqual(utill.generalized_time_to_datetime('20180129120033.0Z'),datetime.datetime(2018,1,29,12,0,33) )

class Test_datetime_to_generalized_time(unittest.TestCase):
    def test_1(self):
        self.assertRaises(WrongParam, utill.datetime_to_generalized_time, u'')

    def test_2(self):
        n=datetime.datetime.now()
        self.assertEqual(utill.datetime_to_generalized_time(n),n.strftime(u"%Y%m%d%H%M%S.0Z"))

    def test_3(self):
        self.assertRaises(WrongParam, utill.datetime_to_generalized_time, datetime.datetime.time(datetime.datetime.now()) )

if __name__ == '__main__':
    unittest.main()
