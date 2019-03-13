# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# Name:        user_test
# Purpose:      tests
#
# Author:      Evgeniy Semenov
#
# Created:     10.02.2017
# Copyright:   (c) Evgeniy Semenov 2017-2019
# Licence:     MIT
#-------------------------------------------------------------------------------
import unittest
import os

pd=os.path.dirname( os.path.dirname( os.path.abspath(__file__) ) )
os.sys.path.insert(0,pd)
from pyncli.ldap import user
from pyncli.ldap import protouser
from pyncli.ldap.uac import *
from pyncli.ldap.admexept import NotEnoughParams, EmptyParam, WrongParam, TooLong

class TestUserMetods(unittest.TestCase):

    def test___init_1(self):
        self.assertRaises(EmptyParam,user.user,u'',u'')

##    def test___init_2(self):
##        self.assertRaises(EmptyParam,user.user,u'pupkin',u'')

    def test___init_3(self):
        self.assertRaises(WrongParam,user.user,['t25'],u'5')

    def test___init_4(self):
        self.assertRaises(WrongParam,user.user,u'pupkin',55)

    def test___init_5(self):
        self.assertRaises(EmptyParam,user.user,u'pupkin',u'564646',
                org_unit=u'')

    def test___init_6(self):
        self.assertRaises(WrongParam,user.user,u'pupkin',u'564646',
                org_unit=u'OU=test,DC=example,DC=com',
                surname=5, first_name=u'', middle_name=u'',
                company=u'', department=u'', division=u'', position=u'',
                mail=u'', mobile=u'',
                other_mailbox=u'0', other_mobile=u'0',
                comment=u'', employee_type=u'',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE])


    def test___init_7(self):
        self.assertRaises(WrongParam,user.user,u'pupkin',u'564646',
                org_unit=u'OU=test,DC=example,DC=com',
                surname=u'', first_name=8, middle_name=u'',
                company=u'', department=u'', division=u'', position=u'',
                mail=u'', mobile=u'',
                other_mailbox=u'0', other_mobile=u'0',
                comment=u'', employee_type=u'',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE])

    def test___init_8(self):
        self.assertRaises(WrongParam,user.user,u'pupkin',u'564646',
                org_unit=u'OU=test,DC=example,DC=com',
                surname=u'', first_name=u'', middle_name=[],
                company=u'', department=u'', division=u'', position=u'',
                mail=u'', mobile=u'',
                other_mailbox=u'0', other_mobile=u'0',
                comment=u'', employee_type=u'',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE])

    def test___init_9(self):
        self.assertRaises(WrongParam,user.user,u'pupkin',u'564646',
                org_unit=u'OU=test,DC=example,DC=com',
                surname=u'', first_name=u'', middle_name=u'',
                company={}, department=u'', division=u'', position=u'',
                mail=u'', mobile=u'',
                other_mailbox=u'0', other_mobile=u'0',
                comment=u'', employee_type=u'',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE])

    def test___init_10(self):
        self.assertRaises(WrongParam,user.user,u'pupkin',u'564646',
                org_unit=u'OU=test,DC=example,DC=com',
                surname=u'', first_name=u'', middle_name=u'',
                company=u'', department=0x02, division=u'', position=u'',
                mail=u'', mobile=u'',
                other_mailbox=u'0', other_mobile=u'0',
                comment=u'', employee_type=u'',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE])


    def test___init_11(self):
        self.assertRaises(WrongParam,user.user,u'pupkin',u'564646',
                org_unit=u'OU=test,DC=example,DC=com',
                surname=u'', first_name=u'', middle_name=u'',
                company=u'', department=u'', division=0, position=u'',
                mail=u'', mobile=u'',
                other_mailbox=u'0', other_mobile=u'0',
                comment=u'', employee_type=u'',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE])

    def test___init_12(self):
        self.assertRaises(WrongParam,user.user,u'pupkin',u'564646',
                org_unit=u'OU=test,DC=example,DC=com',
                surname=u'', first_name=u'', middle_name=u'',
                company=u'', department=u'', division=u'', position=8,
                mail=u'', mobile=u'',
                other_mailbox=u'0', other_mobile=u'0',
                comment=u'', employee_type=u'',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE])

    def test___init_13(self):
        self.assertRaises(WrongParam,user.user,u'pupkin',u'564646',
                org_unit=u'OU=test,DC=example,DC=com',
                surname=u'', first_name=u'', middle_name=u'',
                company=u'', department=u'', division=u'', position=u'',
                mail=uac.NORMAL_ACCOUNT, mobile=u'',
                other_mailbox=u'0', other_mobile=u'0',
                comment=u'', employee_type=u'',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE])

    def test___init_14(self):
        self.assertRaises(WrongParam,user.user,u'pupkin',u'564646',
                org_unit=u'OU=test,DC=example,DC=com',
                surname=u'', first_name=u'', middle_name=u'',
                company=u'', department=u'', division=u'', position=u'',
                mail=u'', mobile=5,
                other_mailbox=u'0', other_mobile=u'0',
                comment=u'', employee_type=u'',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE])

    def test___init_15(self):
        self.assertRaises(WrongParam,user.user,u'pupkin',u'564646',
                org_unit=u'OU=test,DC=example,DC=com',
                surname=u'', first_name=u'', middle_name=u'',
                company=u'', department=u'', division=u'', position=u'',
                mail=u'', mobile=u'',
                other_mailbox=[], other_mobile=u'0',
                comment=u'', employee_type=u'',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE])

    def test___init_16(self):
        self.assertRaises(WrongParam,user.user,u'pupkin',u'564646',
                org_unit=u'OU=test,DC=example,DC=com',
                surname=u'', first_name=u'', middle_name=u'',
                company=u'', department=u'', division=u'', position=u'',
                mail=u'', mobile=u'',
                other_mailbox=u'', other_mobile={},
                comment=u'', employee_type=u'',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE])

    def test___init_17(self):
        self.assertRaises(WrongParam,user.user,u'pupkin',u'564646',
                org_unit=u'OU=test,DC=example,DC=com',
                surname=u'', first_name=u'', middle_name=u'',
                company=u'', department=u'', division=u'', position=u'',
                mail=u'', mobile=u'',
                other_mailbox=u'', other_mobile=u'0',
                comment=56465, employee_type=u'',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE])

    def test___init_18(self):
        self.assertRaises(WrongParam,user.user,u'pupkin',u'564646',
                org_unit=u'OU=test,DC=example,DC=com',
                surname=u'', first_name=u'', middle_name=u'',
                company=u'', department=u'', division=u'', position=u'',
                mail=u'', mobile=u'',
                other_mailbox=u'', other_mobile=u'0',
                comment=u'', employee_type=6,
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE])

    def test___init_19(self):
        self.assertRaises(WrongParam,user.user,u'pupkin',u'564646',
                org_unit=u'OU=test,DC=example,DC=com',
                surname=u'', first_name=u'', middle_name=u'',
                company=u'', department=u'', division=u'', position=u'',
                mail=u'', mobile=u'',
                other_mailbox=u'', other_mobile=u'0',
                comment=56465, employee_type=u'',
                acc_control=uac.NORMAL_ACCOUNT)

    def test___init_20(self):
        self.assertRaises(WrongParam,user.user,u'pupkin',u'564646',
                org_unit=u'OU=test,DC=example,DC=com',
                surname=u'', first_name=u'', middle_name=u'',
                company=u'', department=u'', division=u'', position=u'',
                mail=u'', mobile=u'',
                other_mailbox=u'', other_mobile=u'0',
                comment=u'', employee_type=u'',
                acc_control=uac.NORMAL_ACCOUNT,description=65476)


    def test___init_21(self):
        self.assertRaises(TooLong,user.user,u'ю'*65,u'564646',
                org_unit=u'OU=test,DC=example,DC=com',
                surname=u'', first_name=u'', middle_name=u'',
                company=u'', department=u'', division=u'', position=u'',
                mail=u'', mobile=u'',
                other_mailbox=u'', other_mobile=u'0',
                comment=u'', employee_type=u'',
                acc_control=uac.NORMAL_ACCOUNT,description=u'')

    def test___init_22(self):
        self.assertRaises(TooLong,user.user,u'pupkin',u'5'*257,
                org_unit=u'OU=test,DC=example,DC=com',
                surname=u'', first_name=u'', middle_name=u'',
                company=u'', department=u'', division=u'', position=u'',
                mail=u'', mobile=u'',
                other_mailbox=u'', other_mobile=u'0',
                comment=u'', employee_type=u'',
                acc_control=uac.NORMAL_ACCOUNT,description=u'')

    def test___init_23(self):
        self.assertRaises(TooLong,user.user,u'pupkin',u'564646',
                org_unit=u'OU=test,DC=example,DC=com'*50,
                surname=u'', first_name=u'', middle_name=u'',
                company=u'', department=u'', division=u'', position=u'',
                mail=u'', mobile=u'',
                other_mailbox=u'', other_mobile=u'0',
                comment=u'', employee_type=u'',
                acc_control=uac.NORMAL_ACCOUNT,description=u'')

    def test___init_24(self):
        self.user=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'п'*68, first_name=u'Пирун', middle_name=u'Гансович',
                company=u'ННГУ', department=u'АХУ', division=u'отдел',
                position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertEqual(self.user.surname,u'п'*64)

    def test___init_25(self):
        self.user=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'п', first_name=u'и'*80, middle_name=u'Гансович',
                company=u'ННГУ', department=u'АХУ', division=u'отдел',
                position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertEqual(self.user.first_name,u'и'*64)

    def test___init_26(self):
        self.user=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'п', first_name=u'и', middle_name=u'ч'*80,
                company=u'ННГУ', department=u'АХУ', division=u'отдел',
                position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertEqual(self.user.middle_name,u'ч'*64)

    def test___init_27(self):
        self.user=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'п', first_name=u'и', middle_name=u'ч',
                company=u'У'*80, department=u'АХУ', division=u'отдел',
                position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertEqual(self.user.company,u'У'*64)

    def test___init_28(self):
        self.user=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'п', first_name=u'и', middle_name=u'ч',
                company=u'У', department=u'Х'*80, division=u'отдел',
                position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertEqual(self.user.department,u'Х'*64)

    def test___init_29(self):
        self.user=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'п', first_name=u'и', middle_name=u'ч',
                company=u'У', department=u'Х', division=u'д'*260,
                position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertEqual(self.user.division,u'д'*256)

    def test___init_30(self):
        self.user=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'п', first_name=u'и', middle_name=u'ч',
                company=u'У', department=u'Х', division=u'д',
                position=u'р'*200,
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertEqual(self.user.position,u'р'*128)

    def test___init_31(self):
        self.user=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'п', first_name=u'и', middle_name=u'ч',
                company=u'У', department=u'Х', division=u'д',
                position=u'р',
                mail=u'm'*280, mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertEqual(self.user.mail,u'm'*256)

    def test___init_32(self):
        self.user=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'п', first_name=u'и', middle_name=u'ч',
                company=u'У', department=u'Х', division=u'д',
                position=u'р',
                mail=u'm', mobile=u'7'*66,
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertEqual(self.user.mobile,u'7'*64)

    def test___init_33(self):
        self.user=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'п', first_name=u'и', middle_name=u'ч',
                company=u'У', department=u'Х', division=u'д',
                position=u'р',
                mail=u'm', mobile=u'7',
                other_mailbox=u'0'*66, other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertEqual(self.user.other_mailbox,u'0'*64)

    def test___init_34(self):
        self.user=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'п', first_name=u'и', middle_name=u'ч',
                company=u'У', department=u'Х', division=u'д',
                position=u'р',
                mail=u'm', mobile=u'7',
                other_mailbox=u'0', other_mobile=u'1'*66,
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertEqual(self.user.other_mobile,u'1'*64)

    def test___init_35(self):
        self.user=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'п', first_name=u'и', middle_name=u'ч',
                company=u'У', department=u'Х', division=u'д',
                position=u'р',
                mail=u'm', mobile=u'7',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'к'*1200, employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertEqual(self.user.comment,u'к'*1024)

    def test___init_36(self):
        self.user=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'п', first_name=u'и', middle_name=u'ч',
                company=u'У', department=u'Х', division=u'д',
                position=u'р',
                mail=u'm', mobile=u'7',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'к', employee_type=u'ю'*280,
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertEqual(self.user.employee_type,u'ю'*256)

    def test___init_37(self):
        self.user=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'п', first_name=u'и', middle_name=u'ч',
                company=u'У', department=u'Х', division=u'д',
                position=u'р',
                mail=u'm', mobile=u'7',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'к', employee_type=u'ю',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'ы'*1200)
        self.assertEqual(self.user.description,u'ы'*1024)

    def test___init_38(self):
        self.user=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'п', first_name=u'и', middle_name=u'ч',
                company=u'У', department=u'Х', division=u'д',
                position=u'р',
                mail=u'm', mobile=u'7',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'к', employee_type=u'ю',
                acc_control=514,
                description=u'ы')

        l = uac.get_control([uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE] )
        u=uac.get_control( self.user.acc_control )
        self.assertEqual(u,l)


    def test___get_domain_1(self):
        self.assertRaises(WrongParam,user.user,u'pupkins',u'76348',
                org_unit=u'OU=test3,OU=example,OU=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'UNN', department=u'АХУ', division=u'отдел 5', position=u'beta-тестер',
                mail=u'test@example.com', mobile=u'+77071234567',
                other_mailbox=u'1', other_mobile=u'0',
                comment=u'коммент.net', employee_type=u'юзер-садист',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'очень классный работник')


    def test___get_domain_2(self):
        self.assertRaises(WrongParam,user.user,u'pupkins',u'76348',
                org_unit=u'OU=test3,du=unn,oo=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'UNN', department=u'АХУ', division=u'отдел 5', position=u'beta-тестер',
                mail=u'test@example.com', mobile=u'+77071234567',
                other_mailbox=u'1', other_mobile=u'0',
                comment=u'коммент.net', employee_type=u'юзер-садист',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'очень классный работник')

    def test___get_domain_3(self):
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test3,dc=example,DC=com,Dc=ua',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'UNN', department=u'АХУ', division=u'отдел 5', position=u'beta-тестер',
                mail=u'test@example.com', mobile=u'+77071234567',
                other_mailbox=u'1', other_mobile=u'0',
                comment=u'коммент.net', employee_type=u'юзер-садист',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'очень классный работник')
        self.assertEqual(user1.get_domain(),u'example.com.ua')

    def test___get_domain_4(self):
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test3, dc = example, DC = com, Dc =ua',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'UNN', department=u'АХУ', division=u'отдел 5', position=u'beta-тестер',
                mail=u'test@example.com', mobile=u'+77071234567',
                other_mailbox=u'1', other_mobile=u'0',
                comment=u'коммент.net', employee_type=u'юзер-садист',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'очень классный работник')
        self.assertEqual(user1.get_domain(),u'example.com.ua')

