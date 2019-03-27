# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Name:        user_test
# Purpose:      tests
#
# Author:      Evgeniy Semenov
#
# Created:     10.02.2017
# Copyright:   (c) Evgeniy Semenov 2017-2019
# Licence:     MIT
# -------------------------------------------------------------------------------
import unittest
import os

pd = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.sys.path.insert(0, pd)
from pyncli.ldap import user
from pyncli.ldap import protouser
from pyncli.ldap.uac import *
from pyncli.ldap.admexept import (
    NotEnoughParams,
    EmptyParam,
    WrongParam,
    TooLong,
)


class TestUserMetods(unittest.TestCase):
    def test___init_1(self):
        self.assertRaises(EmptyParam, user.user, "", "")

    ##    def test___init_2(self):
    ##        self.assertRaises(EmptyParam,user.user,u'pupkin',u'')

    def test___init_3(self):
        self.assertRaises(WrongParam, user.user, ["t25"], "5")

    def test___init_4(self):
        self.assertRaises(WrongParam, user.user, "pupkin", 55)

    def test___init_5(self):
        self.assertRaises(
            EmptyParam, user.user, "pupkin", "564646", org_unit=""
        )

    def test___init_6(self):
        self.assertRaises(
            WrongParam,
            user.user,
            "pupkin",
            "564646",
            org_unit="OU=test,DC=example,DC=com",
            surname=5,
            first_name="",
            middle_name="",
            company="",
            department="",
            division="",
            position="",
            mail="",
            mobile="",
            other_mailbox="0",
            other_mobile="0",
            comment="",
            employee_type="",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
        )

    def test___init_7(self):
        self.assertRaises(
            WrongParam,
            user.user,
            "pupkin",
            "564646",
            org_unit="OU=test,DC=example,DC=com",
            surname="",
            first_name=8,
            middle_name="",
            company="",
            department="",
            division="",
            position="",
            mail="",
            mobile="",
            other_mailbox="0",
            other_mobile="0",
            comment="",
            employee_type="",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
        )

    def test___init_8(self):
        self.assertRaises(
            WrongParam,
            user.user,
            "pupkin",
            "564646",
            org_unit="OU=test,DC=example,DC=com",
            surname="",
            first_name="",
            middle_name=[],
            company="",
            department="",
            division="",
            position="",
            mail="",
            mobile="",
            other_mailbox="0",
            other_mobile="0",
            comment="",
            employee_type="",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
        )

    def test___init_9(self):
        self.assertRaises(
            WrongParam,
            user.user,
            "pupkin",
            "564646",
            org_unit="OU=test,DC=example,DC=com",
            surname="",
            first_name="",
            middle_name="",
            company={},
            department="",
            division="",
            position="",
            mail="",
            mobile="",
            other_mailbox="0",
            other_mobile="0",
            comment="",
            employee_type="",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
        )

    def test___init_10(self):
        self.assertRaises(
            WrongParam,
            user.user,
            "pupkin",
            "564646",
            org_unit="OU=test,DC=example,DC=com",
            surname="",
            first_name="",
            middle_name="",
            company="",
            department=0x02,
            division="",
            position="",
            mail="",
            mobile="",
            other_mailbox="0",
            other_mobile="0",
            comment="",
            employee_type="",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
        )

    def test___init_11(self):
        self.assertRaises(
            WrongParam,
            user.user,
            "pupkin",
            "564646",
            org_unit="OU=test,DC=example,DC=com",
            surname="",
            first_name="",
            middle_name="",
            company="",
            department="",
            division=0,
            position="",
            mail="",
            mobile="",
            other_mailbox="0",
            other_mobile="0",
            comment="",
            employee_type="",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
        )

    def test___init_12(self):
        self.assertRaises(
            WrongParam,
            user.user,
            "pupkin",
            "564646",
            org_unit="OU=test,DC=example,DC=com",
            surname="",
            first_name="",
            middle_name="",
            company="",
            department="",
            division="",
            position=8,
            mail="",
            mobile="",
            other_mailbox="0",
            other_mobile="0",
            comment="",
            employee_type="",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
        )

    def test___init_13(self):
        self.assertRaises(
            WrongParam,
            user.user,
            "pupkin",
            "564646",
            org_unit="OU=test,DC=example,DC=com",
            surname="",
            first_name="",
            middle_name="",
            company="",
            department="",
            division="",
            position="",
            mail=uac.NORMAL_ACCOUNT,
            mobile="",
            other_mailbox="0",
            other_mobile="0",
            comment="",
            employee_type="",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
        )

    def test___init_14(self):
        self.assertRaises(
            WrongParam,
            user.user,
            "pupkin",
            "564646",
            org_unit="OU=test,DC=example,DC=com",
            surname="",
            first_name="",
            middle_name="",
            company="",
            department="",
            division="",
            position="",
            mail="",
            mobile=5,
            other_mailbox="0",
            other_mobile="0",
            comment="",
            employee_type="",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
        )

    def test___init_15(self):
        self.assertRaises(
            WrongParam,
            user.user,
            "pupkin",
            "564646",
            org_unit="OU=test,DC=example,DC=com",
            surname="",
            first_name="",
            middle_name="",
            company="",
            department="",
            division="",
            position="",
            mail="",
            mobile="",
            other_mailbox=[],
            other_mobile="0",
            comment="",
            employee_type="",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
        )

    def test___init_16(self):
        self.assertRaises(
            WrongParam,
            user.user,
            "pupkin",
            "564646",
            org_unit="OU=test,DC=example,DC=com",
            surname="",
            first_name="",
            middle_name="",
            company="",
            department="",
            division="",
            position="",
            mail="",
            mobile="",
            other_mailbox="",
            other_mobile={},
            comment="",
            employee_type="",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
        )

    def test___init_17(self):
        self.assertRaises(
            WrongParam,
            user.user,
            "pupkin",
            "564646",
            org_unit="OU=test,DC=example,DC=com",
            surname="",
            first_name="",
            middle_name="",
            company="",
            department="",
            division="",
            position="",
            mail="",
            mobile="",
            other_mailbox="",
            other_mobile="0",
            comment=56465,
            employee_type="",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
        )

    def test___init_18(self):
        self.assertRaises(
            WrongParam,
            user.user,
            "pupkin",
            "564646",
            org_unit="OU=test,DC=example,DC=com",
            surname="",
            first_name="",
            middle_name="",
            company="",
            department="",
            division="",
            position="",
            mail="",
            mobile="",
            other_mailbox="",
            other_mobile="0",
            comment="",
            employee_type=6,
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
        )

    def test___init_19(self):
        self.assertRaises(
            WrongParam,
            user.user,
            "pupkin",
            "564646",
            org_unit="OU=test,DC=example,DC=com",
            surname="",
            first_name="",
            middle_name="",
            company="",
            department="",
            division="",
            position="",
            mail="",
            mobile="",
            other_mailbox="",
            other_mobile="0",
            comment=56465,
            employee_type="",
            acc_control=uac.NORMAL_ACCOUNT,
        )

    def test___init_20(self):
        self.assertRaises(
            WrongParam,
            user.user,
            "pupkin",
            "564646",
            org_unit="OU=test,DC=example,DC=com",
            surname="",
            first_name="",
            middle_name="",
            company="",
            department="",
            division="",
            position="",
            mail="",
            mobile="",
            other_mailbox="",
            other_mobile="0",
            comment="",
            employee_type="",
            acc_control=uac.NORMAL_ACCOUNT,
            description=65476,
        )

    def test___init_21(self):
        self.assertRaises(
            TooLong,
            user.user,
            "ю" * 65,
            "564646",
            org_unit="OU=test,DC=example,DC=com",
            surname="",
            first_name="",
            middle_name="",
            company="",
            department="",
            division="",
            position="",
            mail="",
            mobile="",
            other_mailbox="",
            other_mobile="0",
            comment="",
            employee_type="",
            acc_control=uac.NORMAL_ACCOUNT,
            description="",
        )

    def test___init_22(self):
        self.assertRaises(
            TooLong,
            user.user,
            "pupkin",
            "5" * 257,
            org_unit="OU=test,DC=example,DC=com",
            surname="",
            first_name="",
            middle_name="",
            company="",
            department="",
            division="",
            position="",
            mail="",
            mobile="",
            other_mailbox="",
            other_mobile="0",
            comment="",
            employee_type="",
            acc_control=uac.NORMAL_ACCOUNT,
            description="",
        )

    def test___init_23(self):
        self.assertRaises(
            TooLong,
            user.user,
            "pupkin",
            "564646",
            org_unit="OU=test,DC=example,DC=com" * 50,
            surname="",
            first_name="",
            middle_name="",
            company="",
            department="",
            division="",
            position="",
            mail="",
            mobile="",
            other_mailbox="",
            other_mobile="0",
            comment="",
            employee_type="",
            acc_control=uac.NORMAL_ACCOUNT,
            description="",
        )

    def test___init_24(self):
        self.user = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="п" * 68,
            first_name="Пирун",
            middle_name="Гансович",
            company="ННГУ",
            department="АХУ",
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertEqual(self.user.surname, "п" * 64)

    def test___init_25(self):
        self.user = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="п",
            first_name="и" * 80,
            middle_name="Гансович",
            company="ННГУ",
            department="АХУ",
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertEqual(self.user.first_name, "и" * 64)

    def test___init_26(self):
        self.user = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="п",
            first_name="и",
            middle_name="ч" * 80,
            company="ННГУ",
            department="АХУ",
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertEqual(self.user.middle_name, "ч" * 64)

    def test___init_27(self):
        self.user = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="п",
            first_name="и",
            middle_name="ч",
            company="У" * 80,
            department="АХУ",
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertEqual(self.user.company, "У" * 64)

    def test___init_28(self):
        self.user = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="п",
            first_name="и",
            middle_name="ч",
            company="У",
            department="Х" * 80,
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertEqual(self.user.department, "Х" * 64)

    def test___init_29(self):
        self.user = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="п",
            first_name="и",
            middle_name="ч",
            company="У",
            department="Х",
            division="д" * 260,
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertEqual(self.user.division, "д" * 256)

    def test___init_30(self):
        self.user = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="п",
            first_name="и",
            middle_name="ч",
            company="У",
            department="Х",
            division="д",
            position="р" * 200,
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertEqual(self.user.position, "р" * 128)

    def test___init_31(self):
        self.user = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="п",
            first_name="и",
            middle_name="ч",
            company="У",
            department="Х",
            division="д",
            position="р",
            mail="m" * 280,
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertEqual(self.user.mail, "m" * 256)

    def test___init_32(self):
        self.user = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="п",
            first_name="и",
            middle_name="ч",
            company="У",
            department="Х",
            division="д",
            position="р",
            mail="m",
            mobile="7" * 66,
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertEqual(self.user.mobile, "7" * 64)

    def test___init_33(self):
        self.user = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="п",
            first_name="и",
            middle_name="ч",
            company="У",
            department="Х",
            division="д",
            position="р",
            mail="m",
            mobile="7",
            other_mailbox="0" * 66,
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertEqual(self.user.other_mailbox, "0" * 64)

    def test___init_34(self):
        self.user = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="п",
            first_name="и",
            middle_name="ч",
            company="У",
            department="Х",
            division="д",
            position="р",
            mail="m",
            mobile="7",
            other_mailbox="0",
            other_mobile="1" * 66,
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertEqual(self.user.other_mobile, "1" * 64)

    def test___init_35(self):
        self.user = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="п",
            first_name="и",
            middle_name="ч",
            company="У",
            department="Х",
            division="д",
            position="р",
            mail="m",
            mobile="7",
            other_mailbox="0",
            other_mobile="1",
            comment="к" * 1200,
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertEqual(self.user.comment, "к" * 1024)

    def test___init_36(self):
        self.user = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="п",
            first_name="и",
            middle_name="ч",
            company="У",
            department="Х",
            division="д",
            position="р",
            mail="m",
            mobile="7",
            other_mailbox="0",
            other_mobile="1",
            comment="к",
            employee_type="ю" * 280,
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertEqual(self.user.employee_type, "ю" * 256)

    def test___init_37(self):
        self.user = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="п",
            first_name="и",
            middle_name="ч",
            company="У",
            department="Х",
            division="д",
            position="р",
            mail="m",
            mobile="7",
            other_mailbox="0",
            other_mobile="1",
            comment="к",
            employee_type="ю",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="ы" * 1200,
        )
        self.assertEqual(self.user.description, "ы" * 1024)

    def test___init_38(self):
        self.user = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="п",
            first_name="и",
            middle_name="ч",
            company="У",
            department="Х",
            division="д",
            position="р",
            mail="m",
            mobile="7",
            other_mailbox="0",
            other_mobile="1",
            comment="к",
            employee_type="ю",
            acc_control=514,
            description="ы",
        )

        l = uac.get_control([uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE])
        u = uac.get_control(self.user.acc_control)
        self.assertEqual(u, l)

    def test___get_domain_1(self):
        self.assertRaises(
            WrongParam,
            user.user,
            "pupkins",
            "76348",
            org_unit="OU=test3,OU=example,OU=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="UNN",
            department="АХУ",
            division="отдел 5",
            position="beta-тестер",
            mail="test@example.com",
            mobile="+77071234567",
            other_mailbox="1",
            other_mobile="0",
            comment="коммент.net",
            employee_type="юзер-садист",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="очень классный работник",
        )

    def test___get_domain_2(self):
        self.assertRaises(
            WrongParam,
            user.user,
            "pupkins",
            "76348",
            org_unit="OU=test3,du=unn,oo=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="UNN",
            department="АХУ",
            division="отдел 5",
            position="beta-тестер",
            mail="test@example.com",
            mobile="+77071234567",
            other_mailbox="1",
            other_mobile="0",
            comment="коммент.net",
            employee_type="юзер-садист",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="очень классный работник",
        )

    def test___get_domain_3(self):
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test3,dc=example,DC=com,Dc=ua",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="UNN",
            department="АХУ",
            division="отдел 5",
            position="beta-тестер",
            mail="test@example.com",
            mobile="+77071234567",
            other_mailbox="1",
            other_mobile="0",
            comment="коммент.net",
            employee_type="юзер-садист",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="очень классный работник",
        )
        self.assertEqual(user1.get_domain(), "example.com.ua")

    def test___get_domain_4(self):
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test3, dc = example, DC = com, Dc =ua",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="UNN",
            department="АХУ",
            division="отдел 5",
            position="beta-тестер",
            mail="test@example.com",
            mobile="+77071234567",
            other_mailbox="1",
            other_mobile="0",
            comment="коммент.net",
            employee_type="юзер-садист",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="очень классный работник",
        )
        self.assertEqual(user1.get_domain(), "example.com.ua")


class TestUserMetods2(unittest.TestCase):
    def setUp(self):
        self.user = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="ННГУ",
            department="АХУ",
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )

    def tearDown(self):
        self.user = None

    def test___init_8(self):
        self.assertEqual(self.user.__class__.__name__, "user")

    def test___init_9(self):
        self.assertEqual(self.user.surname, "Пупкин")

    def test___init_10(self):
        self.assertEqual(self.user.first_name, "Пирун")

    def test___init_11(self):
        self.assertEqual(self.user.login, "pupkins")

    def test___init_12(self):
        self.assertEqual(self.user.uid, "76348")

    def test___init_13(self):
        self.assertEqual(self.user.middle_name, "Гансович")

    def test___init_14(self):
        self.assertEqual(self.user.company, "ННГУ")

    def test___init_15(self):
        self.assertEqual(self.user.department, "АХУ")

    def test___init_16(self):
        self.assertEqual(self.user.division, "отдел")

    def test___init_17(self):
        self.assertEqual(self.user.position, "тестер")

    def test___init_18(self):
        self.assertEqual(self.user.mail, "test@example.com")

    def test___init_19(self):
        self.assertEqual(self.user.employee_type, "юзер")

    def test___init_20(self):
        self.assertEqual(self.user.comment, "коммент")

    def test___init_21(self):
        self.assertEqual(self.user.mobile, "+77771234567")

    def test___init_22(self):
        self.assertEqual(self.user.other_mailbox, "0")

    def test___init_23(self):
        self.assertEqual(self.user.other_mobile, "1")

    def test___init_24(self):
        self.assertEqual(
            self.user.acc_control, [uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE]
        )

    def test___init_25(self):
        self.assertEqual(self.user.initials, "Г")

    def test___init_26(self):
        self.assertEqual(self.user.full_name, "Пупкин Пирун Гансович")

    def test___init_27(self):
        self.assertEqual(self.user.dn, "CN=pupkins,OU=test,DC=example,DC=com")

    def test___init_28(self):
        self.assertEqual(self.user.get_initials(), "Г")

    def test___init_29(self):
        self.assertEqual(self.user.get_fullname(), "Пупкин Пирун Гансович")

    def test___init_30(self):
        self.assertEqual(
            self.user.get_dn(), "CN=pupkins,OU=test,DC=example,DC=com"
        )

    def test___init_31(self):
        self.assertEqual(self.user.enabled, False)

    def test___init_32(self):
        self.user.enabled = True
        self.assertEqual(self.user.enabled, True)

    def test___init_33(self):
        self.user.enabled = True
        self.assertListEqual(self.user.acc_control, [uac.NORMAL_ACCOUNT])

    def test___init_34(self):
        d = {
            "comment": "коммент",
            "division": "отдел",
            "displayName": "Пупкин Пирун Гансович",
            "uid": "76348",
            "otherMailbox": "0",
            "title": "тестер",
            "mobile": "+77771234567",
            "company": "ННГУ",
            "userAccountControl": "0x202",
            "initials": "Г",
            "employeeType": "юзер",
            "middleName": "Гансович",
            "otherMobile": "1",
            "sn": "Пупкин",
            "department": "АХУ",
            "mail": "test@example.com",
            "givenName": "Пирун",
            "sAMAccountName": "pupkins",
            "description": "классный работник",
            "userPrincipalName": "pupkins@example.com",
        }

        self.assertDictEqual(self.user.get_ldap_attrs(), d)

    def test_fullname_1(self):
        self.assertEqual(self.user.get_fullname(), "Пупкин Пирун Гансович")

    def test_initials_1(self):
        self.assertEqual(self.user.get_initials(), "Г")

    def test___eq_1(self):
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="ННГУ",
            department="АХУ",
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertEqual(self.user, user1)

    def test___eq_2(self):
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="ННГУ",
            department="АХУ",
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertTrue(self.user == user1)

    def test___eq_3(self):
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="ПУпкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="ННГУ",
            department="АХУ",
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertFalse(self.user == user1)

    def test___eq_4(self):
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="Пупкин",
            first_name="ирун",
            middle_name="Гансович",
            company="ННГУ",
            department="АХУ",
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertFalse(self.user == user1)

    def test___eq_5(self):
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="ННГУ",
            department="АХУ",
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT],
            description="классный работник",
        )
        self.assertFalse(self.user == user1)

    def test___ne_1(self):
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="ННГУ",
            department="АХУ",
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertFalse(self.user != user1)

    def test___ne_2(self):
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="ННГУ",
            department="АХУ",
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="1",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertTrue(self.user != user1)

    def test_diff_1(self):
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="Пупкина",
            first_name="Пирун",
            middle_name="Гансович",
            company="ННГУ",
            department="АХУ",
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertDictEqual(
            self.user.diff(user1),
            {"surname": "Пупкина", "full_name": "Пупкина Пирун Гансович"},
        )

    def test_diff_2(self):
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="Пупкин",
            first_name="Казимир",
            middle_name="Гансович",
            company="ННГУ",
            department="АХУ",
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertDictEqual(
            self.user.diff(user1),
            {"first_name": "Казимир", "full_name": "Пупкин Казимир Гансович"},
        )

    def test_diff_3(self):
        user1 = user.user(
            "pups",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="ННГУ",
            department="АХУ",
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertDictEqual(
            self.user.diff(user1),
            {
                "login": "pups",
                "dn": "CN=pups,OU=test,DC=example,DC=com",
                "principal_name": "pups@example.com",
            },
        )

    def test_diff_4(self):
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="",
            company="ННГУ",
            department="АХУ",
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertDictEqual(
            self.user.diff(user1),
            {"middle_name": "", "initials": "", "full_name": "Пупкин Пирун"},
        )

    def test_diff_5(self):
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="Фирма",
            department="АХУ",
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertDictEqual(self.user.diff(user1), {"company": "Фирма"})

    def test_diff_6(self):
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="ННГУ",
            department="Департамент",
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertDictEqual(
            self.user.diff(user1), {"department": "Департамент"}
        )

    def test_diff_7(self):
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="ННГУ",
            department="АХУ",
            division="Бригада С",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertDictEqual(self.user.diff(user1), {"division": "Бригада С"})

    def test_diff_8(self):
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="ННГУ",
            department="АХУ",
            division="отдел",
            position="кодер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertDictEqual(self.user.diff(user1), {"position": "кодер"})

    def test_diff_9(self):
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="ННГУ",
            department="АХУ",
            division="отдел",
            position="тестер",
            mail="test_1@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertDictEqual(
            self.user.diff(user1), {"mail": "test_1@example.com"}
        )

    def test_diff_10(self):
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="ННГУ",
            department="АХУ",
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="soratnik",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertDictEqual(
            self.user.diff(user1), {"employee_type": "soratnik"}
        )

    def test_diff_11(self):
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="ННГУ",
            department="АХУ",
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="ударник",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertDictEqual(self.user.diff(user1), {"comment": "ударник"})

    def test_diff_12(self):
        self.maxDiff = None
        user1 = user.user(
            "rabbe",
            "666",
            org_unit="OU=best,DC=example,DC=com",
            surname="Рабинович",
            first_name="Изя",
            middle_name="Мойшевич",
            company="Рога и Копыта",
            department="служба быта",
            division="отдел сбыта",
            position="сурдопереводчик",
            mail="test@best.com",
            mobile="+77776666666",
            other_mailbox="1",
            other_mobile="0",
            comment="характер - нордический",
            employee_type="профи",
            acc_control=[uac.PASSWD_NOTREQD, uac.SMARTCARD_REQUIRED],
            description="классный работник 2",
        )
        df = {
            "surname": "Рабинович",
            "login": "rabbe",
            "uid": "666",
            "first_name": "Изя",
            "middle_name": "Мойшевич",
            "initials": "М",
            "company": "Рога и Копыта",
            "division": "отдел сбыта",
            "department": "служба быта",
            "position": "сурдопереводчик",
            "full_name": "Рабинович Изя Мойшевич",
            "employee_type": "профи",
            "mail": "test@best.com",
            "comment": "характер - нордический",
            "dn": "CN=rabbe,OU=best,DC=example,DC=com",
            "mobile": "+77776666666",
            "other_mailbox": "1",
            "other_mobile": "0",
            "acc_control": [uac.PASSWD_NOTREQD, uac.SMARTCARD_REQUIRED],
            "org_unit": "OU=best,DC=example,DC=com",
            "description": "классный работник 2",
            "principal_name": "rabbe@example.com",
        }

        self.assertDictEqual(self.user.diff(user1), df)

    def test_diff_13(self):
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="ННГУ",
            department="АХУ",
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234560",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertDictEqual(self.user.diff(user1), {"mobile": "+77771234560"})

    def test_diff_14(self):
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="ННГУ",
            department="АХУ",
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="1",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertDictEqual(self.user.diff(user1), {"other_mailbox": "1"})

    def test_diff_15(self):
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="ННГУ",
            department="АХУ",
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="0",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertDictEqual(self.user.diff(user1), {"other_mobile": "0"})

    def test_diff_16(self):
        user1 = user.user(
            "pupkins",
            "0",
            org_unit="OU=test,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="ННГУ",
            department="АХУ",
            division="отдел",
            position="тестер",
            mail="test@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )
        self.assertDictEqual(self.user.diff(user1), {"uid": "0"})

    def test_get_ldap_attrs_1(self):
        a = {
            "comment": "коммент",
            "company": "ННГУ",
            "department": "АХУ",
            "displayName": "Пупкин Пирун Гансович",
            "division": "отдел",
            "employeeType": "юзер",
            "givenName": "Пирун",
            "initials": "Г",
            "mail": "test@example.com",
            "middleName": "Гансович",
            "mobile": "+77771234567",
            "otherMailbox": "0",
            "otherMobile": "1",
            "sAMAccountName": "pupkins",
            "sn": "Пупкин",
            "title": "тестер",
            "uid": "76348",
            "userAccountControl": "0x202",
            "description": "классный работник",
            "userPrincipalName": "pupkins@example.com",
        }

        self.assertDictEqual(self.user.get_ldap_attrs(), a)

    def test_diff_ldap_attrs_1(self):
        user1 = user.user(
            "popkina",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="Попкина",
            first_name="Матильда",
            middle_name="Гансовна",
            company="ННГУ",
            department="не АХУ",
            division="отдел",
            position="тестер",
            mail="popna@example.com",
            mobile="+77771234567",
            other_mailbox="0",
            other_mobile="1",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT],
            description="классный работник",
        )
        df = {
            "department": "не АХУ",
            "displayName": "Попкина Матильда Гансовна",
            "givenName": "Матильда",
            "mail": "popna@example.com",
            "middleName": "Гансовна",
            "sAMAccountName": "popkina",
            "sn": "Попкина",
            "userAccountControl": "0x200",
            "userPrincipalName": "popkina@example.com",
        }
        self.assertDictEqual(self.user.diff_ldap_attrs(user1), df)

    def test_diff_ldap_attrs_2(self):
        self.maxDiff = None
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test3,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="UNN",
            department="АХУ",
            division="отдел 5",
            position="beta-тестер",
            mail="test@example.com",
            mobile="+77071234567",
            other_mailbox="1",
            other_mobile="0",
            comment="коммент.net",
            employee_type="юзер-садист",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="очень классный работник",
        )
        df = {
            "comment": "коммент.net",
            "company": "UNN",
            "division": "отдел 5",
            "employeeType": "юзер-садист",
            "mobile": "+77071234567",
            "otherMailbox": "1",
            "otherMobile": "0",
            "description": "очень классный работник",
            "title": "beta-тестер",
        }
        self.assertDictEqual(self.user.diff_ldap_attrs(user1), df)

    def test_diff_ldap_attrs_by_categories_1(self):
        self.maxDiff = None
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test3,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="UNN",
            department="АХУ",
            division="отдел 5",
            position="beta-тестер",
            mail="test@example.com",
            mobile="+77071234567",
            other_mailbox="1",
            other_mobile="0",
            comment="коммент.net",
            employee_type="юзер-садист",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="очень классный работник",
        )
        df = {
            "comment": [("MODIFY_REPLACE", ["коммент.net"])],
            "company": [("MODIFY_REPLACE", ["UNN"])],
            "division": [("MODIFY_REPLACE", ["отдел 5"])],
            "employeeType": [("MODIFY_REPLACE", ["юзер-садист"])],
            "mobile": [("MODIFY_REPLACE", ["+77071234567"])],
            "otherMailbox": [("MODIFY_REPLACE", ["1"])],
            "otherMobile": [("MODIFY_REPLACE", ["0"])],
            "description": [("MODIFY_REPLACE", ["очень классный работник"])],
            "title": [("MODIFY_REPLACE", ["beta-тестер"])],
        }
        self.assertDictEqual(
            self.user.diff_ldap_attrs_by_categories(user1), df
        )

    def test_diff_ldap_attrs_by_categories_2(self):
        self.maxDiff = None
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test3,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="UNN",
            department="АХУ",
            division="отдел 5",
            position="beta-тестер",
            mail="test@example.com",
            mobile="+77071234567",
            other_mailbox="1",
            other_mobile="0",
            comment="",
            employee_type="",
            acc_control=[uac.NORMAL_ACCOUNT],
            description="очень классный работник",
        )
        df = {
            "comment": [("MODIFY_DELETE", [])],
            "company": [("MODIFY_REPLACE", ["UNN"])],
            "division": [("MODIFY_REPLACE", ["отдел 5"])],
            "employeeType": [("MODIFY_DELETE", [])],
            "mobile": [("MODIFY_REPLACE", ["+77071234567"])],
            "otherMailbox": [("MODIFY_REPLACE", ["1"])],
            "otherMobile": [("MODIFY_REPLACE", ["0"])],
            "description": [("MODIFY_REPLACE", ["очень классный работник"])],
            "title": [("MODIFY_REPLACE", ["beta-тестер"])],
            "userAccountControl": [("MODIFY_REPLACE", [512])],
        }
        self.assertDictEqual(
            self.user.diff_ldap_attrs_by_categories(user1), df
        )