class TestUserMetods2(unittest.TestCase):

    def setUp(self):
        self.user=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'ННГУ', department=u'АХУ', division=u'отдел',
                position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')


    def tearDown(self):
        self.user=None

    def test___init_8(self):
        self.assertEqual(self.user.__class__.__name__,'user')

    def test___init_9(self):
        self.assertEqual(self.user.surname,u'Пупкин')

    def test___init_10(self):
        self.assertEqual(self.user.first_name,u'Пирун')

    def test___init_11(self):
        self.assertEqual(self.user.login,u'pupkins')

    def test___init_12(self):
        self.assertEqual(self.user.uid,u'76348')

    def test___init_13(self):
        self.assertEqual(self.user.middle_name,u'Гансович')

    def test___init_14(self):
        self.assertEqual(self.user.company,u'ННГУ')

    def test___init_15(self):
        self.assertEqual(self.user.department,u'АХУ')

    def test___init_16(self):
        self.assertEqual(self.user.division,u'отдел')

    def test___init_17(self):
        self.assertEqual(self.user.position,u'тестер')

    def test___init_18(self):
        self.assertEqual(self.user.mail,u'test@example.com')

    def test___init_19(self):
        self.assertEqual(self.user.employee_type,u'юзер')

    def test___init_20(self):
        self.assertEqual(self.user.comment,u'коммент')

    def test___init_21(self):
        self.assertEqual(self.user.mobile,u'+77771234567')

    def test___init_22(self):
        self.assertEqual(self.user.other_mailbox,u'0')

    def test___init_23(self):
        self.assertEqual(self.user.other_mobile,u'1')

    def test___init_24(self):
        self.assertEqual(self.user.acc_control,[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE])

    def test___init_25(self):
        self.assertEqual(self.user.initials,u'Г')

    def test___init_26(self):
        self.assertEqual(self.user.full_name,u'Пупкин Пирун Гансович')

    def test___init_27(self):
        self.assertEqual(self.user.dn,u'CN=pupkins,OU=test,DC=example,DC=com')

    def test___init_28(self):
        self.assertEqual(self.user.get_initials(),u'Г')

    def test___init_29(self):
        self.assertEqual(self.user.get_fullname(),u'Пупкин Пирун Гансович')

    def test___init_30(self):
        self.assertEqual(self.user.get_dn(),u'CN=pupkins,OU=test,DC=example,DC=com')

    def test___init_31(self):
        self.assertEqual(self.user.enabled,False)

    def test___init_32(self):
        self.user.enabled=True
        self.assertEqual(self.user.enabled,True)

    def test___init_33(self):
        self.user.enabled=True
        self.assertListEqual(self.user.acc_control,[uac.NORMAL_ACCOUNT,])

    def test___init_34(self):
        d={u'comment': u'коммент',
         u'division': u'отдел',
         u'displayName': u'Пупкин Пирун Гансович',
         u'uid': u'76348',
         u'otherMailbox': u'0',
         u'title': u'тестер',
         u'mobile': u'+77771234567',
         u'company': u'ННГУ',
         u'userAccountControl': u'0x202',
         u'initials': u'Г',
         u'employeeType': u'юзер',
         u'middleName': u'Гансович',
         u'otherMobile': u'1',
         u'sn': u'Пупкин',
         u'department': u'АХУ',
         u'mail': u'test@example.com',
         u'givenName': u'Пирун',
         u'sAMAccountName': u'pupkins',
         u'description': u'классный работник',
         u'userPrincipalName':u'pupkins@example.com'}

        self.assertDictEqual(self.user.get_ldap_attrs(),d)


    def test_fullname_1(self):
        self.assertEqual(self.user.get_fullname(),u'Пупкин Пирун Гансович')

    def test_initials_1(self):
        self.assertEqual(self.user.get_initials(),u'Г')

    def test___eq_1(self):
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'ННГУ', department=u'АХУ', division=u'отдел', position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertEqual(self.user, user1)

    def test___eq_2(self):
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'ННГУ', department=u'АХУ', division=u'отдел', position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertTrue(self.user==user1)

    def test___eq_3(self):
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'ПУпкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'ННГУ', department=u'АХУ', division=u'отдел', position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertFalse(self.user==user1)

    def test___eq_4(self):
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'ирун', middle_name=u'Гансович',
                company=u'ННГУ', department=u'АХУ', division=u'отдел', position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertFalse(self.user==user1)

    def test___eq_5(self):
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'ННГУ', department=u'АХУ', division=u'отдел', position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,],
                description=u'классный работник')
        self.assertFalse(self.user==user1)

    def test___ne_1(self):
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'ННГУ', department=u'АХУ', division=u'отдел', position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertFalse(self.user!=user1)

    def test___ne_2(self):
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'ННГУ', department=u'АХУ', division=u'отдел', position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'1', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertTrue(self.user!=user1)

    def test_diff_1(self):
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'Пупкина', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'ННГУ', department=u'АХУ', division=u'отдел', position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertDictEqual(self.user.diff(user1),{u'surname':u'Пупкина',u'full_name':u'Пупкина Пирун Гансович'})

    def test_diff_2(self):
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Казимир', middle_name=u'Гансович',
                company=u'ННГУ', department=u'АХУ', division=u'отдел', position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertDictEqual(self.user.diff(user1),{u'first_name':u'Казимир',u'full_name':u'Пупкин Казимир Гансович'})

    def test_diff_3(self):
        user1=user.user(u'pups',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'ННГУ', department=u'АХУ', division=u'отдел', position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertDictEqual(self.user.diff(user1),{u'login':u'pups',
            u'dn': u'CN=pups,OU=test,DC=example,DC=com',
            u'principal_name':u'pups@example.com'})

    def test_diff_4(self):
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'',
                company=u'ННГУ', department=u'АХУ', division=u'отдел', position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertDictEqual(self.user.diff(user1),{u'middle_name':u'',u'initials':u'', u'full_name':u'Пупкин Пирун'})

    def test_diff_5(self):
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'Фирма', department=u'АХУ', division=u'отдел', position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertDictEqual(self.user.diff(user1),{u'company':u'Фирма'})

    def test_diff_6(self):
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'ННГУ', department=u'Департамент', division=u'отдел', position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertDictEqual(self.user.diff(user1),{u'department':u'Департамент'})

    def test_diff_7(self):
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'ННГУ', department=u'АХУ', division=u'Бригада С', position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertDictEqual(self.user.diff(user1),{u'division':u'Бригада С'})

    def test_diff_8(self):
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'ННГУ', department=u'АХУ', division=u'отдел', position=u'кодер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertDictEqual(self.user.diff(user1),{u'position':u'кодер'})

    def test_diff_9(self):
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'ННГУ', department=u'АХУ', division=u'отдел', position=u'тестер',
                mail=u'test_1@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertDictEqual(self.user.diff(user1),{u'mail':u'test_1@example.com'})

    def test_diff_10(self):
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'ННГУ', department=u'АХУ', division=u'отдел', position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'soratnik',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertDictEqual(self.user.diff(user1),{u'employee_type':u'soratnik'})

    def test_diff_11(self):
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'ННГУ', department=u'АХУ', division=u'отдел', position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'ударник', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertDictEqual(self.user.diff(user1),{u'comment':u'ударник'})

    def test_diff_12(self):
        self.maxDiff=None
        user1=user.user(u'rabbe',u'666',org_unit=u'OU=best,DC=example,DC=com',
                surname=u'Рабинович', first_name=u'Изя', middle_name=u'Мойшевич',
                company=u'Рога и Копыта', department=u'служба быта', division=u'отдел сбыта',
                position=u'сурдопереводчик',
                mail=u'test@best.com', mobile=u'+77776666666',
                other_mailbox=u'1', other_mobile=u'0',
                comment=u'характер - нордический', employee_type=u'профи',
                acc_control=[uac.PASSWD_NOTREQD, uac.SMARTCARD_REQUIRED],
                description=u'классный работник 2')
        df={u'surname':u'Рабинович', u'login':u'rabbe', u'uid':u'666',
            u'first_name':u'Изя', u'middle_name':u'Мойшевич', u'initials':u'М',
            u'company':u'Рога и Копыта', u'division':u'отдел сбыта',
            u'department':u'служба быта',
            u'position':u'сурдопереводчик', u'full_name':u'Рабинович Изя Мойшевич',
            u'employee_type':u'профи', u'mail':u'test@best.com',
            u'comment':u'характер - нордический', u'dn':u'CN=rabbe,OU=best,DC=example,DC=com',
            u'mobile':u'+77776666666', u'other_mailbox':u'1', u'other_mobile':u'0',
            u'acc_control':[uac.PASSWD_NOTREQD, uac.SMARTCARD_REQUIRED],
            u'org_unit':u'OU=best,DC=example,DC=com',
            u'description':u'классный работник 2',
            u'principal_name':u'rabbe@example.com',
           }

        self.assertDictEqual(self.user.diff(user1),df)


    def test_diff_13(self):
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'ННГУ', department=u'АХУ', division=u'отдел', position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234560',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertDictEqual(self.user.diff(user1),{u'mobile':u'+77771234560'})


    def test_diff_14(self):
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'ННГУ', department=u'АХУ', division=u'отдел', position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'1', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertDictEqual(self.user.diff(user1),{u'other_mailbox':u'1'})

    def test_diff_15(self):
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'ННГУ', department=u'АХУ', division=u'отдел', position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'0',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertDictEqual(self.user.diff(user1),{u'other_mobile':u'0'})

    def test_diff_16(self):
        user1=user.user(u'pupkins',u'0',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'ННГУ', department=u'АХУ', division=u'отдел', position=u'тестер',
                mail=u'test@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')
        self.assertDictEqual(self.user.diff(user1),{u'uid':u'0'})

    def test_get_ldap_attrs_1(self):
        a={u'comment': u'коммент',
            u'company': u'ННГУ',
            u'department': u'АХУ',
            u'displayName': u'Пупкин Пирун Гансович',
            u'division': u'отдел',
            u'employeeType': u'юзер',
            u'givenName': u'Пирун',
            u'initials': u'Г',
            u'mail': u'test@example.com',
            u'middleName': u'Гансович',
            u'mobile': u'+77771234567',
            u'otherMailbox': u'0',
            u'otherMobile': u'1',
            u'sAMAccountName': u'pupkins',
            u'sn': u'Пупкин',
            u'title': u'тестер',
            u'uid': u'76348',
            u'userAccountControl': u'0x202',
            u'description':u'классный работник',
            u'userPrincipalName':u'pupkins@example.com'}

        self.assertDictEqual(self.user.get_ldap_attrs(),a)

    def test_diff_ldap_attrs_1(self):
        user1=user.user(u'popkina',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'Попкина', first_name=u'Матильда', middle_name=u'Гансовна',
                company=u'ННГУ', department=u'не АХУ', division=u'отдел', position=u'тестер',
                mail=u'popna@example.com', mobile=u'+77771234567',
                other_mailbox=u'0', other_mobile=u'1',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,],
                description=u'классный работник')
        df={

            u'department': u'не АХУ',
            u'displayName': u'Попкина Матильда Гансовна',
            u'givenName': u'Матильда',
            u'mail': u'popna@example.com',
            u'middleName': u'Гансовна',
            u'sAMAccountName': u'popkina',
            u'sn': u'Попкина',
            u'userAccountControl': u'0x200',
            u'userPrincipalName':u'popkina@example.com'}
        self.assertDictEqual(self.user.diff_ldap_attrs(user1),df)

    def test_diff_ldap_attrs_2(self):
        self.maxDiff=None
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test3,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'UNN', department=u'АХУ', division=u'отдел 5', position=u'beta-тестер',
                mail=u'test@example.com', mobile=u'+77071234567',
                other_mailbox=u'1', other_mobile=u'0',
                comment=u'коммент.net', employee_type=u'юзер-садист',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'очень классный работник')
        df={u'comment': u'коммент.net',
            u'company': u'UNN',


            u'division': u'отдел 5',
            u'employeeType': u'юзер-садист',
            u'mobile': u'+77071234567',
            u'otherMailbox': u'1',
            u'otherMobile': u'0',
            u'description': u'очень классный работник',
            u'title': u'beta-тестер',
            }
        self.assertDictEqual(self.user.diff_ldap_attrs(user1),df)



    def test_diff_ldap_attrs_by_categories_1(self):
        self.maxDiff=None
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test3,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'UNN', department=u'АХУ', division=u'отдел 5', position=u'beta-тестер',
                mail=u'test@example.com', mobile=u'+77071234567',
                other_mailbox=u'1', other_mobile=u'0',
                comment=u'коммент.net', employee_type=u'юзер-садист',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'очень классный работник')
        df={u'comment': [('MODIFY_REPLACE', [u'коммент.net'])],
            u'company': [('MODIFY_REPLACE', [u'UNN'])],


            u'division': [('MODIFY_REPLACE', [u'отдел 5'])],
            u'employeeType': [('MODIFY_REPLACE', [u'юзер-садист'])],
            u'mobile': [('MODIFY_REPLACE', [u'+77071234567'])],
            u'otherMailbox': [('MODIFY_REPLACE', [u'1'])],
            u'otherMobile': [('MODIFY_REPLACE', [u'0'])],
            u'description': [('MODIFY_REPLACE', [u'очень классный работник'])],
            u'title': [('MODIFY_REPLACE', [u'beta-тестер'])],
            }
        self.assertDictEqual(self.user.diff_ldap_attrs_by_categories(user1),df)


    def test_diff_ldap_attrs_by_categories_2(self):
        self.maxDiff=None
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test3,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'UNN', department=u'АХУ', division=u'отдел 5', position=u'beta-тестер',
                mail=u'test@example.com', mobile=u'+77071234567',
                other_mailbox=u'1', other_mobile=u'0',
                comment=u'', employee_type=u'',
                acc_control=[uac.NORMAL_ACCOUNT,],
                description=u'очень классный работник')
        df={u'comment': [('MODIFY_DELETE', [])],
            u'company': [('MODIFY_REPLACE', [u'UNN'])],


            u'division': [('MODIFY_REPLACE', [u'отдел 5'])],
            u'employeeType': [('MODIFY_DELETE', [])],
            u'mobile': [('MODIFY_REPLACE', [u'+77071234567'])],
            u'otherMailbox': [('MODIFY_REPLACE', [u'1'])],
            u'otherMobile': [('MODIFY_REPLACE', [u'0'])],
            u'description': [('MODIFY_REPLACE', [u'очень классный работник'])],
            u'title': [('MODIFY_REPLACE', [u'beta-тестер'])],
            u'userAccountControl': [('MODIFY_REPLACE', [512])],
            }
        self.assertDictEqual(self.user.diff_ldap_attrs_by_categories(user1),df)