class TestUserMetods3(unittest.TestCase):
    def setUp(self):
        self.user = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="ННГУ",
            department="",
            division="",
            position="тестер",
            mail="",
            mobile="",
            other_mailbox="0",
            other_mobile="0",
            comment="коммент",
            employee_type="юзер",
            acc_control=[uac.NORMAL_ACCOUNT, uac.ACCOUNTDISABLE],
            description="классный работник",
        )

    def tearDown(self):
        self.user = None

    def test_diff_ldap_attrs_by_categories_3(self):
        self.maxDiff = None
        user1 = user.user(
            "pupkins",
            "76348",
            org_unit="OU=test3,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="UNN",
            department="АХУ",
            division="отдел 5",
            position="beta-тестер",
            mail="test@example.com",
            mobile="+77071234567",
            other_mailbox="1",
            other_mobile="0",
            comment="",
            employee_type="",
            acc_control=[uac.NORMAL_ACCOUNT],
            description="очень классный работник",
        )
        df = {
            "comment": [("MODIFY_DELETE", [])],
            "company": [("MODIFY_REPLACE", ["UNN"])],
            "department": [("MODIFY_ADD", ["АХУ"])],
            "mail": [("MODIFY_ADD", ["test@example.com"])],
            "division": [("MODIFY_ADD", ["отдел 5"])],
            "employeeType": [("MODIFY_DELETE", [])],
            "mobile": [("MODIFY_ADD", ["+77071234567"])],
            "otherMailbox": [("MODIFY_REPLACE", ["1"])],
            "description": [("MODIFY_REPLACE", ["очень классный работник"])],
            "title": [("MODIFY_REPLACE", ["beta-тестер"])],
            "userAccountControl": [("MODIFY_REPLACE", [512])],
        }
        self.assertDictEqual(
            self.user.diff_ldap_attrs_by_categories(user1), df
        )

    def test_diff_ldap_attrs_by_categories_4(self):
        self.maxDiff = None
        user1 = user.user(
            "pupkins",
            "763",
            org_unit="OU=test3,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="UNN",
            department="АХУ",
            division="отдел 5",
            position="beta-тестер",
            mail="test@example.com",
            mobile="+77071234567",
            other_mailbox="1",
            other_mobile="0",
            comment="",
            employee_type="",
            acc_control=[uac.NORMAL_ACCOUNT],
            description="очень классный работник",
        )
        df = {
            "comment": [("MODIFY_DELETE", [])],
            "company": [("MODIFY_REPLACE", ["UNN"])],
            "department": [("MODIFY_ADD", ["АХУ"])],
            "mail": [("MODIFY_ADD", ["test@example.com"])],
            "division": [("MODIFY_ADD", ["отдел 5"])],
            "employeeType": [("MODIFY_DELETE", [])],
            "mobile": [("MODIFY_ADD", ["+77071234567"])],
            "otherMailbox": [("MODIFY_REPLACE", ["1"])],
            "description": [("MODIFY_REPLACE", ["очень классный работник"])],
            "title": [("MODIFY_REPLACE", ["beta-тестер"])],
            "userAccountControl": [("MODIFY_REPLACE", [512])],
            "uid": [("MODIFY_REPLACE", ["763"])],
        }
        self.assertDictEqual(
            self.user.diff_ldap_attrs_by_categories(user1), df
        )

    def test_diff_ldap_attrs_by_categories_5(self):
        self.maxDiff = None
        user1 = user.user(
            "pupki",
            "763",
            org_unit="OU=ttt,DC=example,DC=com",
            surname="Пупкин",
            first_name="Пирун",
            middle_name="Гансович",
            company="UNN",
            department="АХУ",
            division="отдел 5",
            position="beta-тестер",
            mail="test@example.com",
            mobile="+77071234567",
            other_mailbox="1",
            other_mobile="0",
            comment="",
            employee_type="",
            acc_control=[uac.NORMAL_ACCOUNT],
            description="очень классный работник",
        )
        self.assertRaises(
            WrongParam,
            protouser.protouser.diff_ldap_attrs_by_categories,
            self.user,
            user1,
        )


if __name__ == "__main__":
    unittest.main()