class TestUserMetods3(unittest.TestCase):

    def setUp(self):
        self.user=user.user(u'pupkins',u'76348',org_unit=u'OU=test,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'ННГУ', department=u'', division=u'',
                position=u'тестер',
                mail=u'', mobile=u'',
                other_mailbox=u'0', other_mobile=u'0',
                comment=u'коммент', employee_type=u'юзер',
                acc_control=[uac.NORMAL_ACCOUNT,uac.ACCOUNTDISABLE],
                description=u'классный работник')


    def tearDown(self):
        self.user=None

    def test_diff_ldap_attrs_by_categories_3(self):
        self.maxDiff=None
        user1=user.user(u'pupkins',u'76348',org_unit=u'OU=test3,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'UNN', department=u'АХУ', division=u'отдел 5', position=u'beta-тестер',
                mail=u'test@example.com', mobile=u'+77071234567',
                other_mailbox=u'1', other_mobile=u'0',
                comment=u'', employee_type=u'',
                acc_control=[uac.NORMAL_ACCOUNT,],
                description=u'очень классный работник')
        df={u'comment': [('MODIFY_DELETE', [])],
            u'company': [('MODIFY_REPLACE', [u'UNN'])],
            u'department' : [('MODIFY_ADD', [u'АХУ'])],
            u'mail' : [('MODIFY_ADD', [u'test@example.com'])],
            u'division': [('MODIFY_ADD', [u'отдел 5'])],
            u'employeeType': [('MODIFY_DELETE', [])],
            u'mobile': [('MODIFY_ADD', [u'+77071234567'])],
            u'otherMailbox': [('MODIFY_REPLACE', [u'1'])],

            u'description': [('MODIFY_REPLACE', [u'очень классный работник'])],
            u'title': [('MODIFY_REPLACE', [u'beta-тестер'])],
            u'userAccountControl': [('MODIFY_REPLACE', [512])],
            }
        self.assertDictEqual(self.user.diff_ldap_attrs_by_categories(user1),df)


    def test_diff_ldap_attrs_by_categories_4(self):
        self.maxDiff=None
        user1=user.user(u'pupkins',u'763',org_unit=u'OU=test3,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'UNN', department=u'АХУ', division=u'отдел 5', position=u'beta-тестер',
                mail=u'test@example.com', mobile=u'+77071234567',
                other_mailbox=u'1', other_mobile=u'0',
                comment=u'', employee_type=u'',
                acc_control=[uac.NORMAL_ACCOUNT,],
                description=u'очень классный работник')
        df={u'comment': [('MODIFY_DELETE', [])],
            u'company': [('MODIFY_REPLACE', [u'UNN'])],
            u'department' : [('MODIFY_ADD', [u'АХУ'])],
            u'mail' : [('MODIFY_ADD', [u'test@example.com'])],
            u'division': [('MODIFY_ADD', [u'отдел 5'])],
            u'employeeType': [('MODIFY_DELETE', [])],
            u'mobile': [('MODIFY_ADD', [u'+77071234567'])],
            u'otherMailbox': [('MODIFY_REPLACE', [u'1'])],

            u'description': [('MODIFY_REPLACE', [u'очень классный работник'])],
            u'title': [('MODIFY_REPLACE', [u'beta-тестер'])],
            u'userAccountControl': [('MODIFY_REPLACE', [512])],
            u'uid' : [('MODIFY_REPLACE', [u'763'])],
            }
        self.assertDictEqual(self.user.diff_ldap_attrs_by_categories(user1),df)

    def test_diff_ldap_attrs_by_categories_5(self):
        self.maxDiff=None
        user1=user.user(u'pupki',u'763',org_unit=u'OU=ttt,DC=example,DC=com',
                surname=u'Пупкин', first_name=u'Пирун', middle_name=u'Гансович',
                company=u'UNN', department=u'АХУ', division=u'отдел 5', position=u'beta-тестер',
                mail=u'test@example.com', mobile=u'+77071234567',
                other_mailbox=u'1', other_mobile=u'0',
                comment=u'', employee_type=u'',
                acc_control=[uac.NORMAL_ACCOUNT,],
                description=u'очень классный работник')
        self.assertRaises(WrongParam,protouser.protouser.diff_ldap_attrs_by_categories, self.user, user1)

if __name__ == '__main__':
    unittest.main()
